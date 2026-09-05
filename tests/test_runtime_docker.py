"""Opt-in real image smoke; build both :task-checkpoints images first."""
import os
import subprocess

import pytest


@pytest.mark.skipif(os.environ.get("SCORE2GP_DOCKER_TESTS") != "1",
                    reason="requires built task-checkpoints Docker images")
@pytest.mark.parametrize("image", ["score2gp-agent:task-checkpoints",
                                  "score2gp-codex:task-checkpoints"])
def test_entrypoint_preserves_stdin_and_worker_status(tmp_path, image):
    repo = tmp_path / "task"
    repo.mkdir(mode=0o777)
    repo.chmod(0o777)
    subprocess.run(["git", "init", "-b", "test/smoke", str(repo)], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=smoke",
                    "-c", "user.email=smoke@example.invalid", "commit",
                    "--allow-empty", "-m", "smoke"], check=True, capture_output=True)
    command = ["docker", "run", "--rm", "-i", "--network", "none",
               "--user", "10001:10001", "--read-only", "--cap-drop", "ALL",
               "--security-opt", "no-new-privileges:true", "--tmpfs", "/tmp:rw,noexec,nosuid",
               "--mount", f"type=bind,src={repo},dst=/workspace/task",
               "-e", "SCORE2GP_REPOSITORY_DIR=/workspace/task",
               "-e", "SCORE2GP_TASK=smoke", "-e", "SCORE2GP_TASK_BRANCH=test/smoke",
               "-e", "SCORE2GP_SESSION_MODE=validation", "-e", "GIT_AUTHOR_NAME=smoke",
               "-e", "GIT_AUTHOR_EMAIL=smoke@example.invalid", image,
               "python", "-c",
               "import sys; assert sys.stdin.readline().strip() == 'input-survives'; sys.exit(23)"]
    result = subprocess.run(command, input="input-survives\n", text=True,
                            capture_output=True, timeout=60)
    assert result.returncode == 23, result.stdout + result.stderr
    assert not subprocess.check_output(["git", "-C", str(repo), "status", "--porcelain"])
