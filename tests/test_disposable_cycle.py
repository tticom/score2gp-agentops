"""Real Git repositories exercise checkpoint and recovery; Docker has a separate smoke test."""
from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


RUNTIME = Path(__file__).parents[1] / "agent-runtime"
spec = importlib.util.spec_from_file_location("disposable_cycle", RUNTIME / "cycle.py")
cycle = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = cycle
spec.loader.exec_module(cycle)


def git(path, *args):
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()


@pytest.fixture
def repository(tmp_path):
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
    source = tmp_path / "source"
    subprocess.run(["git", "clone", str(remote), str(source)], check=True, capture_output=True)
    git(source, "config", "user.name", "Fixture author")
    git(source, "config", "user.email", "fixture@example.invalid")
    (source / "src").mkdir()
    (source / "src/example.py").write_text("value = 1\n")
    git(source, "add", ".")
    git(source, "commit", "-m", "Initial source")
    git(source, "branch", "-M", "main")
    git(source, "push", "origin", "main")
    git(source, "switch", "-c", "feat/example")
    git(source, "push", "origin", "feat/example")
    return remote, source


def assignment(**changes):
    data = dict(version=1, task="example", role="automation", mode="author",
                repository="https://github.com/tticom/score2gp.git",
                branch="feat/example", base_sha="a" * 40,
                allowed_paths=["src/"], validation=[["python", "-m", "pytest"]],
                egress_hosts=["api.github.com", "github.com"],
                prompt="Implement the assigned example and report validation.")
    data.update(changes)
    return data


@pytest.mark.parametrize("change,expected_error", [
    ({"branch": "main"}, "an explicit non-protected task branch is required"),
    ({"branch": "master"}, "an explicit non-protected task branch is required"),
    ({"branch": "HEAD"}, "an explicit non-protected task branch is required"),
    ({"allowed_paths": ["../"]}, "allowed_paths must contain explicit safe files or directory prefixes"),
    ({"allowed_paths": ["."]}, "allowed_paths must contain explicit safe files or directory prefixes"),
    ({"allowed_paths": ["fixtures/private/"]}, "allowed_paths must contain explicit safe files or directory prefixes"),
    ({"allowed_paths": [".git/"]}, "allowed_paths must contain explicit safe files or directory prefixes"),
    ({"base_sha": "main"}, "base_sha must pin the assigned branch head"),
    ({"egress_hosts": ["*.google.com"]}, "egress_hosts requires exact DNS names, without wildcards or IP addresses"),
    ({"egress_hosts": ["127.0.0.1"]}, "egress_hosts requires exact DNS names, without wildcards or IP addresses"),
    ({"validation": ["echo pass"]}, "validation must contain nonempty command argument arrays"),
    ({"repository": "https://user:token@github.com/tticom/score2gp.git"},
     "repository must be an approved GitHub HTTPS repository without credentials"),
    ({"mode": "reviewer", "pull_request": 1, "allowed_paths": ["src/"]},
     "reviewer requires a PR number and no writable source paths"),
])
def test_assignment_rejects_ambiguous_or_excessive_authority(change, expected_error):
    with pytest.raises(cycle.CycleError, match=f"^{expected_error}$"):
        cycle.validate_assignment(assignment(**change))


def test_checkpoint_pushes_only_assigned_branch_and_records_validation(repository, tmp_path):
    remote, source = repository
    base = git(source, "rev-parse", "HEAD")
    clone = tmp_path / "cycle-clone"
    cycle.clone_branch(str(remote), "feat/example", base, clone, os.environ.copy())
    assert (clone / ".git").is_dir()
    assert not (clone / ".git/objects/info/alternates").exists()
    (clone / "src/example.py").write_text("value = 2\n")
    head = cycle.checkpoint(clone, str(remote), "feat/example", base, ["src/"],
                            {"cycle_id": "example", "validation": [{"exit_code": 1}]},
                            "Fixture author", "fixture@example.invalid", os.environ.copy())
    assert git(remote, "rev-parse", "refs/heads/feat/example") == head
    assert git(remote, "rev-parse", "refs/heads/main") == base
    assert json.loads(git(clone, "show", "-s", "--format=%b", "HEAD"))["validation"][0]["exit_code"] == 1
    assert not git(clone, "status", "--porcelain")


