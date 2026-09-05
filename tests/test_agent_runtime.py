import os
import json
from pathlib import Path
import runpy
import subprocess
import sys

import pytest


RUNTIME = Path(__file__).parents[1] / "agent-runtime"


@pytest.mark.parametrize("engine", ["agy", "codex"])
def test_live_launcher_requires_explicit_assignment(engine):
    env = {k: v for k, v in os.environ.items() if k != "SCORE2GP_CYCLE_ASSIGNMENT"}
    result = subprocess.run([str(RUNTIME / "scripts" / f"run-{engine}.sh")],
                            env=env, capture_output=True, text=True)
    assert result.returncode == 2
    assert "approved cycle assignment" in result.stderr


@pytest.mark.parametrize("engine", ["agy", "codex"])
def test_live_launcher_passes_engine_and_assignment_to_controller(tmp_path, engine):
    assignment = tmp_path / "assignment.json"
    assignment.write_text('{}')
    result = subprocess.run([str(RUNTIME / "scripts" / f"run-{engine}.sh"),
                             "--assignment", str(assignment)], capture_output=True, text=True)
    assert result.returncode == 64
    assert "assignment is missing required fields" in result.stderr


@pytest.fixture
def worker_entrypoint(monkeypatch):
    """Execute worker.py itself; replace only container files and client process boundary."""
    state = {"mode": "author", "calls": [], "exit_code": 0, "plugin_failure": None}
    original_read = Path.read_text

    def read(path, *args, **kwargs):
        if path == Path("/assignment.json"):
            return json.dumps({"prompt": "Perform the bounded test task.",
                               "branch": "feat/assigned", "mode": state["mode"]})
        if path == Path("/run/secrets/github-token"):
            return "test-token\n"
        return original_read(path, *args, **kwargs)

    def client(argv):
        state["calls"].append(argv)
        assert os.environ["GH_TOKEN"] == "test-token"
        assert os.environ["GIT_TERMINAL_PROMPT"] == "0"
        assert "GIT_ASKPASS" not in os.environ
        is_plugin = argv[:3] == ["agy", "plugin", "install"]
        status = (31 if argv[-1].endswith(str(state["plugin_failure"])) else 0) if is_plugin else state["exit_code"]
        return subprocess.CompletedProcess(argv, status)

    monkeypatch.setattr(Path, "read_text", read)
    monkeypatch.setattr(subprocess, "run", client)
    monkeypatch.setenv("SCORE2GP_CYCLE_ID", "test-cycle")
    monkeypatch.setenv("GH_TOKEN", "initial-test-token")
    monkeypatch.setenv("GIT_TERMINAL_PROMPT", "initial")
    monkeypatch.delenv("GIT_ASKPASS", raising=False)

    def execute(engine, *extra):
        monkeypatch.setattr(sys, "argv", ["worker.py", engine, *extra])
        with pytest.raises(SystemExit) as result:
            runpy.run_path(str(RUNTIME / "worker.py"), run_name="__main__")
        return result.value.code

    return execute, state


@pytest.mark.parametrize("engine", ["agy", "codex"])
@pytest.mark.parametrize("mode", ["author", "reviewer"])
@pytest.mark.parametrize("exit_code", [0, 23])
def test_worker_executes_bounded_client_and_propagates_status(worker_entrypoint, engine, mode, exit_code):
    execute, state = worker_entrypoint
    state.update(mode=mode, exit_code=exit_code)
    assert execute(engine, "--model", "test-model") == exit_code
    if engine == "agy":
        assert state["calls"][:-1] == [
            ["agy", "plugin", "install", f"/workspace/agy-skills/plugins/{plugin}"]
            for plugin in ("engineering", "productivity")]
        assert state["calls"][-1][:-1] == ["agy", "--dangerously-skip-permissions",
                                               "--model", "test-model", "--print"]
    else:
        assert len(state["calls"]) == 1
        assert state["calls"][0][:-1] == ["codex", "exec", "--ephemeral",
            "--dangerously-bypass-approvals-and-sandbox", "--add-dir", "/workspace/agy-skills",
            "--model", "test-model"]
    prompt = state["calls"][-1][-1]
    assert prompt.startswith("Perform the bounded test task.")
    assert "Cycle test-cycle: remain on feat/assigned." in prompt
    assert "Do not push or switch branches." in prompt
    assert "do not select another task" in prompt
    assert ("Source is read-only" in prompt) == (mode == "reviewer")
    assert ("<!-- score2gp-cycle:test-cycle -->" in prompt) == (mode == "reviewer")


@pytest.mark.parametrize("plugin", ["engineering", "productivity"])
def test_worker_stops_before_agent_invocation_on_plugin_failure(worker_entrypoint, plugin):
    execute, state = worker_entrypoint
    state["plugin_failure"] = plugin
    assert execute("agy") == 31
    assert len(state["calls"]) == (1 if plugin == "engineering" else 2)
    assert all(argv[:3] == ["agy", "plugin", "install"] for argv in state["calls"])
