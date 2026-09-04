import os
import subprocess
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "agent-runtime/scripts/run-codex.sh"
STARTUP_SCRIPT = Path(__file__).parents[1] / "agent-runtime/scripts/start-instance.sh"


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
        SCORE2GP_AGENT_ROLE="codex",
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
    assert "type=bind,src=" + str(source_dir / ".git") + ",dst=" + str(source_dir / ".git") + ",readonly=false" in mount_values
    assert "type=bind,src=" + str(skills_dir) + ",dst=/workspace/agy-skills,readonly" in mount_values
    assert any(value.endswith(",dst=/run/secrets/github-token,readonly") for value in mount_values)
    assert "type=volume,src=score2gp-codex-codex-home,dst=/home/agent/.codex" in mount_values
    assert "type=volume,src=score2gp-codex-agent-local,dst=/home/agent/.local" in mount_values
    assert "GIT_AUTHOR_NAME=tticom-codex" in args
    assert "GIT_AUTHOR_EMAIL=tticomcodex@gmail.com" in args
    assert "SCORE2GP_TASK=codex-test" in args
    assert "SCORE2GP_AGENT_ROLE=codex" in args
    assert args[args.index("--entrypoint") + 1] == "/usr/local/bin/entrypoint.sh"
    assert args[-5:] == ["codex", "--dangerously-bypass-approvals-and-sandbox", "--add-dir", "/workspace/agy-skills", "--version"]


def test_start_instance_routes_codex_to_codex_role(tmp_path):
    workspace = tmp_path / "workspace"
    agentops = workspace / "score2gp-agentops"
    launcher = agentops / "agent-runtime/scripts/run-codex.sh"
    launcher.parent.mkdir(parents=True)
    role_file = tmp_path / "role"
    launcher.write_text(f"#!/usr/bin/env bash\nprintf '%s' \"$SCORE2GP_AGENT_ROLE\" > {role_file}\n")
    launcher.chmod(0o755)
    (tmp_path / "home/.config/score2gp").mkdir(parents=True)
    (tmp_path / "home/.config/score2gp/codex-enabled").touch()

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "docker").write_text("#!/usr/bin/env bash\nexit 0\n")
    (bin_dir / "docker").chmod(0o755)

    env = os.environ.copy()
    env.update(
        PATH=f"{bin_dir}:{env['PATH']}",
        HOME=str(tmp_path / "home"),
        SCORE2GP_WORKSPACE_ROOT=str(workspace),
        WSL_DISTRO_NAME="Ubuntu-Codex",
    )
    result = subprocess.run([str(STARTUP_SCRIPT)], env=env, capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stderr
    assert role_file.read_text() == "codex"


def test_start_instance_bootstraps_before_launching(tmp_path):
    workspace = tmp_path / "workspace"
    agentops = workspace / "score2gp-agentops"
    scripts_dir = agentops / "agent-runtime/scripts"
    scripts_dir.mkdir(parents=True)
    order_file = tmp_path / "order"
    bootstrap = scripts_dir / "bootstrap-instance.sh"
    bootstrap.write_text(f"#!/usr/bin/env bash\nprintf '%s\\n' bootstrap >> {order_file}\n")
    bootstrap.chmod(0o755)
    launcher = scripts_dir / "run-agy.sh"
    launcher.write_text(f"#!/usr/bin/env bash\nprintf '%s\\n' launcher >> {order_file}\n")
    launcher.chmod(0o755)

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "docker").write_text("#!/usr/bin/env bash\nexit 0\n")
    (bin_dir / "docker").chmod(0o755)

    env = os.environ.copy()
    env.update(
        PATH=f"{bin_dir}:{env['PATH']}",
        SCORE2GP_WORKSPACE_ROOT=str(workspace),
        WSL_DISTRO_NAME="Ubuntu-Automation",
    )
    result = subprocess.run([str(STARTUP_SCRIPT)], env=env, capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stderr
    assert order_file.read_text().splitlines() == ["bootstrap", "launcher"]
