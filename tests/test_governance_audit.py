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


def test_current_active_task_metadata_parses_pr_branch() -> None:
    status, repository, branch = score2gp_governance_audit.parse_active_task_state(
        """# Active Task

**Task**: CR-04B: Explicit Tempo Override
**Status**: APPROVED
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr04b-explicit-pdf-only-tempo-override`
"""
    )

    assert status == "APPROVED"
    assert repository == "tticom/score2gp"
    assert branch == "agy/cr04b-explicit-pdf-only-tempo-override"


def test_architecture_task_uses_declared_agentops_repository() -> None:
    status, repository, branch = score2gp_governance_audit.parse_active_task_state(
        """# Active Task
**Status**: APPROVED
**Repository**: tticom/score2gp-agentops
**PR Branch**: `agy/cr04c-final-event-duration-consistency-architecture`
"""
    )

    assert status == "APPROVED"
    assert repository == "tticom/score2gp-agentops"
    assert branch == "agy/cr04c-final-event-duration-consistency-architecture"


@pytest.fixture(autouse=True)
def isolate_receipt_audit(request, monkeypatch):
    """GOV-02: main()-level tests must not depend on whether live authority enables step 6.

    The delegated-merge receipt audit is disabled by default. A test that exercises the real
    audit requests the ``real_receipt_audit`` fixture to opt out.
    """
    if "real_receipt_audit" in request.fixturenames:
        return
    monkeypatch.setattr(score2gp_governance_audit, "audit_delegated_merges", lambda authority, gh_json=None: [])


@pytest.fixture
def real_receipt_audit():
    """Opt out of ``isolate_receipt_audit`` to exercise the real receipt audit."""


class RecordedSubprocessRunner:
    def __init__(self, stdout="[]", returncode=0, stderr=""):
        self.stdout = stdout
        self.returncode = returncode
        self.stderr = stderr
        self.calls = []

    def __call__(self, args, **kwargs):
        if args and args[0] == "gh":
            self.calls.append(list(args))
            return subprocess.CompletedProcess(
                args=args,
                returncode=self.returncode,
                stdout=self.stdout,
                stderr=self.stderr,
            )
        return subprocess.run(args, **kwargs)

    def assert_called_with_gh_pr_list(self, repo: str, head: str) -> None:
        assert len(self.calls) == 1, f"Expected 1 gh call, got {len(self.calls)}"
        cmd = self.calls[0]
        assert cmd[0:3] == ["gh", "pr", "list"], f"Command does not start with gh pr list: {cmd}"
        assert "--repo" in cmd and cmd[cmd.index("--repo") + 1] == repo
        assert "--head" in cmd and cmd[cmd.index("--head") + 1] == head
        assert "--state" in cmd and cmd[cmd.index("--state") + 1] == "all"
        assert "--json" in cmd and cmd[cmd.index("--json") + 1] == "number,state"


def test_current_metadata_merged_branch_fails_audit(monkeypatch, capsys) -> None:
    mock_files = [
        "projects/score2gp/skills/architect/SKILL.md",
        "projects/score2gp/skills/developer/SKILL.md",
        "projects/score2gp/skills/reviewer/SKILL.md",
        "skills/score2gp-developer.md",
        "skills/score2gp-pr-hard-review.md",
        "skills/score2gp-task-orchestration.md",
    ]
    monkeypatch.setattr(
        score2gp_governance_audit, "run_cmd", lambda args: "\n".join(mock_files)
    )
    monkeypatch.setattr(os.path, "exists", lambda path: True)

    original_open = open

    def mock_open(path, *args, **kwargs):
        from unittest.mock import mock_open as m_open

        if "ACTIVE_TASK.md" in str(path):
            return m_open(
                read_data="""# Active Task
**Status**: APPROVED
**PR Branch**: `agy/already-merged`
**Repository**: tticom/score2gp
"""
            )()
        if "AGENT-RULES.md" in str(path) or "AGENT_CONTROL.md" in str(path):
            return m_open(read_data="agent_verify.py artifact_audit.py pr_body.py")()
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)

    runner = RecordedSubprocessRunner(
        stdout=json.dumps([{"number": 123, "state": "MERGED"}])
    )
    monkeypatch.setattr(subprocess, "run", runner)

    with pytest.raises(SystemExit) as raised:
        score2gp_governance_audit.main()

    assert raised.value.code == 1
    runner.assert_called_with_gh_pr_list(repo="tticom/score2gp", head="agy/already-merged")
    captured = capsys.readouterr()
    assert "agy/already-merged" in captured.out
    assert "MERGED" in captured.out
    assert "tticom/score2gp" in captured.out
    assert "ACTIVE_TASK.md status is stale" in captured.out


