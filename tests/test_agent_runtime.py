import os
from pathlib import Path
import subprocess

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