@pytest.mark.parametrize("committed", [False, True])
def test_private_or_out_of_scope_changes_block_checkpoint(repository, tmp_path, committed):
    remote, source = repository
    base = git(source, "rev-parse", "HEAD")
    clone = tmp_path / "cycle-clone"
    cycle.clone_branch(str(remote), "feat/example", base, clone, os.environ.copy())
    (clone / "private").mkdir()
    (clone / "private/secret.txt").write_text("synthetic infrastructure test marker\n")
    if committed:
        git(clone, "-c", "user.name=Fixture", "-c", "user.email=f@example.invalid", "add", ".")
        git(clone, "-c", "user.name=Fixture", "-c", "user.email=f@example.invalid", "commit", "-m", "Forbidden path")
    with pytest.raises(cycle.CycleError, match="^out-of-scope path; clone retained:"):
        cycle.checkpoint(clone, str(remote), "feat/example", base, ["src/"],
                         {"cycle_id": "example"}, "Fixture", "f@example.invalid", os.environ.copy())
    assert clone.exists()
    assert git(remote, "rev-parse", "refs/heads/feat/example") == base


def test_concurrent_remote_change_retains_clone_without_overwriting(repository, tmp_path):
    remote, source = repository
    base = git(source, "rev-parse", "HEAD")
    clone = tmp_path / "cycle-clone"
    cycle.clone_branch(str(remote), "feat/example", base, clone, os.environ.copy())
    (source / "src/example.py").write_text("value = 3\n")
    git(source, "commit", "-am", "Concurrent change")
    git(source, "push", "origin", "feat/example")
    other_head = git(source, "rev-parse", "HEAD")
    (clone / "src/example.py").write_text("value = 2\n")
    with pytest.raises(cycle.CycleError, match="^remote branch moved during cycle; clone retained$"):
        cycle.checkpoint(clone, str(remote), "feat/example", base, ["src/"],
                         {"cycle_id": "example"}, "Fixture", "f@example.invalid", os.environ.copy())
    assert clone.exists()
    assert git(remote, "rev-parse", "refs/heads/feat/example") == other_head


def test_worker_git_hook_cannot_execute_on_host(repository, tmp_path):
    remote, source = repository
    base = git(source, "rev-parse", "HEAD")
    clone = tmp_path / "cycle-clone"
    cycle.clone_branch(str(remote), "feat/example", base, clone, os.environ.copy())
    sentinel = tmp_path / "unsafe-host-execution"
    hook = clone / ".git/hooks/pre-commit"
    hook.write_text(f"#!/bin/sh\ntouch '{sentinel}'\n")
    hook.chmod(0o755)
    cycle.checkpoint(clone, str(remote), "feat/example", base, ["src/"],
                     {"cycle_id": "example"}, "Fixture", "f@example.invalid", os.environ.copy())
    assert not sentinel.exists()