def test_newly_promoted_approved_task_without_pr_passes_audit(monkeypatch) -> None:
    mock_files = [
        "projects/score2gp/skills/architect/SKILL.md",
        "projects/score2gp/skills/developer/SKILL.md",
        "projects/score2gp/skills/reviewer/SKILL.md",
        "skills/score2gp-developer.md",
        "skills/score2gp-pr-hard-review.md",
        "skills/score2gp-task-orchestration.md",
    ]
    monkeypatch.setattr(
        score2gp_governance_audit, "run_cmd", lambda args: "\n".join(mock_files)
    )
    monkeypatch.setattr(os.path, "exists", lambda path: True)

    original_open = open

    def mock_open(path, *args, **kwargs):
        from unittest.mock import mock_open as m_open

        if "ACTIVE_TASK.md" in str(path):
            return m_open(
                read_data="""# Active Task
**Status**: APPROVED
**PR Branch**: `agy/cr05-structural-layout-and-titles-architecture`
**Repository**: tticom/score2gp
"""
            )()
        if "AGENT-RULES.md" in str(path) or "AGENT_CONTROL.md" in str(path):
            return m_open(read_data="agent_verify.py artifact_audit.py pr_body.py")()
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)

    runner = RecordedSubprocessRunner(stdout="[]")
    monkeypatch.setattr(subprocess, "run", runner)

    with pytest.raises(SystemExit) as raised:
        score2gp_governance_audit.main()

    assert raised.value.code == 0
    runner.assert_called_with_gh_pr_list(
        repo="tticom/score2gp",
        head="agy/cr05-structural-layout-and-titles-architecture",
    )


def test_unsupported_active_task_status_fails_without_github_lookup(
    monkeypatch, capsys
) -> None:
    mock_files = [
        "projects/score2gp/skills/architect/SKILL.md",
        "projects/score2gp/skills/developer/SKILL.md",
        "projects/score2gp/skills/reviewer/SKILL.md",
        "skills/score2gp-developer.md",
        "skills/score2gp-pr-hard-review.md",
        "skills/score2gp-task-orchestration.md",
    ]
    monkeypatch.setattr(
        score2gp_governance_audit, "run_cmd", lambda args: "\n".join(mock_files)
    )
    monkeypatch.setattr(os.path, "exists", lambda path: True)

    original_open = open

    def mock_open(path, *args, **kwargs):
        from unittest.mock import mock_open as m_open

        if "ACTIVE_TASK.md" in str(path):
            return m_open(
                read_data="""# Active Task
**Status**: ACTIVE
**PR Branch**: `agy/conversion-recovery-architecture`
**Repository**: tticom/score2gp
"""
            )()
        if "AGENT-RULES.md" in str(path) or "AGENT_CONTROL.md" in str(path):
            return m_open(read_data="agent_verify.py artifact_audit.py pr_body.py")()
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)
    runner = RecordedSubprocessRunner(stdout="[]")
    monkeypatch.setattr(subprocess, "run", runner)

    with pytest.raises(SystemExit) as raised:
        score2gp_governance_audit.main()

    assert raised.value.code == 1
    assert runner.calls == []
    assert "unsupported status 'ACTIVE'" in capsys.readouterr().out

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

