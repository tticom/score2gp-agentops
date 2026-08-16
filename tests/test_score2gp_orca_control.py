from copy import deepcopy

import pytest

from scripts.score2gp_orca_control import (
    ControlError,
    RuntimeIdentity,
    build_assignment,
    resolve_state,
    validate_legacy_alignment,
    verify_merge_gate,
)


def authority() -> dict:
    return {
        "schema_version": 1,
        "authority_revision": 4,
        "task": {
            "id": "108",
            "title": "Bounded repair",
            "status": "RUNNING",
            "repository": "tticom/score2gp",
            "branch": "feat/task-108",
            "pull_request": 441,
            "owner_role": "implementation",
            "prompt": "prompt.md",
            "allowed_paths": ["src/a.py", "tests/test_a.py"],
            "acceptance": ["prove repair"],
            "required_evidence": ["negative_control"],
        },
        "incidents": [],
        "roles": {
            "implementation": {
                "github_logins": ["worker"],
                "allowed_actions": ["edit", "test"],
                "forbidden_actions": ["merge"],
            },
            "reviewer": {
                "github_logins": ["reviewer"],
                "allowed_actions": ["publish_review"],
                "forbidden_actions": ["edit", "merge"],
            },
            "governance": {
                "github_logins": ["governor"],
                "allowed_actions": ["publish_governance_review"],
                "forbidden_actions": ["product_edit", "merge"],
            },
            "merge_controller": {
                "github_logins": ["merge-app"],
                "allowed_actions": ["merge_exact_head"],
                "forbidden_actions": ["edit", "bypass"],
            },
        },
        "merge_policy": {
            "required_checks": ["test"],
            "minimum_approvals": 2,
            "require_governance_go": True,
            "require_reviewed_head": True,
            "require_resolved_threads": True,
            "allow_admin_bypass": False,
        },
    }


def live(reviews=None) -> dict:
    return {
        "pull_request": {
            "number": 441,
            "state": "OPEN",
            "head_branch": "feat/task-108",
            "head_sha": "a" * 40,
            "reviews": reviews or [],
            "checks": [{"name": "test", "conclusion": "SUCCESS"}],
            "unresolved_threads": 0,
        }
    }


def test_active_incident_blocks_resolution_and_dispatch() -> None:
    config = authority()
    config["incidents"] = [{"id": "incident-1", "status": "OPEN", "opened_by": "report.md"}]
    resolved = resolve_state(config, live())
    assert resolved["state"] == "BLOCKED"
    assert resolved["blockers"] == ["incident-1"]
    with pytest.raises(ControlError, match="not dispatchable"):
        build_assignment(config, live(), resolved, RuntimeIdentity("tticom", "worker"), "b" * 40)


def test_legacy_active_task_divergence_fails_closed() -> None:
    text = """# Active Task
**Task**: Task 999 — Wrong task
**Status**: IN_PROGRESS
**Repository**: tticom/score2gp
**PR Branch**: `feat/task-108`
**Pull Request**: 441
"""
    with pytest.raises(ControlError, match="diverges.*task"):
        validate_legacy_alignment(authority(), text)


def test_resolved_incident_is_not_reconstructed_from_prose() -> None:
    config = authority()
    config["incidents"] = [{
        "id": "incident-1",
        "status": "RESOLVED",
        "opened_by": "incident.md",
        "resolved_by": "remediation.md",
    }]
    assert resolve_state(config, live())["state"] == "REVIEW_REQUIRED"


def test_current_head_changes_requested_returns_only_to_implementation() -> None:
    reviews = [{"author": "reviewer", "state": "CHANGES_REQUESTED", "head_sha": "a" * 40}]
    resolved = resolve_state(authority(), live(reviews))
    assert resolved["state"] == "RUNNING"
    assert resolved["dispatch_role"] == "implementation"


def test_worker_receives_bounded_assignment_and_cannot_merge_or_sequence() -> None:
    reviews = [{"author": "reviewer", "state": "CHANGES_REQUESTED", "head_sha": "a" * 40}]
    config = authority()
    facts = live(reviews)
    assignment = build_assignment(
        config,
        facts,
        resolve_state(config, facts),
        RuntimeIdentity("tticom", "worker"),
        "b" * 40,
    )
    assert assignment["work"]["allowed_paths"] == ["src/a.py", "tests/test_a.py"]
    assert assignment["work"]["expected_head_sha"] == "a" * 40
    assert assignment["completion_contract"]["may_select_next_task"] is False
    assert assignment["completion_contract"]["may_merge"] is False
    assert "merge" in assignment["capabilities"]["forbidden_actions"]


def test_wrong_identity_cannot_claim_worker_role() -> None:
    config = authority()
    resolved = resolve_state(config, live())
    with pytest.raises(ControlError, match="not authorised"):
        build_assignment(config, live(), resolved, RuntimeIdentity("tticom", "governor"), "b" * 40)


def merge_ready() -> dict:
    facts = live([
        {"author": "reviewer-a", "state": "APPROVED", "head_sha": "a" * 40},
        {"author": "reviewer-b", "state": "APPROVED", "head_sha": "a" * 40},
    ])
    facts["governance"] = {"decision": "GO", "reviewed_head_sha": "a" * 40}
    facts["merge_controller_login"] = "merge-app"
    facts["admin_bypass"] = False
    return facts


def test_merge_gate_allows_only_exact_reviewed_head() -> None:
    assert verify_merge_gate(authority(), merge_ready())["decision"] == "ALLOW"


def test_stale_reviewed_sha_blocks_merge() -> None:
    facts = merge_ready()
    facts["pull_request"]["head_sha"] = "c" * 40
    decision = verify_merge_gate(authority(), facts)
    assert decision["decision"] == "DENY"
    assert "reviewed_head_mismatch" in decision["failures"]
    assert "current_head_not_approved" in decision["failures"]


@pytest.mark.parametrize(
    ("mutation", "failure"),
    [
        (lambda x: x["pull_request"]["checks"].clear(), "required_check_not_success:test"),
        (lambda x: x["governance"].update(decision="NO_GO"), "governance_go_missing"),
        (lambda x: x["pull_request"].update(unresolved_threads=1), "unresolved_review_threads"),
        (lambda x: x.update(merge_controller_login="worker"), "merge_controller_identity_not_configured"),
        (lambda x: x.update(admin_bypass=True), "admin_bypass_forbidden"),
    ],
)
def test_merge_gate_fails_closed(mutation, failure: str) -> None:
    facts = deepcopy(merge_ready())
    mutation(facts)
    assert failure in verify_merge_gate(authority(), facts)["failures"]