@pytest.fixture
def controller(repository, tmp_path, monkeypatch):
    """Real Git transport; stub only cloud identity and Docker (tested separately)."""
    remote, source = repository
    home = tmp_path / "home"
    home.mkdir()
    root = tmp_path / "cycles"
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("SCORE2GP_CYCLE_ROOT", str(root))
    monkeypatch.setenv("SCORE2GP_GCP_PROJECT_ID", "test-project")
    monkeypatch.setenv("AGY_SKILLS_DIR", str(source))
    monkeypatch.delenv("SCORE2GP_AGENT_ROLE", raising=False)
    actual_run = subprocess.run
    state = {"docker": [], "validation_exit": 0, "worker_exit": 0, "interrupt": False,
             "login": "tticom-automation", "review_published": False}
    def boundary(args, **kwargs):
        args = [str(a) for a in args]
        if args[0] == "gcloud":
            return subprocess.CompletedProcess(args, 0, "infrastructure-test-token", "")
        if args[0] == "gh":
            if args[1:3] == ["api", "user"]:
                return subprocess.CompletedProcess(args, 0, state["login"], "")
            if "--slurp" in args:
                folder = next(root.iterdir())
                cycle_id = json.loads((folder / "receipt.json").read_text())["cycle_id"]
                reviews = [[{"user": {"login": state["login"]}, "commit_id": git(source, "rev-parse", "HEAD"),
                            "state": "COMMENTED", "body": f"<!-- score2gp-cycle:{cycle_id} -->",
                            "html_url": "https://github.com/tticom/score2gp/pull/1#pullrequestreview-1"}]] if state["review_published"] else [[]]
                return subprocess.CompletedProcess(args, 0, json.dumps(reviews), "")
            if state.get("pr_create_fail"):
                if args[1:3] == ["pr", "create"]:
                    return subprocess.CompletedProcess(args, 1, "", "pr create failed")
                if args[1:3] == ["pr", "list"]:
                    return subprocess.CompletedProcess(args, 0, "[]", "")
            branch_name = "feat/example"
            if "--head" in args:
                branch_name = args[args.index("--head") + 1]
            current_remote_head = git(remote, "rev-parse", f"refs/heads/{branch_name}")
            pr = {
                "number": 1 if branch_name == "feat/example" else 2,
                "url": f"https://github.com/tticom/score2gp/pull/{1 if branch_name == 'feat/example' else 2}",
                "headRefOid": current_remote_head,
                "head": {"sha": current_remote_head, "ref": branch_name,
                         "repo": {"full_name": "tticom/score2gp"}},
                "user": {"login": "other-author"},
                "state": "open",
            }
            if args[1:3] == ["pr", "list"]:
                return subprocess.CompletedProcess(args, 0, json.dumps([pr]), "")
            return subprocess.CompletedProcess(args, 0, json.dumps(pr), "")
        if args[0] == "git":
            args = [str(remote) if a == "https://github.com/tticom/score2gp.git" else a for a in args]
            return actual_run(args, **kwargs)
        if args[0] == "docker":
            state["docker"].append(args)
            if args[1:3] == ["image", "inspect"]:
                return subprocess.CompletedProcess(args, 0, "sha256:" + "a" * 64, "")
            if "/worker.py" in args and args[1] == "run":
                assert not any("github-askpass.sh" in arg or "GIT_ASKPASS=" in arg for arg in args)
                mounts = [args[i + 1] for i, a in enumerate(args[:-1]) if a == "--mount"]
                source_mount = next(m for m in mounts if "dst=/workspace/score2gp" in m)
                repo = Path(source_mount.split("src=", 1)[1].split(",", 1)[0])
                secret_mount = next(m for m in mounts if "dst=/run/secrets/github-token" in m)
                secret = Path(secret_mount.split("src=", 1)[1].split(",", 1)[0])
                assert secret.stat().st_mode & 0o777 == 0o600
                assert secret.read_text() == "infrastructure-test-token"
                if state["login"] == "tticom-automation":
                    (repo / "src/example.py").write_text("value = 2\n")
                else:
                    assert source_mount.endswith(",readonly")
                if state["interrupt"]:
                    raise KeyboardInterrupt
                return subprocess.CompletedProcess(args, state["worker_exit"], "", "")
            if args[1] == "run" and "--network" in args and args[args.index("--network") + 1] == "none":
                assert not any("github-token" in arg or "/auth/" in arg for arg in args)
                return subprocess.CompletedProcess(args, state["validation_exit"], "", "")
            return subprocess.CompletedProcess(args, 0, "", "")
        return actual_run(args, **kwargs)
    monkeypatch.setattr(subprocess, "run", boundary)
    data = assignment(base_sha=git(source, "rev-parse", "HEAD"))
    return data, state, root, remote


def test_controller_disposes_only_after_remote_readback_and_next_cycle_resumes(controller):
    data, state, root, remote = controller
    assert cycle.execute(data, "codex", []) == 0
    first = next(root.iterdir())
    receipt = json.loads((first / "receipt.json").read_text())
    assert receipt["status"] == "complete"
    assert receipt["published_head"] == git(remote, "rev-parse", "refs/heads/feat/example")
    assert not (first / "repo").exists()
    assert not (first / "skills").exists()
    assert not (first / "github-token").exists()
    data["base_sha"] = receipt["published_head"]
    assert cycle.execute(data, "codex", []) == 0
    assert len(list(root.iterdir())) == 2
    assert all(not (folder / "repo").exists() for folder in root.iterdir())