def test_failed_github_lookup_fails_audit(monkeypatch, capsys) -> None:
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

    runner = RecordedSubprocessRunner(returncode=1, stderr="Failed command")
    monkeypatch.setattr(subprocess, "run", runner)

    # Expect system exit with code 1 due to failed github lookup
    with pytest.raises(SystemExit) as raised:
        score2gp_governance_audit.main()
    assert raised.value.code == 1
    runner.assert_called_with_gh_pr_list(repo="tticom/score2gp", head="feature/test-branch")
    captured = capsys.readouterr()
    assert "Unable to verify active task branch against GitHub" in captured.out

def test_malformed_github_json_fails_audit(monkeypatch, capsys) -> None:
    mock_files = [
        "projects/score2gp/skills/architect/SKILL.md",
        "skills/score2gp-developer.md",
        "skills/score2gp-pr-hard-review.md",
        "skills/score2gp-task-orchestration.md"
    ]
    monkeypatch.setattr(score2gp_governance_audit, "run_cmd", lambda args: "\n".join(mock_files))

    def mock_exists(path):
        return True
    monkeypatch.setattr(os.path, "exists", mock_exists)

    original_open = open
    def mock_open(path, *args, **kwargs):
        from unittest.mock import mock_open as m_open
        if "ACTIVE_TASK.md" in str(path):
            data = """# Active Task
**Status**: APPROVED
**PR Branch**: `agy/malformed-json-test`
**Repository**: tticom/score2gp
"""
            return m_open(read_data=data)()
        if "AGENT-RULES.md" in str(path) or "AGENT_CONTROL.md" in str(path):
            return m_open(read_data="agent_verify.py artifact_audit.py pr_body.py")()
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)

    runner = RecordedSubprocessRunner(stdout="invalid json{")
    monkeypatch.setattr(subprocess, "run", runner)

    with pytest.raises(SystemExit) as raised:
        score2gp_governance_audit.main()
    assert raised.value.code == 1
    runner.assert_called_with_gh_pr_list(repo="tticom/score2gp", head="agy/malformed-json-test")
    captured = capsys.readouterr()
    assert "Unable to verify active task branch against GitHub" in captured.out
    assert "JSON parse error" in captured.out

def test_open_matching_pr_passes_audit(monkeypatch, capsys) -> None:
    mock_files = [
        "projects/score2gp/skills/architect/SKILL.md",
        "skills/score2gp-developer.md",
        "skills/score2gp-pr-hard-review.md",
        "skills/score2gp-task-orchestration.md"
    ]
    monkeypatch.setattr(score2gp_governance_audit, "run_cmd", lambda args: "\n".join(mock_files))

    def mock_exists(path):
        return True
    monkeypatch.setattr(os.path, "exists", mock_exists)

    original_open = open
    def mock_open(path, *args, **kwargs):
        from unittest.mock import mock_open as m_open
        if "ACTIVE_TASK.md" in str(path):
            data = """# Active Task
**Status**: APPROVED
**PR Branch**: `gov/promote-cr05-structural-layout-and-titles-architecture`
**Repository**: tticom/score2gp-agentops
"""
            return m_open(read_data=data)()
        if "AGENT-RULES.md" in str(path) or "AGENT_CONTROL.md" in str(path):
            return m_open(read_data="agent_verify.py artifact_audit.py pr_body.py")()
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)

    runner = RecordedSubprocessRunner(stdout=json.dumps([{"number": 425, "state": "OPEN"}]))
    monkeypatch.setattr(subprocess, "run", runner)

    with pytest.raises(SystemExit) as raised:
        score2gp_governance_audit.main()
    assert raised.value.code == 0
    runner.assert_called_with_gh_pr_list(repo="tticom/score2gp-agentops", head="gov/promote-cr05-structural-layout-and-titles-architecture")
    captured = capsys.readouterr()
    assert "GOVERNANCE AUDIT PASS" in captured.out


