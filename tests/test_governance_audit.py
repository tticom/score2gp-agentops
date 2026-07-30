import sys
import os
import json
import subprocess
from pathlib import Path
import pytest

# Add scripts to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import score2gp_governance_audit

def test_case_insensitive_banned_extensions(monkeypatch) -> None:
    # Mock git ls-files output to include uppercase extensions
    mock_files = [
        "projects/score2gp/skills/architect/SKILL.md",
        "skills/score2gp-developer.md",
        "skills/score2gp-pr-hard-review.md",
        "skills/score2gp-task-orchestration.md",
        "test_file.PDF",
        "another_file.MusicXML"
    ]
    monkeypatch.setattr(score2gp_governance_audit, "run_cmd", lambda args: "\n".join(mock_files))

    # Mock exist checks to return True for policy files and required skills
    original_exists = os.path.exists
    def mock_exists(path):
        if "ACTIVE_TASK.md" in str(path):
            return False # avoid active task check here
        return True
    monkeypatch.setattr(os.path, "exists", mock_exists)

    # Mock open to return clean policy file content (no mentions errors)
    original_open = open
    def mock_open(path, *args, **kwargs):
        if "AGENT-RULES.md" in str(path) or "AGENT_CONTROL.md" in str(path):
            from unittest.mock import mock_open as m_open
            return m_open(read_data="agent_verify.py artifact_audit.py pr_body.py")()
        return original_open(path, *args, **kwargs)
    monkeypatch.setattr("builtins.open", mock_open)

    # Expect system exit with code 1 due to test_file.PDF and another_file.MusicXML
    with pytest.raises(SystemExit) as raised:
        score2gp_governance_audit.main()
    assert raised.value.code == 1

def test_failed_github_lookup_fails_audit(monkeypatch) -> None:
    # Mock files to be clean
    mock_files = [
        "projects/score2gp/skills/architect/SKILL.md",
        "skills/score2gp-developer.md",
        "skills/score2gp-pr-hard-review.md",
        "skills/score2gp-task-orchestration.md"
    ]
    monkeypatch.setattr(score2gp_governance_audit, "run_cmd", lambda args: "\n".join(mock_files))

    # Mock exist checks
    def mock_exists(path):
        if "ACTIVE_TASK.md" in str(path):
            return True
        return True
    monkeypatch.setattr(os.path, "exists", mock_exists)

    # Mock open to return active task with APPROVED status and branch suggestion
    # Also mock clean policy files
    def mock_open(path, *args, **kwargs):
        from unittest.mock import mock_open as m_open
        if "ACTIVE_TASK.md" in str(path):
            data = """
## Status
APPROVED

## Branch Suggestion
`feature/test-branch`
"""
            return m_open(read_data=data)()
        if "AGENT-RULES.md" in str(path) or "AGENT_CONTROL.md" in str(path):
            return m_open(read_data="agent_verify.py artifact_audit.py pr_body.py")()
        return original_open(path, *args, **kwargs)

    original_open = open
    monkeypatch.setattr("builtins.open", mock_open)

    # Mock subprocess.run to simulate gh command failure (returncode != 0)
    class MockCompletedProcess:
        def __init__(self, returncode, stdout, stderr):
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def mock_run(args, **kwargs):
        if "gh" in args:
            return MockCompletedProcess(1, "", "Failed command")
        return subprocess.run(args, **kwargs)

    monkeypatch.setattr(subprocess, "run", mock_run)

    # Expect system exit with code 1 due to failed github lookup
    with pytest.raises(SystemExit) as raised:
        score2gp_governance_audit.main()
    assert raised.value.code == 1

def test_non_active_task_no_github_lookup(monkeypatch) -> None:
    # Mock files to be clean
    mock_files = [
        "projects/score2gp/skills/architect/SKILL.md",
        "skills/score2gp-developer.md",
        "skills/score2gp-pr-hard-review.md",
        "skills/score2gp-task-orchestration.md"
    ]
    monkeypatch.setattr(score2gp_governance_audit, "run_cmd", lambda args: "\n".join(mock_files))

    # Mock exist checks
    def mock_exists(path):
        if "ACTIVE_TASK.md" in str(path):
            return True
        return True
    monkeypatch.setattr(os.path, "exists", mock_exists)

    # Mock open to return active task with non-active status like COMPLETED or NONE
    def mock_open(path, *args, **kwargs):
        from unittest.mock import mock_open as m_open
        if "ACTIVE_TASK.md" in str(path):
            data = """
## Status
COMPLETED

## Branch Suggestion
`feature/test-branch`
"""
            return m_open(read_data=data)()
        if "AGENT-RULES.md" in str(path) or "AGENT_CONTROL.md" in str(path):
            return m_open(read_data="agent_verify.py artifact_audit.py pr_body.py")()
        return original_open(path, *args, **kwargs)

    original_open = open
    monkeypatch.setattr("builtins.open", mock_open)

    # Mock subprocess.run to raise exception if gh is called (proves it's not called)
    def mock_run(args, **kwargs):
        if "gh" in args:
            raise Exception("gh command should not be called")
        return subprocess.run(args, **kwargs)

    monkeypatch.setattr(subprocess, "run", mock_run)

    # Expect system exit with code 0 (success) because COMPLETED task shouldn't trigger gh
    with pytest.raises(SystemExit) as raised:
        score2gp_governance_audit.main()
    assert raised.value.code == 0

