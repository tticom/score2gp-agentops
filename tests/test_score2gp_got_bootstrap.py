from pathlib import Path

import pytest

from scripts.score2gp_got_bootstrap import GotError, resolve_got_state, validate_governance_identity


def test_merged_pr_overrides_historical_review_state() -> None:
    result = resolve_got_state(
        {"state": "MERGED", "headRefOid": "e" * 40, "number": 393},
        [{"state": "CHANGES_REQUESTED", "commit_id": "c" * 40}],
    )
    assert result["state"] == "PROMOTE_MERGED_TASK"
    assert result["current_review"] is None


def test_merged_pr_emits_promote_resolved_task_when_status_resolved() -> None:
    result = resolve_got_state(
        {"state": "MERGED", "headRefOid": "e" * 40, "number": 421},
        [],
        active_task_status="RESOLVED",
    )
    assert result["state"] == "PROMOTE_RESOLVED_TASK"
    assert result["current_review"] is None


def test_merged_pr_emits_promote_merged_task_when_status_not_resolved() -> None:
    result = resolve_got_state(
        {"state": "MERGED", "headRefOid": "e" * 40, "number": 396},
        [],
        active_task_status="APPROVED",
    )
    assert result["state"] == "PROMOTE_MERGED_TASK"
    assert result["current_review"] is None


def test_no_pr_waits_for_author_publication() -> None:
    result = resolve_got_state(None, [])
    assert result == {
        "state": "AWAITING_AGY_PUBLICATION",
        "current_review": None,
    }


def test_open_pr_uses_latest_exact_head_review() -> None:
    head = "a" * 40
    reviews = [
        {"id": 1, "state": "APPROVED", "commit_id": head,
         "submitted_at": "2026-07-28T18:00:00Z", "user": {"login": "tticomgov-code"}},
        {"id": 2, "state": "CHANGES_REQUESTED", "commit_id": head,
         "submitted_at": "2026-07-28T19:00:00Z", "user": {"login": "tticomgov-code"}},
    ]
    result = resolve_got_state(
        {"state": "OPEN", "headRefOid": head, "number": 393}, reviews
    )
    assert result["state"] == "AWAITING_AGY_FIXES"
    assert result["current_review"]["id"] == 2


def test_open_pr_accepts_newer_codex_change_request() -> None:
    head = "a" * 40
    result = resolve_got_state(
        {"state": "OPEN", "headRefOid": head, "number": 396},
        [
            {"id": 1, "state": "APPROVED", "commit_id": head,
             "submitted_at": "2026-07-30T15:59:00Z", "user": {"login": "tticomgov-code"}},
            {"id": 2, "state": "CHANGES_REQUESTED", "commit_id": head,
             "submitted_at": "2026-07-30T16:48:00Z", "user": {"login": "tticom-codex"}},
        ],
    )
    assert result["state"] == "AWAITING_AGY_FIXES"
    assert result["current_review"]["id"] == 2


def test_open_pr_accepts_owner_verdict() -> None:
    head = "b" * 40
    result = resolve_got_state(
        {"state": "OPEN", "headRefOid": head, "number": 396},
        [{"id": 3, "state": "APPROVED", "commit_id": head,
          "submitted_at": "2026-07-30T17:00:00Z", "user": {"login": "tticom"}}],
    )
    assert result["state"] == "READY_FOR_HUMAN_MERGE"


def test_governance_worker_uses_codex_publishing_identity() -> None:
    validate_governance_identity(
        linux_user="tticom-gov",
        home="/home/tticom-gov",
        gh_user="tticomgov-code",
        git_user="tticomgov-code",
        agentops=Path("/home/tticom-gov/work/score2gp-workspace/score2gp-agentops"),
        product=Path("/home/tticom-gov/work/score2gp-workspace/score2gp"),
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("linux_user", "tticom"),
        ("gh_user", "tticom"),
        ("git_user", "tticom"),
    ],
)
def test_governance_identity_rejects_personal_account(field: str, value: str) -> None:
    values = {
        "linux_user": "tticom-gov",
        "home": "/home/tticom-gov",
        "gh_user": "tticomgov-code",
        "git_user": "tticomgov-code",
        "agentops": Path("/home/tticom-gov/work/score2gp-workspace/score2gp-agentops"),
        "product": Path("/home/tticom-gov/work/score2gp-workspace/score2gp"),
    }
    values[field] = value
    with pytest.raises(GotError):
        validate_governance_identity(**values)
