import importlib.util
from pathlib import Path
import pytest
from types import SimpleNamespace

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

def test_convert_governance_promotion_is_writable():
    result = adapter.convert(governed("governance", 459), AUTHORITY, "gov", ["github.com"])
    assert result["mode"] == "author"
    assert result["allowed_paths"] == ["src/a.py"]

@pytest.mark.parametrize("assignment", [{}, {"work": {}, "worker": {}},
    {"authority": {"task_id": "UNKNOWN"}, "worker": {"role": "implementation"}, "work": {}}])
def test_convert_rejects_incomplete_assignment(assignment):
    with pytest.raises(adapter.AdapterError):
        adapter.convert(assignment, AUTHORITY, "automation", ["github.com"])

def test_hosts_are_explicit():
    with pytest.raises(adapter.AdapterError):
        adapter.parse_hosts("")
    assert adapter.parse_hosts("api.github.com github.com") == ["api.github.com", "github.com"]


def test_role_dispatch_environment_fetches_secret_without_gh_login(monkeypatch):
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        return type("Result", (), {"returncode": 0, "stdout": "role-token\n", "stderr": ""})()

    monkeypatch.setattr(adapter.subprocess, "run", run)
    monkeypatch.setenv("SCORE2GP_GCP_PROJECT_ID", "score2gp-test")
    monkeypatch.setenv("SCORE2GP_GITHUB_SECRET_NAME", "score2gp-github-automation-token")
    env = adapter.role_dispatch_environment("automation")
    assert env["GH_TOKEN"] == "role-token"
    assert calls == [[
        "gcloud", "secrets", "versions", "access", "latest",
        "--secret=score2gp-github-automation-token", "--project=score2gp-test",
    ]]


def test_convert_creates_missing_task_branch_from_product_main(monkeypatch, tmp_path):
    commands = []

    def run(command, **kwargs):
        commands.append(command)
        if command[:2] == ["git", "ls-remote"]:
            return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        if command[:3] == ["git", "-C", str(tmp_path)]:
            if command[3:] == ["status", "--porcelain"]:
                return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            if command[3:] == ["fetch", "origin", "main"]:
                return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            if command[3:] == ["rev-parse", "origin/main"]:
                return type("Result", (), {"returncode": 0, "stdout": "a" * 40, "stderr": ""})()
            if command[3:] == ["branch", "--show-current"]:
                return type("Result", (), {"returncode": 0, "stdout": "main", "stderr": ""})()
            if command[3:] == ["rev-parse", "HEAD"]:
                return type("Result", (), {"returncode": 0, "stdout": "a" * 40, "stderr": ""})()
        if command[:3] == ["gh", "api", "repos/tticom/score2gp/git/refs"]:
            return type("Result", (), {"returncode": 0, "stdout": "{}", "stderr": ""})()
        raise AssertionError(command)

    monkeypatch.setattr(adapter.subprocess, "run", run)
    heads = iter([None, None, "a" * 40, "a" * 40])
    monkeypatch.setattr(adapter, "remote_branch_head", lambda repository, branch: next(heads))
    assignment = governed()
    assignment["work"]["expected_head_sha"] = None
    result = adapter.convert(
        assignment, AUTHORITY, "automation", ["github.com"], product=tmp_path, env={}
    )
    assert result["base_sha"] == "a" * 40
    assert any(command[:3] == ["gh", "api", "repos/tticom/score2gp/git/refs"] for command in commands)


def test_convert_creates_missing_branch_from_task_repository_main(monkeypatch, tmp_path):
    commands = []
    product_base = "a" * 40
    task_repository_base = "b" * 40

    def run(command, **kwargs):
        commands.append(command)
        if command[:2] == ["git", "ls-remote"]:
            return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        if command[:3] == ["git", "-C", str(tmp_path)]:
            if command[3:] == ["status", "--porcelain"]:
                return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            if command[3:] == ["fetch", "origin", "main"]:
                return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            if command[3:] == ["rev-parse", "origin/main"]:
                return type("Result", (), {"returncode": 0, "stdout": product_base, "stderr": ""})()
            if command[3:] == ["branch", "--show-current"]:
                return type("Result", (), {"returncode": 0, "stdout": "main", "stderr": ""})()
            if command[3:] == ["rev-parse", "HEAD"]:
                return type("Result", (), {"returncode": 0, "stdout": product_base, "stderr": ""})()
        if command[:3] == ["gh", "api", "repos/tticom/score2gp-agentops/git/refs"]:
            assert f"sha={task_repository_base}" in command
            return type("Result", (), {"returncode": 0, "stdout": "{}", "stderr": ""})()
        raise AssertionError(command)

    monkeypatch.setattr(adapter.subprocess, "run", run)
    heads = iter([None, None, task_repository_base, task_repository_base])
    monkeypatch.setattr(adapter, "remote_branch_head", lambda repository, branch: next(heads))
    assignment = governed()
    assignment["work"]["repository"] = "tticom/score2gp-agentops"
    assignment["work"]["expected_head_sha"] = None

    result = adapter.convert(
        assignment,
        AUTHORITY,
        "automation",
        ["github.com"],
        product=tmp_path,
        env={},
    )

    assert result["base_sha"] == task_repository_base


def test_command_json_preserves_dispatch_diagnostic(monkeypatch, tmp_path):
    def run(*args, **kwargs):
        return SimpleNamespace(returncode=1, stdout="", stderr="gh: not logged in")

    monkeypatch.setattr(adapter.subprocess, "run", run)
    with pytest.raises(adapter.AdapterError, match="gh: not logged in"):
        adapter.command_json(["dispatch"], tmp_path, {})