def test_orchestration_direct_main_removed() -> None:
    orchestration_path = PROJECT_ROOT / "skills/score2gp-task-orchestration.md"
    content = orchestration_path.read_text(encoding="utf-8")
    assert "committed directly to main" not in content


def test_active_governance_uses_identity_isolated_workspaces() -> None:
    operational_files = [
        "projects/score2gp/AGENT_CONTROL.md",
        "projects/score2gp/skills/project-director/SKILL.md",
        ".agents/skills/score2gp-project-director/SKILL.md",
        "skills/score2gp-project-director.md",
        "projects/prompts/05-project-director.md",
        ".agents/agents/project-director/agent.json",
    ]

    for relative_path in operational_files:
        content = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
        assert "/home/tticom/work/score2gp-workspace" not in content

    control = (PROJECT_ROOT / "projects/score2gp/AGENT_CONTROL.md").read_text(
        encoding="utf-8"
    )
    assert "/home/tticom-automation/work/score2gp-workspace" in control
    assert "/home/tticom-gov/work/score2gp-workspace" in control
    assert "must never operate from the other identity's home" in control

    automation_skill = (
        PROJECT_ROOT / ".agents/skills/score2gp-project-director/SKILL.md"
    ).read_text(encoding="utf-8")
    assert "git config --global --get user.name" in automation_skill
    assert "git config --global --get user.email" in automation_skill
    assert "git config --local --get user." not in automation_skill


def test_operational_scripts_default_to_current_linux_home() -> None:
    for relative_path in [
        "scripts/status.sh",
        "scripts/capture-pytest.sh",
        "scripts/capture-developer-diff.sh",
    ]:
        content = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
        assert "${HOME}/work/score2gp-workspace" in content
        assert "/home/tticom/work/score2gp-workspace" not in content


def test_next_uses_permanent_role_dispatchers() -> None:
    content = (PROJECT_ROOT / "projects/score2gp/prompts/NEXT.md").read_text(
        encoding="utf-8"
    )
    assert "next/go-dispatch.md" in content
    assert "next/got-dispatch.md" in content
    assert "0017-post-cr04d-public-pdf-only-conversion-replay.md" not in content


def test_go_dispatch_cannot_repeat_merged_work() -> None:
    content = (
        PROJECT_ROOT / "projects/score2gp/prompts/next/go-dispatch.md"
    ).read_text(encoding="utf-8")
    assert "head is exactly" in content
    assert "Do not rerun" in content
    assert "READY_FOR_HUMAN_MERGE" in content
    assert "AWAITING_GOVERNANCE_REVIEW" in content
    assert "score2gp_go_bootstrap.py" in content


def test_got_dispatch_requires_pinned_handback() -> None:
    content = (
        PROJECT_ROOT / "projects/score2gp/prompts/next/got-dispatch.md"
    ).read_text(encoding="utf-8")
    assert "handback comment pins the current head" in content
    assert "AWAITING_AGY_HANDBACK" in content
    assert "AWAITING_AGY_FIXES" in content
    assert "Never merge" in content


def test_governance_approval_requires_executed_adversarial_evidence() -> None:
    reviewer = (
        PROJECT_ROOT / "projects/score2gp/skills/reviewer/SKILL.md"
    ).read_text(encoding="utf-8")
    rules = (PROJECT_ROOT / "projects/score2gp/REVIEW_RULES.md").read_text(
        encoding="utf-8"
    )
    template = (
        PROJECT_ROOT / "projects/score2gp/PR_REVIEW_TEMPLATE.md"
    ).read_text(encoding="utf-8")
    dispatch = (
        PROJECT_ROOT / "projects/score2gp/prompts/next/got-dispatch.md"
    ).read_text(encoding="utf-8")

    for text in (reviewer, rules, template, dispatch):
        assert "reviewer-created counterexample" in text.lower()
    assert "input permutation" in reviewer
    assert "second-order probe" in reviewer
    assert "green CI and author tests are not substitutes" in dispatch
    for field in [
        "Changed abstraction boundary",
        "Strongest false-success mode",
        "Reviewer-created counterexample",
        "Exact command or probe",
        "Observed output",
        "Metamorphic relation checked",
        "Residual risk",
    ]:
        assert field in reviewer
        assert field in template