def test_audit_fails_if_gh_command_args_mutated() -> None:
    runner = RecordedSubprocessRunner()
    runner(["gh", "pr", "list", "--head", "my-branch"])
    with pytest.raises(AssertionError):
        runner.assert_called_with_gh_pr_list(repo="tticom/score2gp", head="my-branch")

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
    for slot in ("worktrees/auto", "worktrees/gov", "worktrees/codex"):
        assert f"<workspace-root>/{slot}/score2gp-agentops" in control
    assert "must never operate from the other identity's workspace" in control
    assert "python scripts/verify_identity.py" in control
    for forbidden in ("/home/tticom-", "/mnt/c", "uname -s", "WSL Execution Environment Gate"):
        assert forbidden not in control

    automation_skill = (
        PROJECT_ROOT / ".agents/skills/score2gp-project-director/SKILL.md"
    ).read_text(encoding="utf-8")
    assert "git config --global --get user.name" in automation_skill
    assert "git config --global --get user.email" in automation_skill
    assert "git config --local --get user." not in automation_skill


RETIRED_PATHS = ("agent-runtime", "legacy", "scripts/agy-cycle")


def _tracked_files() -> list[str]:
    output = subprocess.run(
        ["git", "ls-files", "-z"], cwd=PROJECT_ROOT, capture_output=True, check=True
    ).stdout.decode("utf-8")
    return [path for path in output.split("\0") if path]


def _non_python_tooling(tracked: list[str]) -> list[str]:
    return sorted(
        path
        for path in tracked
        if path.endswith((".sh", ".ps1"))
        or any(path == retired or path.startswith(retired + "/") for retired in RETIRED_PATHS)
    )


def test_repository_tooling_is_python_only() -> None:
    # Tracked files only: untracked local leftovers (e.g. an old agent-runtime/
    # directory in a long-lived worktree) are not repository content.
    assert _non_python_tooling(_tracked_files()) == []


def test_python_only_check_flags_tracked_shell_and_retired_paths() -> None:
    tracked = [
        "scripts/tool.py",
        "scripts/run.sh",
        "tools/setup.ps1",
        "agent-runtime/cycle.py",
        "legacy",
        "scripts/agy-cycle",
        "scripts/agy_cycle.py",
        "docs/agent-runtime-notes.md",
    ]
    assert _non_python_tooling(tracked) == [
        "agent-runtime/cycle.py",
        "legacy",
        "scripts/agy-cycle",
        "scripts/run.sh",
        "tools/setup.ps1",
    ]


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
    rules = (PROJECT_ROOT / "projects/score2gp/REVIEW_RULES.md").read_text(
        encoding="utf-8"
    )
    template = (
        PROJECT_ROOT / "projects/score2gp/PR_REVIEW_TEMPLATE.md"
    ).read_text(encoding="utf-8")
    dispatch = (
        PROJECT_ROOT / "projects/score2gp/prompts/next/got-dispatch.md"
    ).read_text(encoding="utf-8")

    for text in (rules, template, dispatch):
        assert "reviewer-created counterexample" in text.lower()
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
        assert field in template
    for text in (rules, dispatch):
        assert "claim-to-oracle" in text.lower()
    assert "sensitive path" in rules.lower()


def test_developer_handback_requires_claim_assertion_defect_sweep() -> None:
    developer = (
        PROJECT_ROOT / "projects/score2gp/skills/developer/SKILL.md"
    ).read_text(encoding="utf-8")
    dispatch = (
        PROJECT_ROOT / "projects/score2gp/prompts/next/go-dispatch.md"
    ).read_text(encoding="utf-8")

    assert "Pre-handback defect sweep" in developer
    assert "actual assertions line by line" in developer
    assert "same value in that same output" in developer
    assert "pre-handback defect sweep" in dispatch
    assert "challenge one nearby" in dispatch
    assert "false-success case" in dispatch


def test_audit_fails_if_run_record_combines_reviewer_identities(tmp_path, monkeypatch) -> None:
    bad_run_record = tmp_path / "projects/score2gp/runs/bad_run.md"
    bad_run_record.parent.mkdir(parents=True, exist_ok=True)
    bad_run_record.write_text("Reviewed by tticom-codex / tticomgov-code", encoding="utf-8")

    monkeypatch.setattr(score2gp_governance_audit, "run_cmd", lambda args: "")

    def mock_exists(path):
        if "ACTIVE_TASK.md" in str(path):
            return False
        return True

    monkeypatch.setattr(os.path, "exists", mock_exists)

    def mock_walk(top):
        if "runs" in str(top):
            yield (str(bad_run_record.parent), [], ["bad_run.md"])

    monkeypatch.setattr(os, "walk", mock_walk)

    original_open = open

    def mock_open(path, *args, **kwargs):
        if "bad_run.md" in str(path):
            return original_open(bad_run_record, *args, **kwargs)
        if "AGENT-RULES.md" in str(path) or "AGENT_CONTROL.md" in str(path):
            from unittest.mock import mock_open as m_open
            return m_open(read_data="agent_verify.py artifact_audit.py pr_body.py")()
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)

    with pytest.raises(SystemExit) as raised:
        score2gp_governance_audit.main()
    assert raised.value.code == 1


