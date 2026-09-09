"""Behavioral tests for the autonomous orchestration decision interface."""

from copy import deepcopy
from typing import Any

import pytest

from scripts.score2gp_orchestrator import (
    LIFECYCLE_STATES,
    OrchestrationError,
    advance,
    build_task_registry,
    render_active_task,
    resolve_task_lifecycle,
    upgrade_authority,
)


def authority(status: str = "RUNNING") -> dict:
    return {
        "schema_version": 2,
        "authority_revision": 7,
        "task": {
            "id": "NPG-00A",
            "title": "Inventory the native conversion baseline",
            "objective": "Produce an exact dependency and evidence inventory.",
            "status": status,
            "repository": "tticom/score2gp-agentops",
            "base_branch": "main",
            "branch": "agy/npg-00a-baseline",
            "pull_request": 600,
            "owner_role": "implementation",
            "allowed_paths": ["projects/score2gp/reports/baseline.md"],
            "validation_commands": ["python3 scripts/score2gp_governance_audit.py"],
            "dependencies": [],
            "stop_conditions": ["source_pdf_missing"],
            "reviewer_role": "reviewer",
            "delivery_action": "pull_request",
        },
        "incidents": [],
    }


def live(*, state: str = "OPEN", reviews: list[dict] | None = None) -> dict:
    return {
        "snapshot": {"captured_at": "2026-08-19T20:00:00Z"},
        "pull_request": {
            "number": 600,
            "state": state,
            "head_branch": "agy/npg-00a-baseline",
            "head_sha": "a" * 40,
            "reviews": reviews or [],
            "checks": [{"name": "test", "conclusion": "SUCCESS"}],
            "unresolved_threads": 0,
        },
    }


def test_authorized_unpublished_task_executes_one_bounded_assignment() -> None:
    facts = {"snapshot": {"captured_at": "2026-08-19T20:00:00Z"}}

    decision = advance(authority("READY"), facts)

    assert decision["action"] == "EXECUTE_ASSIGNMENT"
    assert decision["dispatch_role"] == "implementation"
    assert decision["assignment"]["objective"].startswith("Produce an exact")
    assert decision["assignment"]["allowed_paths"] == [
        "projects/score2gp/reports/baseline.md"
    ]
    assert decision["assignment"]["may_merge"] is False


def test_changed_head_returns_exact_pr_to_author_for_remediation() -> None:
    reviews = [
        {
            "author": "reviewer",
            "state": "CHANGES_REQUESTED",
            "head_sha": "a" * 40,
        }
    ]

    decision = advance(authority(), live(reviews=reviews))

    assert decision["action"] == "REMEDIATE_CURRENT_PR"
    assert decision["dispatch_role"] == "implementation"
    assert decision["assignment"]["expected_head_sha"] == "a" * 40


def test_unreviewed_head_awaits_independent_review() -> None:
    decision = advance(authority(), live())

    assert decision["action"] == "AWAIT_REVIEW"
    assert decision["dispatch_role"] == "reviewer"


def test_approved_head_awaits_human_merge() -> None:
    reviews = [
        {"author": "reviewer", "state": "APPROVED", "head_sha": "a" * 40}
    ]

    decision = advance(authority(), live(reviews=reviews))

    assert decision["action"] == "AWAIT_HUMAN_MERGE"
    assert "dispatch_role" not in decision


def test_musical_ambiguity_requests_adjudication_before_other_work() -> None:
    facts = live()
    facts["adjudication"] = {
        "status": "REQUIRED",
        "packet": "work/adjudication/measure-12.json",
        "reason_codes": ["conflicting_meter_candidates"],
    }

    decision = advance(authority(), facts)

    assert decision["action"] == "REQUEST_MUSICAL_ADJUDICATION"
    assert decision["adjudication_packet"] == "work/adjudication/measure-12.json"


def test_merged_task_proposes_next_task_without_executing_it() -> None:
    decision = advance(authority(), live(state="MERGED"))

    assert decision["action"] == "PROPOSE_NEXT_TASK"
    assert decision["may_execute_next_task"] is False


def test_merged_task_awaits_review_for_matching_promotion_pr() -> None:
    config = authority("MERGED")
    config["next_task_proposal"] = {
        "id": "REC-02", "status": "PROPOSED", "repository": "tticom/score2gp-agentops",
    }
    facts = live()
    facts["snapshot"]["repository"] = "tticom/score2gp-agentops"
    facts["pull_request"]["head_branch"] = "gov/promote-rec-02"
    decision = advance(config, facts)
    assert decision["action"] == "AWAIT_REVIEW"


