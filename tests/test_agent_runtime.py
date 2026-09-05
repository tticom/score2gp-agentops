import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

RUNTIME = Path(__file__).parents[1] / "agent-runtime"


def git(repo, *args, env=None):
    return subprocess.run(["git", "-C", str(repo), *args], env=env, check=True, capture_output=True, text=True).stdout.strip()


@pytest.fixture
def launch_env(tmp_path):
    env = os.environ.copy()
    config = tmp_path / "gitconfig"
    config.write_text('[user]\n name = Test Worker\n email = worker@example.invalid\n')
    env.update(GIT_CONFIG_GLOBAL=str(config), GIT_CONFIG_NOSYSTEM="1")
    source = tmp_path / "score2gp"
    source.mkdir()
    git(source, "init", "-b", "main", env=env)
    (source / ".gitignore").write_text("*.egg-info/\n")
    git(source, "add", ".gitignore", env=env)
    git(source, "commit", "-m", "base", env=env)
    remote = tmp_path / "remote.git"
    git(source, "init", "--bare", str(remote), env=env)
    git(source, "remote", "add", "origin", str(remote), env=env)
    git(source, "push", "origin", "main", env=env)
    git(remote, "symbolic-ref", "HEAD", "refs/heads/main", env=env)
    github_url = "https://github.com/tticom/score2gp.git"
    git(source, "remote", "set-url", "origin", github_url, env=env)

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    real_git = shutil.which("git")
    # Only transport is substituted. All Git branch/ref/clone operations are real.
    (bin_dir / "git").write_text(
        "#!/usr/bin/env python3\nimport os,sys\n"
        f"real={real_git!r}\n"
        f"mapping=['-c', 'url.{remote}.insteadOf={github_url}']\n"
        "args=sys.argv[1:]\n"
        "if 'get-url' in args: mapping=[]\n"
        "os.execv(real,[real,*mapping,*args])\n"
    )
    (bin_dir / "gcloud").write_text("#!/bin/sh\nprintf %s test-token\n")
    (bin_dir / "gh").write_text("#!/bin/sh\nprintf '%s\\n' \"$TEST_GITHUB_LOGIN\"\n")
    (bin_dir / "setfacl").write_text("#!/bin/sh\nexit 0\n")
    (bin_dir / "docker").write_text(
        "#!/usr/bin/env python3\nimport os,sys,json\nfrom pathlib import Path\n"
        "args=sys.argv[1:]\n"
        "with open(os.environ['TEST_DOCKER_LOG'],'a') as f: f.write(json.dumps(args)+'\\n')\n"
        "if '--name' in args:\n"
        " if os.environ.get('TEST_DIRTY') == '1':\n"
        "  Path(os.environ['SCORE2GP_TASK_WORKTREE'],'unfinished.txt').write_text('unsaved work')\n"
        " sys.exit(int(os.environ.get('TEST_WORKER_EXIT','0')))\n"
    )
    for file in bin_dir.iterdir():
        file.chmod(0o755)
    skills = tmp_path / "skills"
    for plugin in ["engineering", "productivity"]:
        folder = skills / "plugins" / plugin
        folder.mkdir(parents=True)
        (folder / "plugin.json").write_text("{}")
    env.update(
        PATH=f"{bin_dir}:{env['PATH']}",
        SCORE2GP_PRODUCT_DIR=str(source),
        SCORE2GP_TASK_WORKTREE=str(tmp_path / "worker"),
        SCORE2GP_TASK="example",
        SCORE2GP_TASK_BRANCH="feat/example",
        SCORE2GP_GCP_PROJECT_ID="test-project",
        SCORE2GP_AGENT_ROLE="automation",
        AGY_SKILLS_DIR=str(skills),
        TEST_GITHUB_LOGIN="tticom-automation",
        TEST_DOCKER_LOG=str(tmp_path / "docker.jsonl"),
    )
    for name in ["SCORE2GP_REPOSITORY_DIR", "SCORE2GP_SESSION_MODE", "AGY_CONFIG_VOLUME",
                 "AGY_STATE_VOLUME", "AGENT_LOCAL_VOLUME", "CODEX_HOME_VOLUME"]:
        env.pop(name, None)
    return env, remote