def test_audit_fails_if_run_record_has_short_sha_or_non_distinct_reviewer(tmp_path, monkeypatch) -> None:
    bad_run = tmp_path / "projects/score2gp/runs/bad_sha_run.md"
    bad_run.parent.mkdir(parents=True, exist_ok=True)
    bad_run.write_text(
        "**Governance Publisher**: `tticomgov-code`\n"
        "**Independent Reviewer**: `tticomgov-code`\n"
        "**Product Main SHA**: `5a84056`\n",
        encoding="utf-8"
    )

    monkeypatch.setattr(score2gp_governance_audit, "run_cmd", lambda args: "")

    def mock_exists(path):
        if "ACTIVE_TASK.md" in str(path):
            return False
        return True

    monkeypatch.setattr(os.path, "exists", mock_exists)

    def mock_walk(top):
        if "runs" in str(top):
            yield (str(bad_run.parent), [], ["bad_sha_run.md"])

    monkeypatch.setattr(os, "walk", mock_walk)

    original_open = open

    def mock_open(path, *args, **kwargs):
        if "bad_sha_run.md" in str(path):
            return original_open(bad_run, *args, **kwargs)
        if "AGENT-RULES.md" in str(path) or "AGENT_CONTROL.md" in str(path):
            from unittest.mock import mock_open as m_open
            return m_open(read_data="agent_verify.py artifact_audit.py pr_body.py")()
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)

    with pytest.raises(SystemExit) as raised:
        score2gp_governance_audit.main()
    assert raised.value.code == 1


def test_audit_fails_if_run_record_has_non_hex_sha(tmp_path, monkeypatch) -> None:
    bad_run = tmp_path / "projects/score2gp/runs/bad_non_hex_run.md"
    bad_run.parent.mkdir(parents=True, exist_ok=True)
    bad_run.write_text(
        "**Governance Publisher**: `tticomgov-code`\n"
        "**Independent Reviewer**: `tticom-codex`\n"
        "**Product Main SHA**: `not-a-sha`\n",
        encoding="utf-8"
    )

    monkeypatch.setattr(score2gp_governance_audit, "run_cmd", lambda args: "")

    def mock_exists(path):
        if "ACTIVE_TASK.md" in str(path):
            return False
        return True

    monkeypatch.setattr(os.path, "exists", mock_exists)

    def mock_walk(top):
        if "runs" in str(top):
            yield (str(bad_run.parent), [], ["bad_non_hex_run.md"])

    monkeypatch.setattr(os, "walk", mock_walk)

    original_open = open

    def mock_open(path, *args, **kwargs):
        if "bad_non_hex_run.md" in str(path):
            return original_open(bad_run, *args, **kwargs)
        if "AGENT-RULES.md" in str(path) or "AGENT_CONTROL.md" in str(path):
            from unittest.mock import mock_open as m_open
            return m_open(read_data="agent_verify.py artifact_audit.py pr_body.py")()
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)

    with pytest.raises(SystemExit) as raised:
        score2gp_governance_audit.main()
    assert raised.value.code == 1


def test_sha_metadata_accepts_canonical_and_reapproved_head_forms() -> None:
    first = "a" * 40
    second = "b" * 40
    assert score2gp_governance_audit.is_valid_sha_metadata(
        "Product Main SHA", f"`{first}`"
    )
    assert score2gp_governance_audit.is_valid_sha_metadata(
        "Product Head SHA",
        f"`{first}` (Re-approved head SHA: `{second}`)",
    )
    assert not score2gp_governance_audit.is_valid_sha_metadata(
        "Product Main SHA",
        f"`{first}` (Re-approved head SHA: `{second}`)",
    )
    assert not score2gp_governance_audit.is_valid_sha_metadata(
        "Product Head SHA", "deadbee"
    )


