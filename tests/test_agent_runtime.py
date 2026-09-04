import os
import subprocess
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "agent-runtime/scripts/run-agy.sh"


def test_run_agy_uses_valid_long_form_bind_mount(tmp_path):
    source_dir = tmp_path / "product"
    source_dir.mkdir()
    (source_dir / "pyproject.toml").write_text("[project]\nname = 'test-product'\n")
    (source_dir / ".git").mkdir()
    task_worktree = tmp_path / "task-worktree"
    skills_dir = tmp_path / "agy-skills"
    (skills_dir / "plugins/engineering").mkdir(parents=True)
    (skills_dir / "plugins/productivity").mkdir(parents=True)
    (skills_dir / "plugins/engineering/plugin.json").write_text("{}")
    (skills_dir / "plugins/productivity/plugin.json").write_text("{}")

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    args_file = tmp_path / "docker-args"
    (bin_dir / "docker").write_text(
        "#!/usr/bin/env bash\n"
        "if [[ $1 == volume ]]; then exit 0; fi\n"
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
    (bin_dir / "gcloud").write_text(
        "#!/usr/bin/env bash\n"
        "printf '%s' token\n"
    )
    (bin_dir / "gcloud").chmod(0o755)

    env = os.environ.copy()
    env.update(
        PATH=f"{bin_dir}:{env['PATH']}",
        SCORE2GP_PRODUCT_DIR=str(source_dir),
        AGY_SKILLS_DIR=str(skills_dir),
        SCORE2GP_TASK_WORKTREE=str(task_worktree),
        SCORE2GP_TASK="test-task",
        SCORE2GP_GCP_PROJECT_ID="test-project",
        SCORE2GP_GITHUB_SECRET_NAME="test-secret",
        AGY_CONFIG_VOLUME="test-config",
        AGY_STATE_VOLUME="test-state",
    )
    result = subprocess.run(
        [str(SCRIPT), "--help"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    args = args_file.read_text().splitlines()
    mount_values = [value for index, value in enumerate(args) if args[index - 1] == "--mount"]
    assert "type=bind,src=" + str(task_worktree) + ",dst=/workspace/score2gp,readonly=false" in mount_values
    assert "type=volume,src=test-config,dst=/home/agent/.config" in mount_values
    assert "type=volume,src=test-state,dst=/home/agent/.gemini" in mount_values
    assert "type=bind,src=" + str(skills_dir) + ",dst=/workspace/agy-skills,readonly" in mount_values
    assert any(value.endswith(",dst=/run/secrets/github-token,readonly") for value in mount_values)
    assert "GIT_AUTHOR_NAME=tticom-automation" in args
    assert "GIT_AUTHOR_EMAIL=tticomautomation@gmail.com" in args
    assert "GIT_COMMITTER_NAME=tticom-automation" in args
    assert "GIT_COMMITTER_EMAIL=tticomautomation@gmail.com" in args
    assert "SCORE2GP_TASK=test-task" in args
    assert args[args.index("--entrypoint") + 1] == "/usr/local/bin/entrypoint.sh"
    assert args[-2:] == ["--dangerously-skip-permissions", "--help"]


def test_run_agy_defaults_to_role_scoped_volumes(tmp_path):
    source_dir = tmp_path / "product"
    source_dir.mkdir()
    (source_dir / "pyproject.toml").write_text("[project]\nname = 'test-product'\n")
    (source_dir / ".git").mkdir()
    task_worktree = tmp_path / "task-worktree"
    skills_dir = tmp_path / "agy-skills"
    for plugin in ("engineering", "productivity"):
        (skills_dir / "plugins" / plugin).mkdir(parents=True)
        (skills_dir / "plugins" / plugin / "plugin.json").write_text("{}")

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    args_file = tmp_path / "docker-args"
    (bin_dir / "docker").write_text(
        "#!/usr/bin/env bash\n"
        "if [[ $1 == volume ]]; then exit 0; fi\n"
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
    (bin_dir / "gcloud").write_text(
        "#!/usr/bin/env bash\n"
        "printf '%s' token\n"
    )
    (bin_dir / "gcloud").chmod(0o755)

    env = os.environ.copy()
    env.update(
        PATH=f"{bin_dir}:{env['PATH']}",
        SCORE2GP_PRODUCT_DIR=str(source_dir),
        AGY_SKILLS_DIR=str(skills_dir),
        SCORE2GP_TASK_WORKTREE=str(task_worktree),
        SCORE2GP_TASK="test-task",
        SCORE2GP_GCP_PROJECT_ID="test-project",
        SCORE2GP_GITHUB_SECRET_NAME="test-secret",
        SCORE2GP_AGENT_ROLE="gov",
    )
    result = subprocess.run(
        [str(SCRIPT), "--help"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    args = args_file.read_text().splitlines()
    mount_values = [value for index, value in enumerate(args) if args[index - 1] == "--mount"]
    assert "type=volume,src=score2gp-gov-agy-config,dst=/home/agent/.config" in mount_values
    assert "type=volume,src=score2gp-gov-agy-state,dst=/home/agent/.gemini" in mount_values


def test_run_agy_rejects_unknown_agent_role(tmp_path):
    source_dir = tmp_path / "product"
    source_dir.mkdir()
    (source_dir / "pyproject.toml").write_text("[project]\nname = 'test-product'\n")
    (source_dir / ".git").mkdir()
    skills_dir = tmp_path / "agy-skills"
    for plugin in ("engineering", "productivity"):
        (skills_dir / "plugins" / plugin).mkdir(parents=True)
        (skills_dir / "plugins" / plugin / "plugin.json").write_text("{}")

    env = os.environ.copy()
    env.update(
        SCORE2GP_PRODUCT_DIR=str(source_dir),
        AGY_SKILLS_DIR=str(skills_dir),
        SCORE2GP_TASK="test-task",
        SCORE2GP_AGENT_ROLE="reviewer",
    )
    result = subprocess.run(
        [str(SCRIPT), "--help"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 64
    assert "SCORE2GP_AGENT_ROLE must be automation or gov" in result.stderr
