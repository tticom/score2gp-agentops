from scripts.score2gp_pr_review_state import TRUSTED_REVIEWERS, resolve_current_head_review

HEAD = "a" * 40


def review(review_id: int, state: str, *, head: str = HEAD, user: str = "tticomgov-code"):
    return {
        "id": review_id,
        "state": state,
        "commit_id": head,
        "submitted_at": f"2026-07-28T18:{review_id:02d}:00Z",
        "user": {"login": user},
    }


def test_later_changes_requested_supersedes_earlier_approval() -> None:
    selected = resolve_current_head_review(
        [review(1, "APPROVED"), review(2, "CHANGES_REQUESTED")],
        HEAD,
        "tticomgov-code",
    )
    assert selected and selected["id"] == 2


def test_later_approval_supersedes_earlier_changes_requested() -> None:
    selected = resolve_current_head_review(
        [review(1, "CHANGES_REQUESTED"), review(2, "APPROVED")],
        HEAD,
        "tticomgov-code",
    )
    assert selected and selected["state"] == "APPROVED"


def test_ignores_prior_head_dismissed_and_other_reviewer() -> None:
    selected = resolve_current_head_review(
        [
            review(4, "CHANGES_REQUESTED", head="b" * 40),
            review(5, "CHANGES_REQUESTED", user="someone-else"),
            review(6, "DISMISSED"),
        ],
        HEAD,
        "tticomgov-code",
    )
    assert selected is None


def test_latest_exact_head_verdict_across_all_trusted_reviewers_governs() -> None:
    selected = resolve_current_head_review(
        [
            review(1, "APPROVED", user="tticomgov-code"),
            review(2, "CHANGES_REQUESTED", user="tticom-codex"),
            review(3, "APPROVED", user="tticom"),
        ],
        HEAD,
        TRUSTED_REVIEWERS,
    )
    assert selected and selected["id"] == 3


def test_codex_change_request_supersedes_older_governance_approval() -> None:
    selected = resolve_current_head_review(
        [
            review(1, "APPROVED", user="tticomgov-code"),
            review(2, "CHANGES_REQUESTED", user="tticom-codex"),
        ],
        HEAD,
    )
    assert selected and selected["state"] == "CHANGES_REQUESTED"


def test_untrusted_reviewer_cannot_supersede_owner() -> None:
    selected = resolve_current_head_review(
        [
            review(1, "APPROVED", user="tticom"),
            review(2, "CHANGES_REQUESTED", user="someone-else"),
        ],
        HEAD,
    )
    assert selected and selected["id"] == 1