def test_review_id_accepts_rest_numeric_and_graphql_node_ids() -> None:
    assert score2gp_governance_audit.has_valid_review_id(
        "**Review Verdict**: APPROVED (Review ID `4889312509`)"
    )
    assert score2gp_governance_audit.has_valid_review_id(
        "**Review Verdict**: APPROVED (Review ID `PRR_kwDOShNpkc8AAAABI2oOKg`)"
    )
    assert not score2gp_governance_audit.has_valid_review_id(
        "**Review Verdict**: APPROVED (Review ID `looks-good`)"
    )


# --- GOV-01 detective control: delegated merges need a matching merge-executor receipt ---

def _merge_audit_authority(since="2026-09-25", controllers=("tticom-codex", "tticomgov-code")):
    return {
        "merge_policy": {"executor_audit_since": since},
        "roles": {"merge_controller": {"github_logins": list(controllers)}},
    }


def _fake_gh(merged_by="tticom-codex", receipt_head="a" * 40, receipt_merge="m" * 40, fail=False):
    from scripts.score2gp_orca_control import format_merge_receipt

    calls = []

    def gh_json(args):
        calls.append(args)
        if fail:
            raise RuntimeError("HTTP 401")
        if args[:2] == ["pr", "list"]:
            if args[3] != "tticom/score2gp":
                return []
            return [{"number": 7, "mergedBy": {"login": merged_by}, "headRefOid": "a" * 40,
                     "mergeCommit": {"oid": "m" * 40}}]
        body = format_merge_receipt({"head_sha": receipt_head, "merge_commit": receipt_merge, "merged_by": merged_by})
        return [{"user": {"login": merged_by}, "body": body}]

    return gh_json, calls


def test_merge_receipt_audit_is_inactive_without_a_cutoff_or_controllers(real_receipt_audit) -> None:
    gh_json, calls = _fake_gh()
    assert score2gp_governance_audit.audit_delegated_merges(_merge_audit_authority(since=""), gh_json) == []
    assert score2gp_governance_audit.audit_delegated_merges(_merge_audit_authority(controllers=()), gh_json) == []
    assert calls == []


def test_merge_receipt_audit_passes_a_matching_receipt_and_queries_both_repositories(real_receipt_audit) -> None:
    gh_json, calls = _fake_gh()
    assert score2gp_governance_audit.audit_delegated_merges(_merge_audit_authority(), gh_json) == []
    listed = [args[3] for args in calls if args[:2] == ["pr", "list"]]
    assert listed == ["tticom/score2gp", "tticom/score2gp-agentops"]
    assert all("merged:>=2026-09-25" in args for args in calls if args[:2] == ["pr", "list"])


def test_merge_receipt_audit_flags_a_delegated_merge_with_a_mismatched_receipt(real_receipt_audit) -> None:
    gh_json, _ = _fake_gh(receipt_head="c" * 40)
    violations = score2gp_governance_audit.audit_delegated_merges(_merge_audit_authority(), gh_json)
    assert violations == [
        "tticom/score2gp#7 merged by delegated login tticom-codex without a matching merge-executor receipt"
    ]


def test_merge_receipt_audit_fails_closed_when_github_is_unavailable(real_receipt_audit) -> None:
    gh_json, _ = _fake_gh(fail=True)
    violations = score2gp_governance_audit.audit_delegated_merges(_merge_audit_authority(), gh_json)
    assert len(violations) == 2
    assert all(v.startswith("Unable to audit merge receipts for ") and "HTTP 401" in v for v in violations)


# --- GOV-01 review 5307413925: exhaustive collection, merger identity, gh page shapes ---