@pytest.mark.parametrize("client,role,login", [
    ("agy", "automation", "tticom-automation"),
    ("agy", "gov", "tticomgov-code"),
    ("codex", "codex", "tticom-codex"),
])
def test_live_launcher_has_durable_branch_and_isolated_mounts(launch_env, client, role, login):
    env, remote = launch_env
    env.update(SCORE2GP_AGENT_ROLE=role, TEST_GITHUB_LOGIN=login)
    result = subprocess.run([str(RUNTIME / "scripts" / f"run-{client}.sh"), "--help"],
                            env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    calls = [json.loads(line) for line in Path(env["TEST_DOCKER_LOG"]).read_text().splitlines()]
    args = next(call for call in calls if "--name" in call)
    mounts = [args[i+1] for i, value in enumerate(args) if value == "--mount"]
    worker = Path(env["SCORE2GP_TASK_WORKTREE"])
    assert f"type=bind,src={worker},dst=/workspace/score2gp" in mounts
    assert not any(str(Path(env["SCORE2GP_PRODUCT_DIR"]) / ".git") in value for value in mounts)
    assert (worker / ".git").is_dir()
    assert "--rm" not in args
    assert "--cap-drop" in args and "ALL" in args
    assert "no-new-privileges:true" in args
    assert f"GIT_AUTHOR_NAME={login}" in args
    assert "SCORE2GP_TASK_BRANCH=feat/example" in args
    assert git(remote, "rev-parse", "refs/heads/feat/example", env=env) == git(worker, "rev-parse", "HEAD", env=env)
    assert any(call[0] == "rm" for call in calls)
    secret_mount = next(value for value in mounts if "dst=/run/secrets/github-token" in value)
    secret_path = secret_mount.split("src=")[1].split(",")[0]
    assert not Path(secret_path).exists()


@pytest.mark.parametrize("dirty,worker_exit,expected", [(True, 0, 75), (False, 9, 9)])
def test_failed_session_is_not_disposed(launch_env, dirty, worker_exit, expected):
    env, _ = launch_env
    env.update(TEST_DIRTY=str(int(dirty)), TEST_WORKER_EXIT=str(worker_exit))
    result = subprocess.run([str(RUNTIME / "scripts/run-agy.sh")], env=env, capture_output=True, text=True)
    assert result.returncode == expected
    assert "RECOVERY_REQUIRED" in result.stderr
    calls = [json.loads(line) for line in Path(env["TEST_DOCKER_LOG"]).read_text().splitlines()]
    assert not any(call[0] == "rm" for call in calls)
    if dirty:
        assert (Path(env["SCORE2GP_TASK_WORKTREE"]) / "unfinished.txt").read_text() == "unsaved work"


def test_identity_mismatch_prevents_clone_and_docker(launch_env):
    env, _ = launch_env
    env["TEST_GITHUB_LOGIN"] = "wrong-account"
    result = subprocess.run([str(RUNTIME / "scripts/run-agy.sh")], env=env, capture_output=True, text=True)
    assert result.returncode == 77
    assert not Path(env["SCORE2GP_TASK_WORKTREE"]).exists()
    assert not Path(env["TEST_DOCKER_LOG"]).exists()


def test_missing_task_branch_prevents_launch(launch_env):
    env, _ = launch_env
    env.pop("SCORE2GP_TASK_BRANCH")
    result = subprocess.run([str(RUNTIME / "scripts/run-codex.sh")], env=env, capture_output=True, text=True)
    assert result.returncode != 0
    assert not Path(env["TEST_DOCKER_LOG"]).exists()
