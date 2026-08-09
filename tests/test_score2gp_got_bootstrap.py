from pathlib import Path

import pytest

from scripts.score2gp_got_bootstrap import (
    GotError,
    resolve_got_state,
    find_current_head_handback,
    gate_review_on_handback,
    select_review_level,
    validate_governance_identity,
)


def test_merged_pr_overrides_historical_review_state() -> None:
    result = resolve_got_state(
        {"state": "MERGED", "headRefOid": "e" * 40, "number": 393},
        [{"state": "CHANGES_REQUESTED", "commit_id": "c" * 40}],
    )
    assert result["state"] == "PROMOTE_MERGED_TASK"
    assert result["current_review"] is None


def test_promoted_merged_task_is_terminal_for_got() -> None:
    result = resolve_got_state(
        {"state": "MERGED", "headRefOid": "e" * 40, "number": 398},
        [{"state": "CHANGES_REQUESTED", "commit_id": "c" * 40}],
        active_task_status="MERGED",
    )
    assert result == {"state": "NO_ACTIVE_TASK", "current_review": None}


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


def test_resolved_task_with_no_pr_emits_promote_resolved_task() -> None:
    result = resolve_got_state(None, [], active_task_status="RESOLVED")
    assert result == {
        "state": "PROMOTE_RESOLVED_TASK",
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


def test_codex_reviewer_uses_isolated_codex_identity() -> None:
    validate_governance_identity(
        linux_user="tticom-codex",
        home="/home/tticom-codex",
        gh_user="tticom-codex",
        git_user="tticom-codex",
        agentops=Path("/home/tticom-codex/work/score2gp-workspace/score2gp-agentops"),
        product=Path("/home/tticom-codex/work/score2gp-workspace/score2gp"),
    )


def test_codex_reviewer_rejects_cross_profile_identity() -> None:
    with pytest.raises(GotError):
        validate_governance_identity(
            linux_user="tticom-codex",
            home="/home/tticom-codex",
            gh_user="tticomgov-code",
            git_user="tticom-codex",
            agentops=Path("/home/tticom-codex/work/score2gp-workspace/score2gp-agentops"),
            product=Path("/home/tticom-codex/work/score2gp-workspace/score2gp"),
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


def test_personal_reviewer_uses_personal_identity() -> None:
    # Test with unauthenticated/empty gh_user
    validate_governance_identity(
        linux_user="tticom",
        home="/home/tticom",
        gh_user="",
        git_user="tticom",
        agentops=Path("/home/tticom/work/score2gp-workspace/score2gp-agentops"),
        product=Path("/home/tticom/work/score2gp-workspace/score2gp"),
    )
    # Test with authenticated gh_user
    validate_governance_identity(
        linux_user="tticom",
        home="/home/tticom",
        gh_user="tticom",
        git_user="tticom",
        agentops=Path("/home/tticom/work/score2gp-workspace/score2gp-agentops"),
        product=Path("/home/tticom/work/score2gp-workspace/score2gp"),
    )


def test_low_risk_documentation_pr_selects_basic_review() -> None:
    selected = select_review_level(
        repository="tticom/score2gp",
        changed_paths=["docs/user-guide.md"],
        task="Clarify CLI spelling",
        title="docs: clarify CLI spelling",
        live_head="a" * 40,
    )
    assert selected == {
        "level": "basic",
        "skill": "code-review",
        "reasons": ["low-risk documentation-only change"],
    }


def test_code_or_test_change_selects_hard_review() -> None:
    selected = select_review_level(
        repository="tticom/score2gp",
        changed_paths=["src/score2gp/config.py", "tests/test_config.py"],
        task="Configuration cleanup",
        title="refactor: simplify configuration loading",
        live_head="b" * 40,
    )
    assert selected["level"] == "hard"
    assert selected["skill"] == "hard-review"
    assert "code, test, fixture, or executable-script change" in selected["reasons"]


@pytest.mark.parametrize(
    ("repository", "paths", "task", "role", "reason"),
    [
        (
            "tticom/score2gp-agentops",
            ["projects/score2gp/ACTIVE_TASK.md"],
            "Promote task",
            "Governor",
            "governance/control-plane repository change",
        ),
        (
            "tticom/score2gp",
            ["docs/design/conversion-architecture.md"],
            "Conversion architecture",
            "Architect / Researcher",
            "architecture, research, or authority translation",
        ),
        (
            "tticom/score2gp",
            ["src/score2gp/timing.py"],
            "Repair MusicXML timing",
            "Developer",
            "high-risk conversion or evidence claim",
        ),
    ],
)
def test_high_risk_context_selects_devils_advocate_review(
    repository: str,
    paths: list[str],
    task: str,
    role: str,
    reason: str,
) -> None:
    selected = select_review_level(
        repository=repository,
        changed_paths=paths,
        task=task,
        authorised_role=role,
        live_head="c" * 40,
    )
    assert selected["level"] == "devils-advocate"
    assert selected["skill"] == "devils-advocate-review"
    assert reason in selected["reasons"]


def test_prior_trusted_review_on_earlier_head_forces_devils_advocate_rereview() -> None:
    selected = select_review_level(
        repository="tticom/score2gp",
        changed_paths=["docs/user-guide.md"],
        task="Clarify CLI spelling",
        live_head="d" * 40,
        reviews=[
            {
                "commit_id": "e" * 40,
                "state": "APPROVED",
                "user": {"login": "tticomgov-code"},
            }
        ],
    )
    assert selected["level"] == "devils-advocate"
    assert "re-review after a trusted review on an earlier head" in selected["reasons"]


def test_declared_review_level_can_escalate_but_not_weaken() -> None:
    escalated = select_review_level(
        repository="tticom/score2gp",
        changed_paths=["docs/user-guide.md"],
        declared_level="real review",
        live_head="f" * 40,
    )
    assert escalated["level"] == "devils-advocate"

    not_weakened = select_review_level(
        repository="tticom/score2gp",
        changed_paths=["src/score2gp/config.py"],
        declared_level="basic",
        live_head="f" * 40,
    )
    assert not_weakened["level"] == "hard"


def test_invalid_declared_review_level_fails_closed() -> None:
    with pytest.raises(GotError, match="unsupported Review Level"):
        select_review_level(
            repository="tticom/score2gp",
            changed_paths=["docs/user-guide.md"],
            declared_level="friendly glance",
        )


def test_exact_head_author_handback_is_required_for_review_dispatch() -> None:
    head = "a" * 40
    handback = {
        "id": 12,
        "body": f"Head: {head}\nAWAITING_GOVERNANCE_REVIEW",
        "user": {"login": "tticom-automation"},
    }
    found = find_current_head_handback(
        [handback], head=head, author="tticom-automation"
    )
    assert found == handback
    assert gate_review_on_handback(
        {"state": "REVIEW_CURRENT_HEAD", "current_review": None}, found
    ) == {"state": "REVIEW_CURRENT_HEAD", "current_review": None}


@pytest.mark.parametrize(
    "comment",
    [
        {
            "id": 1,
            "body": f"Head: {'b' * 40}\nAWAITING_GOVERNANCE_REVIEW",
            "user": {"login": "tticom-automation"},
        },
        {
            "id": 2,
            "body": f"Head: {'a' * 40}\nAWAITING_GOVERNANCE_REVIEW",
            "user": {"login": "tticom-gov"},
        },
        {
            "id": 3,
            "body": f"Head: {'a' * 40}\nTests passed",
            "user": {"login": "tticom-automation"},
        },
    ],
)
def test_stale_wrong_author_or_unmarked_comment_is_not_a_handback(
    comment: dict,
) -> None:
    assert find_current_head_handback(
        [comment], head="a" * 40, author="tticom-automation"
    ) is None


def test_missing_handback_emits_terminal_wait_state() -> None:
    assert gate_review_on_handback(
        {"state": "REVIEW_CURRENT_HEAD", "current_review": None}, None
    ) == {"state": "AWAITING_AGY_HANDBACK", "current_review": None}


def test_handback_gate_does_not_override_other_states() -> None:
    resolved = {
        "state": "AWAITING_AGY_FIXES",
        "current_review": {"id": 99},
    }
    assert gate_review_on_handback(resolved, None) is resolved