@pytest.mark.parametrize("failure", ["worker_exit", "validation_exit", "interrupt", "push"])
def test_controller_retains_failed_cycles_and_always_removes_secrets(controller, failure):
    data, state, root, remote = controller
    if failure == "push":
        hook = remote / "hooks/pre-receive"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
    else:
        state[failure] = 1
    assert cycle.execute(data, "codex", []) == 1
    folder = next(root.iterdir())
    assert (folder / "repo/src/example.py").read_text() == "value = 2\n"
    assert not (folder / "github-token").exists()
    receipt = json.loads((folder / "receipt.json").read_text())
    assert receipt["status"] == "retained"
    head = git(remote, "rev-parse", "refs/heads/feat/example")
    if failure == "validation_exit":
        assert head == receipt["published_head"]
        assert json.loads(git(remote, "show", "-s", "--format=%b", head))["validation"][0]["exit_code"] == 1
    else:
        assert head == data["base_sha"]
    assert any(args[1:3] == ["rm", "--force"] for args in state["docker"])


@pytest.mark.parametrize("published", [False, True])
def test_reviewer_never_pushes_source_and_requires_remote_review_receipt(controller, published):
    data, state, root, remote = controller
    state.update(login="tticom-codex", review_published=published)
    data.update(role="codex", mode="reviewer", allowed_paths=[], pull_request=1)
    assert cycle.execute(data, "codex", []) == (0 if published else 1)
    assert git(remote, "rev-parse", "refs/heads/feat/example") == data["base_sha"]
    folder = next(root.iterdir())
    assert (folder / "repo").exists() != published
    assert not (folder / "github-token").exists()


def test_bootstrap_switches_clean_controller_checkout_to_main(repository, tmp_path):
    remote, source = repository
    scripts = source / "agent-runtime/scripts"
    scripts.mkdir(parents=True)
    configure = scripts / "configure-shell-startup.sh"
    configure.write_text((RUNTIME / "scripts/configure-shell-startup.sh").read_text())
    configure.chmod(0o755)
    git(source, "add", ".")
    git(source, "commit", "-m", "Bootstrap fixture")
    git(source, "push", "origin", "HEAD:main")
    binaries = tmp_path / "bin"
    binaries.mkdir()
    docker = binaries / "docker"
    docker.write_text("#!/bin/sh\nexit 0\n")
    docker.chmod(0o755)
    workspace = tmp_path / "workspace"
    env = os.environ.copy()
    env.update(PATH=f"{binaries}:{env['PATH']}", SCORE2GP_WORKSPACE_ROOT=str(workspace),
               AGENTOPS_REPO=str(remote), AGY_SKILLS_REPO=str(remote), AGENTOPS_REF="main", AGY_SKILLS_REF="main",
               SCORE2GP_SHELL_STARTUP_FILE=str(tmp_path / "bashrc"))
    command = [str(RUNTIME / "scripts/bootstrap-instance.sh")]
    first = subprocess.run(command, env=env, capture_output=True, text=True)
    assert first.returncode == 0, first.stderr
    checkout = workspace / "score2gp-agentops"
    git(checkout, "switch", "-c", "feat/unfinished")
    second = subprocess.run(command, env=env, capture_output=True, text=True)
    assert second.returncode == 0, second.stderr
    assert git(checkout, "branch", "--show-current") == "main"
    assert not (workspace / "score2gp").exists()