def _many_merges_gh(count, unreceipted_position):
    from scripts.score2gp_orca_control import format_merge_receipt

    def gh_json(args):
        if args[:2] == ["pr", "list"]:
            if args[3] != "tticom/score2gp":
                return []
            return [{"number": n, "mergedBy": {"login": "tticom-codex"}, "headRefOid": "a" * 40,
                     "mergeCommit": {"oid": f"{n:040d}"}} for n in range(1, count + 1)]
        number = int(args[-1].rsplit("/", 2)[-2])
        if number == unreceipted_position:
            return []
        body = format_merge_receipt({"head_sha": "a" * 40, "merge_commit": f"{number:040d}", "merged_by": "tticom-codex"})
        return [{"user": {"login": "tticom-codex"}, "body": body}]

    return gh_json


def test_merge_receipt_audit_covers_merges_beyond_the_first_two_hundred(real_receipt_audit) -> None:
    violations = score2gp_governance_audit.audit_delegated_merges(_merge_audit_authority(), _many_merges_gh(250, 201))
    assert violations == [
        "tticom/score2gp#201 merged by delegated login tticom-codex without a matching merge-executor receipt"
    ]


def test_merge_receipt_audit_fails_closed_when_the_merged_list_may_be_truncated(real_receipt_audit) -> None:
    limit = score2gp_governance_audit.MERGE_AUDIT_PR_LIMIT
    violations = score2gp_governance_audit.audit_delegated_merges(_merge_audit_authority(), _many_merges_gh(limit, 0))
    assert len(violations) == 1
    assert "reached the query limit" in violations[0] and "tticom/score2gp" in violations[0]


def test_merge_receipt_audit_flags_a_merge_with_no_merger_identity(real_receipt_audit) -> None:
    def gh_json(args):
        if args[:2] == ["pr", "list"]:
            return [{"number": 9, "mergedBy": None, "headRefOid": "a" * 40, "mergeCommit": {"oid": "m" * 40}}] \
                if args[3] == "tticom/score2gp" else []
        return []

    assert score2gp_governance_audit.audit_delegated_merges(_merge_audit_authority(), gh_json) == [
        "tticom/score2gp#9 has no merger identity; cannot verify it against merge-executor receipts"
    ]


@pytest.mark.parametrize(
    ("stdout", "expected"),
    [
        ('[{"a": 1}]\n[{"a": 2}]\n', [{"a": 1}, {"a": 2}]),      # --paginate: one array per page
        ('[[{"a": 1}], [{"a": 2}]]', [{"a": 1}, {"a": 2}]),      # --paginate --slurp
        ('{"login": "x"}', {"login": "x"}),                      # single object
        ("", None),
    ],
    ids=["paginate-pages", "slurp", "object", "empty"],
)
def test_gh_json_stream_parses_real_cli_page_shapes(stdout, expected) -> None:
    assert score2gp_governance_audit.parse_gh_json_stream(stdout) == expected


def test_merge_receipt_audit_reads_receipts_from_multi_page_comment_output(monkeypatch, real_receipt_audit) -> None:
    # Drive the default gh adapter with CLI-shaped stdout: a receipt on the second comment page.
    from scripts.score2gp_orca_control import format_merge_receipt

    receipt = format_merge_receipt({"head_sha": "a" * 40, "merge_commit": "m" * 40, "merged_by": "tticom-codex"})
    pages = json.dumps([[{"user": {"login": "tticom-automation"}, "body": "handback"}],
                        [{"user": {"login": "tticom-codex"}, "body": receipt}]])
    merged = json.dumps([{"number": 7, "mergedBy": {"login": "tticom-codex"}, "headRefOid": "a" * 40,
                          "mergeCommit": {"oid": "m" * 40}}])
    seen = []

    def fake_run(command, capture_output, text):
        seen.append(command)
        if command[1:3] == ["pr", "list"]:
            stdout = merged if command[4] == "tticom/score2gp" else "[]"
        else:
            assert "--slurp" in command
            stdout = pages
        return subprocess.CompletedProcess(command, 0, stdout, "")

    monkeypatch.setattr(score2gp_governance_audit.subprocess, "run", fake_run)
    assert score2gp_governance_audit.audit_delegated_merges(_merge_audit_authority()) == []
    assert any(c[1] == "api" for c in seen)


