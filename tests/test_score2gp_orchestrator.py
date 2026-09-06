"""Behavioral tests for the autonomous orchestration decision interface."""

from copy import deepcopy
from typing import Any

import pytest

from scripts.score2gp_orchestrator import (
    OrchestrationError,
    advance,
    reconcile,
    render_active_task,
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


def live_merged(
    *,
    head_sha: str = "a" * 40,
    merge_commit: str = "c" * 40,
    pr_number: int = 600,
    branch: str = "agy/npg-00a-baseline",
    repo: str = "tticom/score2gp-agentops",
) -> dict:
    return {
        "snapshot": {"captured_at": "2026-08-19T20:00:00Z", "repository": repo},
        "pull_request": {
            "number": pr_number,
            "state": "MERGED",
            "head_branch": branch,
            "head_sha": head_sha,
            "merge_commit": merge_commit,
            "reviews": [],
            "checks": [{"name": "test", "conclusion": "SUCCESS"}],
            "unresolved_threads": 0,
        },
    }


def test_reconcile_moves_active_task_to_completed_tasks_with_contract_and_metadata() -> None:
    auth = authority("RUNNING")
    auth["next_task_proposal"] = {
        "id": "NPG-01",
        "title": "Next step",
        "status": "PROPOSED",
        "repository": "tticom/score2gp-agentops",
    }
    facts = live_merged(head_sha="1" * 40, merge_commit="2" * 40)

    updated = reconcile(auth, facts)

    assert len(updated["completed_tasks"]) == 1
    completed = updated["completed_tasks"][0]
    assert completed["id"] == "NPG-00A"
    assert completed["status"] == "MERGED"
    assert completed["head_sha"] == "1" * 40
    assert completed["merge_commit"] == "2" * 40

    # Task contract preserved
    assert completed["title"] == auth["task"]["title"]
    assert completed["objective"] == auth["task"]["objective"]
    assert completed["repository"] == auth["task"]["repository"]
    assert completed["branch"] == auth["task"]["branch"]
    assert completed["allowed_paths"] == auth["task"]["allowed_paths"]
    assert completed["validation_commands"] == auth["task"]["validation_commands"]
    assert completed["dependencies"] == auth["task"]["dependencies"]
    assert completed["stop_conditions"] == auth["task"]["stop_conditions"]
    assert completed["reviewer_role"] == auth["task"]["reviewer_role"]
    assert completed["delivery_action"] == auth["task"]["delivery_action"]

    # Active task status updated to MERGED
    assert updated["task"]["status"] == "MERGED"

    # Next task proposal remains PROPOSED
    assert updated["next_task_proposal"]["status"] == "PROPOSED"


def test_reconciled_authority_advance_cannot_dispatch_successor() -> None:
    auth = authority("RUNNING")
    auth["next_task_proposal"] = {
        "id": "NPG-01",
        "title": "Next step",
        "status": "PROPOSED",
        "repository": "tticom/score2gp-agentops",
    }
    facts = live_merged()
    updated = reconcile(auth, facts)

    decision = advance(updated, facts)

    assert decision["action"] == "PROPOSE_NEXT_TASK"
    assert decision["reason"] == "task_declared_complete"
    assert decision["may_execute_next_task"] is False
    assert "assignment" not in decision
    assert "dispatch_role" not in decision


def test_reconcile_replaying_same_verified_merge_does_not_duplicate_completed_task() -> None:
    auth = authority("RUNNING")
    facts = live_merged()

    first = reconcile(auth, facts)
    assert len(first["completed_tasks"]) == 1

    second = reconcile(first, facts)
    assert len(second["completed_tasks"]) == 1
    assert second == first


@pytest.mark.parametrize("mutator,match_err", [
    (lambda l: l["pull_request"].update(state="OPEN"), "expected 'MERGED'"),
    (lambda l: l["pull_request"].update(state="CLOSED"), "expected 'MERGED'"),
    (lambda l: l["pull_request"].update(number=999), "PR number mismatch"),
    (lambda l: l["pull_request"].update(head_branch="wrong-branch"), "branch mismatch"),
    (lambda l: l.update(snapshot={"repository": "wrong/repo"}), "repository mismatch"),
    (lambda l: l["pull_request"].update(head_sha=""), "invalid or missing product head SHA"),
    (lambda l: l["pull_request"].update(head_sha="short"), "invalid or missing product head SHA"),
    (lambda l: l["pull_request"].update(head_sha="z" * 40), "invalid or missing product head SHA"),
    (lambda l: l["pull_request"].pop("merge_commit"), "invalid or missing merge commit SHA"),
    (lambda l: l["pull_request"].update(merge_commit="invalid"), "invalid or missing merge commit SHA"),
    (lambda l: l.update(governance={"reviewed_head_sha": "b" * 40}), "does not match reviewed head"),
    (lambda l: l.update(expected_head_sha="b" * 40), "does not match expected head"),
    (lambda l: l.update(expected_merge_commit="b" * 40), "does not match expected merge commit"),
])
def test_reconcile_fails_closed_and_leaves_authority_byte_for_byte_unchanged(
    mutator: Any, match_err: str
) -> None:
    auth = authority("RUNNING")
    facts = live_merged()
    mutator(facts)

    original = deepcopy(auth)
    with pytest.raises(OrchestrationError, match=match_err):
        reconcile(auth, facts)

    assert auth == original


def test_reconcile_refuses_already_completed_task_with_conflicting_merge() -> None:
    auth = authority("RUNNING")
    facts = live_merged(merge_commit="1" * 40)
    updated = reconcile(auth, facts)

    conflicting_facts = live_merged(merge_commit="2" * 40)
    with pytest.raises(OrchestrationError, match="different merge metadata"):
        reconcile(updated, conflicting_facts)


def test_reconciled_active_task_never_reports_merged_task_as_active() -> None:
    auth = authority("RUNNING")
    facts = live_merged()
    updated = reconcile(auth, facts)

    rendered = render_active_task(updated)

    assert "**Status**: MERGED" in rendered
    assert "**Status**: APPROVED" not in rendered
    assert "**Status**: PROMOTED" not in rendered
    assert "**Status**: IN_PROGRESS" not in rendered