def test_bootstrap_refuses_dirty_controller_checkout(repository, tmp_path):
    remote, source = repository
    scripts = source / "agent-runtime/scripts"
    scripts.mkdir(parents=True)
    configure = scripts / "configure-shell-startup.sh"
    configure.write_text((RUNTIME / "scripts/configure-shell-startup.sh").read_text())
    configure.chmod(0o755)
    git(source, "add", ".")
    git(source, "commit", "-m", "Bootstrap fixture")
    git(source, "push", "origin", "HEAD:main")
    binaries = tmp_path / "bin"
    binaries.mkdir()
    docker = binaries / "docker"
    docker.write_text("#!/bin/sh\nexit 0\n")
    docker.chmod(0o755)
    workspace = tmp_path / "workspace"
    env = os.environ.copy()
    env.update(PATH=f"{binaries}:{env['PATH']}", SCORE2GP_WORKSPACE_ROOT=str(workspace),
               AGENTOPS_REPO=str(remote), AGY_SKILLS_REPO=str(remote), AGENTOPS_REF="main", AGY_SKILLS_REF="main",
               SCORE2GP_SHELL_STARTUP_FILE=str(tmp_path / "bashrc"))
    command = [str(RUNTIME / "scripts/bootstrap-instance.sh")]
    first = subprocess.run(command, env=env, capture_output=True, text=True)
    assert first.returncode == 0, first.stderr
    checkout = workspace / "score2gp-agentops"
    (checkout / "uncommitted.txt").write_text("unfinished work\n")
    second = subprocess.run(command, env=env, capture_output=True, text=True)
    assert second.returncode == 75
    assert "dirty repository" in second.stderr


def test_cycle_run_preserves_safe_cloud_diagnostic(monkeypatch):
    def run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 1, "", "ERROR: PERMISSION_DENIED secret=topsecret")

    monkeypatch.setattr(cycle.subprocess, "run", run)
    with pytest.raises(cycle.CycleError, match="PERMISSION_DENIED") as error:
        cycle.run(["gcloud", "secrets"])
    assert "topsecret" not in str(error.value)
    assert "REDACTED" in str(error.value)


def test_author_cycle_retained_when_pr_creation_fails(controller):
    data, state, root, remote = controller
    state["pr_create_fail"] = True
    assert cycle.execute(data, "codex", []) == 1
    folder = next(root.iterdir())
    assert (folder / "repo").exists()
    receipt = json.loads((folder / "receipt.json").read_text())
    assert receipt["status"] == "retained"
    assert "PR creation failed" in receipt.get("reason", "")


def test_remote_branch_moved_after_assignment_retains_cycle(controller):
    data, state, root, remote = controller
    data["base_sha"] = "0" * 40
    assert cycle.execute(data, "codex", []) == 1
    folder = next(root.iterdir())
    assert (folder / "repo").exists()
    receipt = json.loads((folder / "receipt.json").read_text())
    assert receipt["status"] == "retained"


def test_reviewer_self_review_fails_closed(controller, monkeypatch):
    data, state, root, remote = controller
    state.update(login="tticom-codex", review_published=True)
    data.update(role="codex", mode="reviewer", allowed_paths=[], pull_request=1)
    orig_boundary = subprocess.run
    def self_review_run(args, **kwargs):
        args = [str(a) for a in args]
        if args[0] == "gh" and args[1:3] == ["api", "user"]:
            return subprocess.CompletedProcess(args, 0, "tticom-codex", "")
        if args[0] == "gh" and any("pulls/1" in a for a in args):
            pr = {
                "head": {"sha": data["base_sha"], "ref": "feat/example", "repo": {"full_name": "tticom/score2gp"}},
                "user": {"login": "tticom-codex"},
                "state": "open",
            }
            return subprocess.CompletedProcess(args, 0, json.dumps(pr), "")
        return orig_boundary(args, **kwargs)
    monkeypatch.setattr(subprocess, "run", self_review_run)
    assert cycle.execute(data, "codex", []) == 1
    folder = next(root.iterdir())
    receipt = json.loads((folder / "receipt.json").read_text())
    assert receipt["status"] == "retained"
    assert "self-review is forbidden" in receipt.get("reason", "")


def test_concurrent_distinct_task_cycles_remain_isolated(controller):
    data1, state, root, remote = controller
    data2 = deepcopy(data1)
    data2["task"] = "TASK-B"
    data2["branch"] = "feat/task-b"
    git(remote, "branch", "feat/task-b", data1["base_sha"])

    assert cycle.execute(data1, "codex", []) == 0
    assert cycle.execute(data2, "codex", []) == 0

    folders = list(root.iterdir())
    assert len(folders) == 2
    receipts = [json.loads((f / "receipt.json").read_text()) for f in folders]
    tasks = {r["assignment"]["task"] for r in receipts}
    assert tasks == {"example", "TASK-B"}
    leases = {r["cycle_id"] for r in receipts}
    assert len(leases) == 2