# --- GOV-02: step 6 at the main() level, independent of live authority ---

def _run_main_with_other_steps_passing(monkeypatch, authority=None, gh_stdout=None):
    """Run main() with steps 1-5 passing and an OPEN active-task PR; return (exit code, gh calls)."""
    mock_files = [
        "projects/score2gp/skills/architect/SKILL.md",
        "skills/score2gp-developer.md",
        "skills/score2gp-pr-hard-review.md",
        "skills/score2gp-task-orchestration.md",
    ]
    monkeypatch.setattr(score2gp_governance_audit, "run_cmd", lambda args: "\n".join(mock_files))
    monkeypatch.setattr(os.path, "exists", lambda path: True)
    monkeypatch.delenv("SCORE2GP_GOVERNANCE_AUDIT_OFFLINE", raising=False)
    original_open = open

    def mock_open(path, *args, **kwargs):
        from unittest.mock import mock_open as m_open
        if "ACTIVE_TASK.md" in str(path):
            return m_open(read_data="""# Active Task
**Status**: APPROVED
**PR Branch**: `feat/gov-02-fixture`
**Repository**: tticom/score2gp-agentops
""")()
        if "AGENT-RULES.md" in str(path) or "AGENT_CONTROL.md" in str(path):
            return m_open(read_data="agent_verify.py artifact_audit.py pr_body.py")()
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)
    if authority is not None:
        monkeypatch.setattr(score2gp_governance_audit, "load_authority", lambda path: authority)
    runner = RecordedSubprocessRunner(stdout=gh_stdout or json.dumps([{"number": 425, "state": "OPEN"}]))
    monkeypatch.setattr(subprocess, "run", runner)
    with pytest.raises(SystemExit) as raised:
        score2gp_governance_audit.main()
    return raised.value.code, runner.calls


def test_main_fails_when_the_receipt_audit_reports_a_violation(monkeypatch, capsys) -> None:
    violation = "tticom/score2gp#7 merged by delegated login tticom-codex without a matching merge-executor receipt"
    monkeypatch.setattr(score2gp_governance_audit, "audit_delegated_merges", lambda authority, gh_json=None: [violation])
    code, _ = _run_main_with_other_steps_passing(monkeypatch)
    assert code == 1
    assert violation in capsys.readouterr().out


def test_main_skips_the_receipt_audit_when_no_cutoff_is_set(monkeypatch, real_receipt_audit) -> None:
    authority = _merge_audit_authority(since="")
    code, calls = _run_main_with_other_steps_passing(monkeypatch, authority=authority)
    assert code == 0
    assert [call[:3] for call in calls] == [["gh", "pr", "list"]]  # only step 4's active-task lookup
    assert "--head" in calls[0]


def test_main_runs_the_receipt_audit_when_the_cutoff_is_set(monkeypatch, capsys, real_receipt_audit) -> None:
    # With a cut-off and controllers, main() really queries merged PRs in both repositories.
    # The recorded gh stub returns a merged PR with no merger identity, which must fail closed.
    authority = _merge_audit_authority(since="2026-09-24T18:16:59Z")
    code, calls = _run_main_with_other_steps_passing(monkeypatch, authority=authority)
    assert code == 1
    merged_queries = [c for c in calls if "--state" in c and c[c.index("--state") + 1] == "merged"]
    assert [c[c.index("--repo") + 1] for c in merged_queries] == ["tticom/score2gp", "tticom/score2gp-agentops"]
    assert "has no merger identity" in capsys.readouterr().out


def test_suite_isolation_holds_when_live_authority_enables_the_receipt_audit(monkeypatch, capsys) -> None:
    # The GOV-02 defect: live authority with executor_audit_since and merge_controller set must not
    # change a main()-level test that is about another step. isolate_receipt_audit guarantees this.
    authority = _merge_audit_authority(since="2026-09-24T18:16:59Z")
    code, calls = _run_main_with_other_steps_passing(monkeypatch, authority=authority)
    assert code == 0
    assert len(calls) == 1
    assert "GOVERNANCE AUDIT PASS" in capsys.readouterr().out
