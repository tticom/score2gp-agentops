import json
import subprocess

import pytest

from scripts.score2gp_publish_review import (
    ReviewPublishError,
    normalize_verdict,
    publish_review,
    validate_approval_evidence,
)


def result(payload, returncode=0, stderr=""):
    return subprocess.CompletedProcess(
        args=[], returncode=returncode, stdout=json.dumps(payload), stderr=stderr
    )


def test_normalize_needs_changes_to_formal_review_state() -> None:
    assert normalize_verdict("needs changes") == (
        "CHANGES_REQUESTED",
        "REQUEST_CHANGES",
        "AWAITING_AGY_FIXES",
    )
    assert normalize_verdict("CHANGES_REQUESTED")[0] == "CHANGES_REQUESTED"


def test_rejects_unknown_verdict() -> None:
    with pytest.raises(ReviewPublishError, match="unsupported verdict"):
        normalize_verdict("needs work maybe")


def approval_body() -> str:
    return """
- **Changed abstraction boundary**: Chord subgroup duration reconciliation across candidate evidence.
- **Strongest false-success mode**: Conflicting member durations silently become order dependent.
- **Reviewer-created counterexample**: One quarter and one eighth candidate in a two-string chord.
- **Exact command or probe**: python -c 'assemble_pdf_tab_bar([quarter, eighth])'
- **Observed output**: PdfTabBarAssemblerError with pdf_only_tab_ambiguous_duration.
- **Metamorphic relation checked**: Reversing candidate order preserves the same rejection.
- **Residual risk**: Real scanned morphology noise remains outside this bounded synthetic probe.
""".strip()


def test_approval_requires_substantive_adversarial_evidence() -> None:
    with pytest.raises(ReviewPublishError, match="Changed abstraction boundary"):
        validate_approval_evidence("CI passed and the patch looks good.")

    incomplete = approval_body().replace(
        "One quarter and one eighth candidate in a two-string chord.", "not run"
    )
    with pytest.raises(ReviewPublishError, match="Reviewer-created counterexample"):
        validate_approval_evidence(incomplete)


def test_complete_adversarial_evidence_is_accepted() -> None:
    validate_approval_evidence(approval_body())


def test_approved_publication_is_blocked_before_github_without_evidence() -> None:
    called = False

    def runner(command, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("GitHub must not be called")

    with pytest.raises(ReviewPublishError, match="adversarial evidence"):
        publish_review(
            repo="tticom/score2gp",
            pr_number=395,
            expected_head="a" * 40,
            verdict="APPROVED",
            body="All existing tests pass.",
            runner=runner,
        )
    assert called is False


def test_publishes_and_verifies_exact_head_changes_request() -> None:
    head = "a" * 40
    calls = []
    responses = iter(
        [
            result({"state": "OPEN", "headRefOid": head}),
            result({"id": 42}),
            result({"state": "OPEN", "headRefOid": head}),
            result(
                [
                    {
                        "id": 42,
                        "state": "CHANGES_REQUESTED",
                        "commit_id": head,
                        "submitted_at": "2026-07-30T09:00:00Z",
                        "user": {"login": "tticomgov-code"},
                    }
                ]
            ),
        ]
    )

    def runner(command, **kwargs):
        calls.append(command)
        return next(responses)

    published = publish_review(
        repo="tticom/score2gp",
        pr_number=394,
        expected_head=head,
        verdict="needs changes",
        body="Fix the EOF hygiene error.",
        runner=runner,
    )

    assert published["state"] == "AWAITING_AGY_FIXES"
    assert published["review"]["id"] == 42
    assert "event=REQUEST_CHANGES" in calls[1]
    assert f"commit_id={head}" in calls[1]
    assert calls[2][-1] == "state,headRefOid"


def test_fails_closed_when_head_moves_before_publication() -> None:
    expected = "a" * 40
    actual = "b" * 40

    def runner(command, **kwargs):
        return result({"state": "OPEN", "headRefOid": actual})

    with pytest.raises(ReviewPublishError, match="head changed"):
        publish_review(
            repo="tticom/score2gp",
            pr_number=394,
            expected_head=expected,
            verdict="needs changes",
            body="Finding.",
            runner=runner,
        )


def test_fails_when_published_review_is_not_authoritative() -> None:
    head = "a" * 40
    responses = iter(
        [
            result({"state": "OPEN", "headRefOid": head}),
            result({"id": 42}),
            result({"state": "OPEN", "headRefOid": head}),
            result([]),
        ]
    )

    def runner(command, **kwargs):
        return next(responses)

    with pytest.raises(ReviewPublishError, match="not authoritative"):
        publish_review(
            repo="tticom/score2gp",
            pr_number=394,
            expected_head=head,
            verdict="needs changes",
            body="Finding.",
            runner=runner,
        )


def test_fails_closed_when_head_moves_during_publication() -> None:
    expected = "a" * 40
    actual = "b" * 40
    responses = iter(
        [
            result({"state": "OPEN", "headRefOid": expected}),
            result({"id": 42}),
            result({"state": "OPEN", "headRefOid": actual}),
        ]
    )

    def runner(command, **kwargs):
        return next(responses)

    with pytest.raises(ReviewPublishError, match="during publication"):
        publish_review(
            repo="tticom/score2gp",
            pr_number=394,
            expected_head=expected,
            verdict="needs changes",
            body="Finding.",
            runner=runner,
        )
