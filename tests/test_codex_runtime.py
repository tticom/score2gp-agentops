import os
import subprocess
from pathlib import Path

import pytest

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
        SCORE2GP_CYCLE_ASSIGNMENT=str(tmp_path / "assignment.json"),
    )
    result = subprocess.run([str(STARTUP_SCRIPT)], env=env, capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stderr
    assert role_file.read_text() == "codex"


def test_start_instance_never_bootstraps_or_changes_existing_checkouts(tmp_path):
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
        SCORE2GP_CYCLE_ASSIGNMENT=str(tmp_path / "assignment.json"),
    )
    result = subprocess.run([str(STARTUP_SCRIPT)], env=env, capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stderr
    assert order_file.read_text().splitlines() == ["launcher"]


def test_start_instance_is_idle_without_assignment(tmp_path):
    env = {k: v for k, v in os.environ.items() if k not in {
        "SCORE2GP_CYCLE_ASSIGNMENT", "SCORE2GP_INSTANCE_STARTUP_DONE"}}
    env.update(WSL_DISTRO_NAME="Ubuntu-Gov", SCORE2GP_RUNTIME_ENV_FILE=str(tmp_path / "absent"))
    result = subprocess.run([str(STARTUP_SCRIPT)], env=env, capture_output=True, text=True)
    assert result.returncode == 0
    assert "idle" in result.stdout


@pytest.mark.parametrize("missing", ["launcher", "image"])
def test_assigned_startup_fails_when_prerequisites_are_missing(tmp_path, missing):
    scripts = tmp_path / "workspace/score2gp-agentops/agent-runtime/scripts"
    scripts.mkdir(parents=True)
    sentinel = tmp_path / "launched"
    if missing != "launcher":
        launcher = scripts / "run-agy.sh"
        launcher.write_text(f"#!/bin/sh\ntouch '{sentinel}'\n")
        launcher.chmod(0o755)
    binaries = tmp_path / "bin"
    binaries.mkdir()
    docker = binaries / "docker"
    docker.write_text("#!/bin/sh\nexit 1\n")
    docker.chmod(0o755)
    env = {k: v for k, v in os.environ.items() if k != "SCORE2GP_INSTANCE_STARTUP_DONE"}
    env.update(PATH=f"{binaries}:{env['PATH']}", WSL_DISTRO_NAME="Ubuntu-Automation",
               SCORE2GP_WORKSPACE_ROOT=str(tmp_path / "workspace"),
               SCORE2GP_RUNTIME_ENV_FILE=str(tmp_path / "absent"),
               SCORE2GP_CYCLE_ASSIGNMENT=str(tmp_path / "assignment.json"))
    result = subprocess.run([str(STARTUP_SCRIPT)], env=env, capture_output=True, text=True)
    assert result.returncode == 69
    assert ("not installed" if missing == "launcher" else "not built") in result.stderr
    assert not sentinel.exists()
