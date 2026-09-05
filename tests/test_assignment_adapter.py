import importlib.util
from pathlib import Path
import pytest

spec = importlib.util.spec_from_file_location("assignment_adapter", Path(__file__).parents[1] / "agent-runtime/assignment_adapter.py")
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)

AUTHORITY = {"task": {"id": "REC-04", "prompt": "task prompt", "allowed_paths": ["src/a.py"],
                       "validation_commands": ["python -m pytest tests/test_a.py"]}}

def governed(worker_role="implementation", pull_request=None):
    return {"authority": {"task_id": "REC-04"}, "worker": {"role": worker_role},
            "work": {"repository": "tticom/score2gp", "branch": "feat/rec-04-local-scale-model",
                     "expected_head_sha": "a" * 40, "pull_request": pull_request,
                     "allowed_paths": ["src/a.py"], "prompt": "worker prompt"}}

def test_convert_author_assignment():
    result = adapter.convert(governed(pull_request=459), AUTHORITY, "automation", ["api.github.com"])
    assert result["mode"] == "author"
    assert result["repository"] == "https://github.com/tticom/score2gp.git"
    assert result["validation"] == [["python", "-m", "pytest", "tests/test_a.py"]]

def test_convert_reviewer_is_read_only():
    result = adapter.convert(governed("reviewer", 459), AUTHORITY, "gov", ["github.com"])
    assert result["mode"] == "reviewer"
    assert result["allowed_paths"] == []

@pytest.mark.parametrize("assignment", [{}, {"work": {}, "worker": {}},
    {"authority": {"task_id": "UNKNOWN"}, "worker": {"role": "implementation"}, "work": {}}])
def test_convert_rejects_incomplete_assignment(assignment):
    with pytest.raises(adapter.AdapterError):
        adapter.convert(assignment, AUTHORITY, "automation", ["github.com"])

def test_hosts_are_explicit():
    with pytest.raises(adapter.AdapterError):
        adapter.parse_hosts("")
    assert adapter.parse_hosts("api.github.com github.com") == ["api.github.com", "github.com"]
