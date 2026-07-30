import json
import subprocess

import pytest

from scripts.score2gp_publish_review import (
    ReviewPublishError,
    normalize_verdict,
    publish_review,
    validate_approval_evidence,
)
from scripts.score2gp_review_evidence_gate import (
    ATTESTATION,
    ReviewEvidenceError,
    active_strikes,
    validate_approval_packet,
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


def approval_packet(probe_count: int = 2) -> dict:
    head = "a" * 40
    return {
        "verdict": "APPROVE",
        "review_head": head,
        "baseline_failure_expectation": "Assume duration evidence is dropped before GPIF emission.",
        "claims": [{
            "claim": "duration evidence reaches ScoreIR",
            "status": "verified",
            "production_path": "PDF -> TabRaw -> ScoreIR",
            "evidence_path": "reviewer probes",
            "false_success_mutation": "inject duration below PDF extraction",
            "failure_oracle": "Final GPIF rhythm differs from the fixture oracle.",
            "disproof_attempt": "Disabled duration propagation and inspected final GPIF.",
            "probe_names": ["probe-0"],
        }],
        "probes": [
            {
                "name": f"probe-{index}",
                "reviewer_created": True,
                "author_test_only": False,
                "production_path": True,
                "head_sha": head,
                "probe_type": "mutation" if index == 0 else "artifact",
                "command": f"python probe_{index}.py",
                "input": f"fixture-{index}",
                "false_success_mutation": f"mutation-{index}",
                "observed_output": f"distinct-output-{index}",
                "exit_code": 0,
                "output_sha256": f"{index + 1:064x}",
                "invariant": f"invariant-{index}",
                "result": "killed",
            }
            for index in range(probe_count)
        ],
        "residual_risks": ["Proprietary GUI rendering remains untested."],
        "integrity_attestation": ATTESTATION,
    }


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


def test_approval_packet_quota_increases_with_reviewer_strikes() -> None:
    assert validate_approval_packet(
        approval_packet(2), expected_head="a" * 40, strikes=0, high_risk=False
    ) == (2, 4)
    with pytest.raises(ReviewEvidenceError, match="at least 3"):
        validate_approval_packet(
            approval_packet(2), expected_head="a" * 40, strikes=1, high_risk=False
        )
    assert validate_approval_packet(
        approval_packet(3), expected_head="a" * 40, strikes=1, high_risk=False
    ) == (3, 6)


def test_approval_packet_is_bound_to_head_and_claims_to_probes() -> None:
    packet = approval_packet(2)
    packet["review_head"] = "b" * 40
    with pytest.raises(ReviewEvidenceError, match="review_head"):
        validate_approval_packet(
            packet, expected_head="a" * 40, strikes=0, high_risk=False
        )

    packet = approval_packet(2)
    packet["claims"][0]["probe_names"] = ["invented-probe"]
    with pytest.raises(ReviewEvidenceError, match="unknown probes"):
        validate_approval_packet(
            packet, expected_head="a" * 40, strikes=0, high_risk=False
        )


def test_approval_requires_mutation_and_final_artifact_probes() -> None:
    packet = approval_packet(2)
    for probe in packet["probes"]:
        probe["probe_type"] = "boundary"
    with pytest.raises(ReviewEvidenceError, match="mutation and final-artifact"):
        validate_approval_packet(
            packet, expected_head="a" * 40, strikes=0, high_risk=False
        )


def test_scorecard_returns_reviewer_strike_count() -> None:
    scorecard = {"reviewers": {"tticomgov-code": {"active_strikes": 1}}}
    assert active_strikes(scorecard, "tticomgov-code") == 1


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


def test_approved_publication_rejects_body_only_evidence_before_github() -> None:
    called = False

    def runner(command, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("GitHub must not be called")

    with pytest.raises(ReviewPublishError, match="machine-validated evidence"):
        publish_review(
            repo="tticom/score2gp",
            pr_number=396,
            expected_head="a" * 40,
            verdict="APPROVED",
            body=approval_body(),
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