def test_incident_blocks_all_progress() -> None:
    config = authority()
    config["incidents"] = [{"id": "incident-1", "status": "BLOCKING"}]

    decision = advance(config, live())

    assert decision["action"] == "BLOCKED"
    assert decision["blockers"] == ["incident-1"]


def test_replay_is_idempotent_when_only_capture_time_changes() -> None:
    first_live = live()
    second_live = deepcopy(first_live)
    second_live["snapshot"]["captured_at"] = "2026-08-19T20:05:00Z"

    first = advance(authority(), first_live)
    second = advance(authority(), second_live)

    assert first == second
    assert first["decision_id"].startswith("decision-")


def test_invalid_task_contract_fails_closed() -> None:
    config = authority()
    del config["task"]["validation_commands"]

    with pytest.raises(OrchestrationError, match="validation_commands"):
        advance(config, live())


def test_failed_required_validation_blocks_review_and_merge() -> None:
    facts = live()
    facts["pull_request"]["checks"] = [{"name": "test", "conclusion": "FAILURE"}]

    decision = advance(authority(), facts)

    assert decision["action"] == "BLOCKED"
    assert decision["reason"] == "required_validation_not_successful"
    assert decision["blockers"] == ["test"]


def test_triggered_stop_condition_blocks_assignment() -> None:
    facts = {"stop_conditions": ["source_pdf_missing"]}

    decision = advance(authority("READY"), facts)

    assert decision["action"] == "BLOCKED"
    assert decision["reason"] == "task_stop_condition_triggered"


def test_v1_authority_is_upgraded_at_the_compatibility_adapter() -> None:
    legacy = {
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
            "allowed_paths": ["src/a.py"],
            "acceptance": ["prove repair"],
            "required_evidence": ["focused_tests"],
        },
        "incidents": [],
    }

    upgraded = upgrade_authority(legacy)

    assert upgraded["schema_version"] == 2
    assert upgraded["task"]["objective"] == "Bounded repair"
    assert upgraded["task"]["validation_commands"] == []
    assert upgraded["task"]["delivery_action"] == "pull_request"


def test_active_task_is_a_generated_view_of_authority() -> None:
    rendered = render_active_task(authority("READY"))

    assert "<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->" in rendered
    assert "**Task**: NPG-00A — Inventory the native conversion baseline" in rendered
    assert "**Status**: APPROVED" in rendered
    assert "**PR Branch**: `agy/npg-00a-baseline`" in rendered
    assert "`projects/score2gp/reports/baseline.md`" in rendered


@pytest.mark.parametrize("invalid_pr,expected_reason", [
    (None, "active_task_missing_pull_request"),
    ("", "active_task_invalid_pull_request"),
    ("not-a-number", "active_task_invalid_pull_request"),
    (441.9, "active_task_invalid_pull_request"),
    ("441.9", "active_task_invalid_pull_request"),
    (True, "active_task_invalid_pull_request"),
    (False, "active_task_invalid_pull_request"),
    (0, "active_task_invalid_pull_request"),
    (-1, "active_task_invalid_pull_request"),
    ([], "active_task_invalid_pull_request"),
    ({}, "active_task_invalid_pull_request"),
])
def test_advance_handles_missing_or_invalid_authority_pull_request(
    invalid_pr: Any, expected_reason: str
) -> None:
    auth = authority("RUNNING")
    auth["task"]["pull_request"] = invalid_pr
    decision = advance(auth, live())
    assert decision["action"] == "BLOCKED"
    assert decision["reason"] == expected_reason


def test_build_task_registry_preserves_required_metadata() -> None:
    auth = authority("RUNNING")
    auth["next_task_proposal"] = {
        "id": "REC-06",
        "title": "Staff and System Topology",
        "objective": "Reconstruct pages",
        "status": "PROPOSED",
        "repository": "tticom/score2gp",
        "base_branch": "main",
        "branch": "feat/rec-06-topology",
        "owner_role": "implementation",
        "reviewer_role": "reviewer",
        "allowed_paths": ["src/topology.py"],
        "validation_commands": ["python3 -m pytest tests/test_topology.py"],
    }
    registry = build_task_registry(auth, live())
    assert "NPG-00A" in registry
    assert "REC-06" in registry

    rec = registry["NPG-00A"]
    required_keys = {
        "id", "repository", "base_branch", "branch", "owner_role", "reviewer_role",
        "pull_request", "head_sha", "lifecycle_state", "lease_id",
        "validation_commands", "validation_contract", "allowed_paths",
        "recovery_receipt_location",
    }
    assert required_keys <= rec.keys()
    assert rec["repository"] == "tticom/score2gp-agentops"
    assert rec["base_branch"] == "main"
    assert rec["branch"] == "agy/npg-00a-baseline"
    assert rec["owner_role"] == "implementation"
    assert rec["reviewer_role"] == "reviewer"
    assert rec["pull_request"] == 600
    assert rec["head_sha"] == "a" * 40
    assert rec["lifecycle_state"] in LIFECYCLE_STATES


