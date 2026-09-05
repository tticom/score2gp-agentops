import importlib.util
import subprocess
from pathlib import Path

import pytest

RUNTIME = Path(__file__).parents[1] / "agent-runtime"
spec = importlib.util.spec_from_file_location("task_branch", RUNTIME / "task_branch.py")
task = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task)


def run(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True, check=True).stdout.strip()


@pytest.fixture
def repos(tmp_path, monkeypatch):
    config = tmp_path / "gitconfig"
    config.write_text('[user]\n name = Test Worker\n email = worker@example.invalid\n')
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(config))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    remote = tmp_path / "remote.git"
    source = tmp_path / "source"
    source.mkdir()
    run(source, "init", "-b", "main")
    (source / "file.txt").write_text("base\n")
    run(source, "add", "file.txt")
    run(source, "commit", "-m", "base")
    run(source, "init", "--bare", str(remote))
    run(source, "remote", "add", "origin", str(remote))
    run(source, "push", "origin", "main")
    run(remote, "symbolic-ref", "HEAD", "refs/heads/main")
    # GitHub policy is tested separately; lifecycle tests use real local transport.
    monkeypatch.setattr(task, "github_remote", lambda url: url)
    return source, remote, tmp_path / "worker"


def test_publish_and_resume_from_remote_in_fresh_clone(repos):
    source, remote, worker = repos
    receipt = task.prepare(source, worker, "feat/example", "main")
    assert receipt["head"] == run(remote, "rev-parse", "refs/heads/feat/example")
    assert (worker / ".git").is_dir()
    assert not (worker / ".git/objects/info/alternates").exists()
    (worker / "file.txt").write_text("unfinished but saved work\n")
    run(worker, "add", "file.txt")
    run(worker, "commit", "-m", "checkpoint: incomplete implementation")
    task.checkpoint(worker, "feat/example", str(remote))
    recovered = worker.with_name("fresh-worker")
    task.prepare(source, recovered, "feat/example", "main")
    assert (recovered / "file.txt").read_text() == "unfinished but saved work\n"
    assert run(recovered, "rev-parse", "HEAD") == run(worker, "rev-parse", "HEAD")
    assert run(source, "branch", "--show-current") == "main"


@pytest.mark.parametrize("branch", ["main", "master", "", "HEAD", "bad branch", "feat/../main"])
def test_protected_or_invalid_branch_rejected(repos, branch):
    source, _, worker = repos
    with pytest.raises(task.CheckpointError):
        task.prepare(source, worker, branch, "main")
    assert not worker.exists()


def test_dirty_work_is_preserved_and_cannot_be_reported_pushed(repos):
    source, remote, worker = repos
    task.prepare(source, worker, "feat/example", "main")
    original = run(remote, "rev-parse", "refs/heads/feat/example")
    (worker / "new.txt").write_text("do not lose this")
    with pytest.raises(task.CheckpointError, match="uncommitted"):
        task.checkpoint(worker, "feat/example", str(remote))
    with pytest.raises(task.CheckpointError, match="uncommitted"):
        task.prepare(source, worker, "feat/example", "main")
    assert (worker / "new.txt").read_text() == "do not lose this"
    assert run(remote, "rev-parse", "refs/heads/feat/example") == original


def test_diverged_histories_not_overwritten(repos):
    source, remote, worker = repos
    task.prepare(source, worker, "feat/example", "main")
    other = worker.with_name("other")
    task.prepare(source, other, "feat/example", "main")
    for repo, text in [(worker, "local"), (other, "remote")]:
        (repo / "file.txt").write_text(text)
        run(repo, "add", "file.txt")
        run(repo, "commit", "-m", text)
    task.checkpoint(other, "feat/example", str(remote))
    local_head = run(worker, "rev-parse", "HEAD")
    remote_sha = run(other, "rev-parse", "HEAD")
    with pytest.raises(task.CheckpointError, match="diverged"):
        task.prepare(source, worker, "feat/example", "main")
    assert run(worker, "rev-parse", "HEAD") == local_head
    assert run(remote, "rev-parse", "refs/heads/feat/example") == remote_sha


def test_rejected_push_and_review_never_publish(repos):
    source, remote, worker = repos
    task.prepare(source, worker, "feat/example", "main")
    hook = remote / "hooks/pre-receive"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o755)
    (worker / "file.txt").write_text("local checkpoint")
    run(worker, "add", "file.txt")
    run(worker, "commit", "-m", "checkpoint")
    local = run(worker, "rev-parse", "HEAD")
    with pytest.raises(task.CheckpointError, match="git push failed"):
        task.checkpoint(worker, "feat/example", str(remote))
    with pytest.raises(task.CheckpointError, match="remote HEAD differs"):
        task.checkpoint(worker, "feat/example", str(remote), publish=False)
    assert run(worker, "rev-parse", "HEAD") == local


def test_detached_and_alternate_push_url_refused(repos):
    source, remote, worker = repos
    task.prepare(source, worker, "feat/example", "main")
    run(worker, "switch", "--detach")
    with pytest.raises(task.CheckpointError, match="detached"):
        task.checkpoint(worker, "feat/example", str(remote))
    run(worker, "switch", "feat/example")
    run(worker, "remote", "set-url", "--push", "origin", "https://github.com/other/wrong.git")
    with pytest.raises(task.CheckpointError, match="URL mismatch"):
        task.checkpoint(worker, "feat/example", str(remote))


def test_github_remote_rejects_embedded_token_and_other_hosts():
    for remote in ["https://token@github.com/tticom/repo.git", "https://evil.invalid/repo.git", "/tmp/repo.git"]:
        with pytest.raises(task.CheckpointError):
            task.github_remote(remote)
    assert task.github_remote("https://github.com/tticom/score2gp.git")
