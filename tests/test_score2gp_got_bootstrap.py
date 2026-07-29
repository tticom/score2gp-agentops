import json
import subprocess

import pytest

from scripts.score2gp_got_bootstrap import query_pr, resolve_got_state


def test_merged_pr_overrides_historical_review_state() -> None:
    result = resolve_got_state(
        {"state": "MERGED", "headRefOid": "e" * 40, "number": 393},
        [{"state": "CHANGES_REQUESTED", "commit_id": "c" * 40}],
    )
    assert result["state"] == "MERGED_AWAITING_GOVERNANCE_PROMOTION"
    assert result["current_review"] is None


def test_open_pr_uses_latest_exact_head_review() -> None:
    head = "a" * 40
    reviews = [
        {"id": 1, "state": "APPROVED", "commit_id": head,
         "submitted_at": "2026-07-28T18:00:00Z", "user": {"login": "tticom-codex"}},
        {"id": 2, "state": "CHANGES_REQUESTED", "commit_id": head,
         "submitted_at": "2026-07-28T19:00:00Z", "user": {"login": "tticom-codex"}},
    ]
    result = resolve_got_state(
        {"state": "OPEN", "headRefOid": head, "number": 393}, reviews
    )
    assert result["state"] == "AWAITING_AGY_FIXES"
    assert result["current_review"]["id"] == 2


def test_no_pr_waits_for_implementation_without_dispatch_failure() -> None:
    result = resolve_got_state(None, [])
    assert result == {
        "state": "AWAITING_AGY_IMPLEMENTATION",
        "current_review": None,
    }


def test_query_pr_uses_empty_successful_list_for_no_pr(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        assert args[:3] == ["gh", "pr", "list"]
        assert "--head" in args
        return subprocess.CompletedProcess(args, 0, json.dumps([]), "")

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert query_pr("tticom/score2gp", "agy/new-task") is None
