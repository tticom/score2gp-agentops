"""CP-16: the branch cannot supply its own open-PR recording authority.

The historical CP-13 metadata pair is 5dddf7e (branch: TBD) and
8c9d7dc (main after #714: 713). GitHub replies here are protocol test data,
not evidence of a live GitHub audit.
"""
import json
import subprocess
from pathlib import Path

import pytest

from scripts import score2gp_governance_audit as audit


BRANCH = "feat/cp-13-codex-author-lane"
MAIN_RECORD = "git", "show", "origin/main:projects/score2gp/ACTIVE_TASK.md"


def record(number="TBD", branch=BRANCH, repository="tticom/score2gp-agentops"):
    return (
        "**Status**: PROMOTED\n"
        f"**Repository**: {repository}\n"
        f"**PR Branch**: `{branch}`\n"
        + (f"**Pull Request**: {number}\n" if number is not None else "")
    )


def run_audit(monkeypatch, tmp_path, branch_record, main_record, *, git_error=False,
              state="OPEN"):
    """Drive all of main(); only external Git/GitHub replies are substituted."""
    monkeypatch.chdir(tmp_path)
    for name in (
        "projects/score2gp/skills/architect/SKILL.md",
        "projects/score2gp/skills/developer/SKILL.md",
        "skills/score2gp-developer.md", "skills/score2gp-pr-hard-review.md",
        "skills/score2gp-task-orchestration.md", "AGENT-RULES.md",
        "projects/score2gp/AGENT_CONTROL.md",
    ):
        path = Path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("agent_verify.py artifact_audit.py pr_body.py", encoding="utf-8")
    Path("projects/score2gp/ACTIVE_TASK.md").write_text(branch_record, encoding="utf-8")
    monkeypatch.delenv("SCORE2GP_GOVERNANCE_AUDIT_OFFLINE", raising=False)
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        assert kwargs["encoding"] == "utf-8" and kwargs["errors"] == "strict"
        if command == ["git", "ls-files"]:
            stdout = "AGENT-RULES.md"
        elif tuple(command) == MAIN_RECORD:
            if git_error:
                raise subprocess.CalledProcessError(128, command, stderr="missing main record")
            stdout = main_record
        elif command[:3] == ["gh", "pr", "list"]:
            repository = audit.parse_active_task_state(branch_record)[1]
            assert command[command.index("--repo") + 1] == repository
            assert command[command.index("--head") + 1] == BRANCH
            stdout = json.dumps([{"number": 713, "state": state}])
        else:
            pytest.fail(f"Unexpected command: {command}")
        return subprocess.CompletedProcess(command, 0, stdout, "")

    monkeypatch.setattr(audit.subprocess, "run", run)
    with pytest.raises(SystemExit) as raised:
        audit.main()
    return raised.value.code, calls


def test_number_on_main_with_tbd_on_branch_passes(monkeypatch, tmp_path, capsys):
    # Rejects the named mutant: read the branch copy.
    code, calls = run_audit(monkeypatch, tmp_path, record(), record("713"))
    assert code == 0
    assert "GOVERNANCE AUDIT PASS" in capsys.readouterr().out
    assert list(MAIN_RECORD) in calls


@pytest.mark.parametrize("main_number", [None, "TBD", "714"])
def test_branch_cannot_record_itself(monkeypatch, tmp_path, capsys, main_number):
    # Rejects both named mutants: read the branch copy; skip the comparison.
    code, _ = run_audit(monkeypatch, tmp_path, record("713"), record(main_number))
    assert code == 1
    assert "OPEN PR #713" in capsys.readouterr().out


@pytest.mark.parametrize("main_record", [
    "", record("713", branch="feat/other-task"),
    record("713", repository="tticom/score2gp"),
])
def test_main_record_must_identify_the_same_task_branch(monkeypatch, tmp_path, main_record):
    # Empty record rejects branch fallback; other cases reject trusting a matching
    # PR number without binding repository and branch (see mutation receipts).
    code, _ = run_audit(monkeypatch, tmp_path, record("713"), main_record)
    assert code == 1


def test_unreadable_main_record_fails_closed(monkeypatch, tmp_path):
    # Rejects falling back to the branch when origin/main cannot be read.
    code, _ = run_audit(monkeypatch, tmp_path, record("713"), "", git_error=True)
    assert code == 1


@pytest.mark.parametrize("state, expected", [("CLOSED", 0), ("MERGED", 1)])
def test_non_open_pr_keeps_existing_checks(monkeypatch, tmp_path, capsys, state, expected):
    # Rejects moving the main lookup ahead of OPEN filtering (and skipping replay).
    code, calls = run_audit(monkeypatch, tmp_path, record(), "", git_error=True, state=state)
    assert code == expected
    assert list(MAIN_RECORD) not in calls
    assert ("already MERGED" in capsys.readouterr().out) == (state == "MERGED")


@pytest.mark.parametrize("branch_number, main_number, expected", [
    ("713", "TBD", 0), ("TBD", "713", 1),
])
def test_product_pr_binding_is_unchanged(monkeypatch, tmp_path, branch_number,
                                         main_number, expected):
    # Rejects broadening CP-16 to change product PR authority as well.
    code, calls = run_audit(
        monkeypatch, tmp_path,
        record(branch_number, repository="tticom/score2gp"),
        record(main_number, repository="tticom/score2gp"),
    )
    assert code == expected
    assert list(MAIN_RECORD) not in calls
