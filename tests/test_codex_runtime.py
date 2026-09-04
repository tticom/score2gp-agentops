import os
import subprocess
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "agent-runtime/scripts/run-codex.sh"


def test_run_codex_uses_role_scoped_home_and_secret_mount(tmp_path):
    source_dir = tmp_path / "product"
    source_dir.mkdir()
    (source_dir / "pyproject.toml").write_text("[project]\nname = 'test-product'\n")
    (source_dir / ".git").mkdir()
    task_worktree = tmp_path / "task-worktree"
    skills_dir = tmp_path / "agy-skills"
    skills_dir.mkdir()

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    args_file = tmp_path / "docker-args"
    (bin_dir / "docker").write_text(
        "#!/usr/bin/env bash\n"
        f"printf '%s\\n' \"$@\" > {args_file}\n"
    )
    (bin_dir / "docker").chmod(0o755)
    (bin_dir / "git").write_text(
        "#!/usr/bin/env bash\n"
        "if [[ $1 == -C && $3 == worktree && $4 == add ]]; then\n"
        f"  mkdir -p {task_worktree}; printf '%s\\n' '[project]' > {task_worktree}/pyproject.toml; mkdir -p {task_worktree}/.git\n"
        "fi\n"
    )
    (bin_dir / "git").chmod(0o755)
    (bin_dir / "gcloud").write_text("#!/usr/bin/env bash\nprintf '%s' token\n")
    (bin_dir / "gcloud").chmod(0o755)

    env = os.environ.copy()
    env.update(
        PATH=f"{bin_dir}:{env['PATH']}",
        SCORE2GP_PRODUCT_DIR=str(source_dir),
        AGY_SKILLS_DIR=str(skills_dir),
        SCORE2GP_TASK_WORKTREE=str(task_worktree),
        SCORE2GP_TASK="codex-test",
        SCORE2GP_GCP_PROJECT_ID="test-project",
        SCORE2GP_GITHUB_SECRET_NAME="test-secret",
        SCORE2GP_AGENT_ROLE="automation",
    )
    result = subprocess.run(
        [str(SCRIPT), "--version"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    args = args_file.read_text().splitlines()
    mount_values = [value for index, value in enumerate(args) if args[index - 1] == "--mount"]
    assert "type=bind,src=" + str(task_worktree) + ",dst=/workspace/score2gp,readonly=false" in mount_values
    assert "type=bind,src=" + str(skills_dir) + ",dst=/workspace/agy-skills,readonly" in mount_values
    assert any(value.endswith(",dst=/run/secrets/github-token,readonly") for value in mount_values)
    assert "type=volume,src=score2gp-automation-codex-home,dst=/home/agent/.codex" in mount_values
    assert args[args.index("--entrypoint") + 1] == "/usr/local/bin/entrypoint.sh"
    assert args[-5:] == ["codex", "--dangerously-bypass-approvals-and-sandbox", "--add-dir", "/workspace/agy-skills", "--version"]