def test_resolve_task_lifecycle_covers_all_nine_states() -> None:
    # 1. authoring
    t_auth = {"status": "RUNNING", "pull_request": None}
    assert resolve_task_lifecycle(t_auth) == "authoring"

    # 2. pr_open
    t_open = {"status": "RUNNING", "pull_request": 100}
    assert resolve_task_lifecycle(t_open) == "pr_open"

    # 3. review_required
    live_review_req = {
        "pull_request": {
            "number": 100,
            "state": "OPEN",
            "head_sha": "a" * 40,
            "reviews": [],
        }
    }
    assert resolve_task_lifecycle(t_open, live_review_req) == "review_required"

    # 4. changes_requested
    live_changes = {
        "pull_request": {
            "number": 100,
            "state": "OPEN",
            "head_sha": "a" * 40,
            "reviews": [{"author": "rev", "state": "CHANGES_REQUESTED", "head_sha": "a" * 40}],
        }
    }
    assert resolve_task_lifecycle(t_open, live_changes) == "changes_requested"

    # 5. approved (pending checks or unresolved threads)
    live_approved = {
        "pull_request": {
            "number": 100,
            "state": "OPEN",
            "head_sha": "a" * 40,
            "reviews": [{"author": "rev", "state": "APPROVED", "head_sha": "a" * 40}],
            "checks": [{"name": "ci", "conclusion": "FAILURE"}],
            "unresolved_threads": 0,
        }
    }
    assert resolve_task_lifecycle(t_open, live_approved) == "approved"

    # 6. human_merge (approved, all checks passed, 0 unresolved threads)
    live_merge = {
        "pull_request": {
            "number": 100,
            "state": "OPEN",
            "head_sha": "a" * 40,
            "reviews": [{"author": "rev", "state": "APPROVED", "head_sha": "a" * 40}],
            "checks": [{"name": "ci", "conclusion": "SUCCESS"}],
            "unresolved_threads": 0,
        }
    }
    assert resolve_task_lifecycle(t_open, live_merge) == "human_merge"

    # 7. merged
    t_merged = {"status": "MERGED", "pull_request": 100}
    assert resolve_task_lifecycle(t_merged) == "merged"

    # 8. reconciled
    t_reconciled = {"status": "MERGED", "reconciled": True}
    assert resolve_task_lifecycle(t_reconciled) == "reconciled"

    # 9. successor_prepared
    t_succ = {"status": "PROPOSED"}
    assert resolve_task_lifecycle(t_succ) == "successor_prepared"


def test_cross_task_branch_reuse_in_orchestrator_fails_closed() -> None:
    auth = authority("RUNNING")
    auth["next_task_proposal"] = {
        "id": "REC-06",
        "title": "Staff and System Topology",
        "objective": "Reconstruct pages",
        "status": "RUNNING",
        "repository": "tticom/score2gp",
        "base_branch": "main",
        "branch": "agy/npg-00a-baseline",  # Reuse active branch of NPG-00A!
        "owner_role": "implementation",
        "reviewer_role": "reviewer",
        "allowed_paths": ["src/topology.py"],
        "validation_commands": ["python3 -m pytest tests/test_topology.py"],
        "dependencies": [],
        "stop_conditions": [],
        "delivery_action": "pull_request",
    }
    with pytest.raises(OrchestrationError, match="cross-task branch reuse detected"):
        build_task_registry(auth)


def test_advance_with_task_id() -> None:
    auth = authority("READY")
    auth["next_task_proposal"] = {
        "id": "REC-06",
        "title": "Staff and System Topology",
        "objective": "Reconstruct pages",
        "status": "READY",
        "repository": "tticom/score2gp",
        "base_branch": "main",
        "branch": "feat/rec-06-topology",
        "pull_request": None,
        "owner_role": "implementation",
        "reviewer_role": "reviewer",
        "allowed_paths": ["src/topology.py"],
        "validation_commands": ["python3 -m pytest tests/test_topology.py"],
        "dependencies": [],
        "stop_conditions": [],
        "delivery_action": "pull_request",
    }
    decision = advance(auth, {}, task_id="REC-06")
    assert decision["action"] == "EXECUTE_ASSIGNMENT"
    assert decision["task_id"] == "REC-06"

