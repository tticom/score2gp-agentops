import os
import subprocess
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "agent-runtime/scripts/run-codex.sh"
STARTUP_SCRIPT = Path(__file__).parents[1] / "agent-runtime/scripts/start-instance.sh"


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
