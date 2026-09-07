"""Tests for the Orca control plane and state reducer.

Rationale for synthetic/mocked tests:
This test suite verifies the state resolution, validation, and merge gate logic of the Orca control plane (non-domain infrastructure). Since it relies on querying the GitHub API via the `gh` command-line utility, running real integration tests against GitHub during test execution would require active network access, API tokens with repository access, and live PR mutations. To ensure deterministic, offline, and fast test execution, the GitHub API calls and CLI executions are synthetically mocked. Real-world end-to-end integration and GitHub API schema checks are shadow-tested via actual manual runs and Orca supervisor pilot execution.
"""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

import pytest

from scripts.score2gp_orca_control import (
    ControlError,
    RuntimeIdentity,
    build_assignment,
    capture_live_state,
    current_head_review,
    reconcile,
    reconcile_post_merge,
    resolve_state,
    validate_assignment,
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
        },
        "protection": {"active_rulesets": 1, "current_user_can_bypass": False},
    }


def test_active_incident_blocks_resolution_and_dispatch() -> None:
    config = authority()
    config["incidents"] = [{"id": "incident-1", "status": "OPEN", "opened_by": "report.md"}]
    resolved = resolve_state(config, live())
    assert resolved["state"] == "BLOCKED"
    assert resolved["blockers"] == ["incident-1"]
    with pytest.raises(ControlError, match="not dispatchable"):
        build_assignment(config, live(), resolved, RuntimeIdentity("tticom", "worker"), "b" * 40)



def test_promoted_legacy_active_task_alignment_passes() -> None:
    text = """# Active Task
**Task**: 108 — Bounded repair
**Status**: PROMOTED
**Repository**: tticom/score2gp
**PR Branch**: `feat/task-108`
**Pull Request**: 441
"""
    auth = authority()
    auth["task"]["status"] = "PROMOTED"
    validate_legacy_alignment(auth, text)


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


def test_missing_authorised_pull_request_fails_closed() -> None:
    config = authority()
    config["task"]["pull_request"] = None

    resolved = resolve_state(config, live())

    assert resolved == {
        "schema_version": 1,
        "state": "BLOCKED",
        "reason": "active_task_missing_pull_request",
        "task_id": "108",
    }


def test_assignment_validation_rejects_changed_head() -> None:
    config = authority()
    facts = live([{"author": "reviewer", "state": "CHANGES_REQUESTED", "head_sha": "a" * 40}])
    identity = RuntimeIdentity("tticom", "worker")
    assignment = build_assignment(config, facts, resolve_state(config, facts), identity, "b" * 40)
    changed = deepcopy(facts)
    changed["pull_request"]["head_sha"] = "c" * 40
    with pytest.raises(ControlError, match="stale"):
        validate_assignment(config, changed, assignment, identity, "b" * 40)


def test_snapshot_normalizes_github_facts(monkeypatch) -> None:
    responses = iter([
        {
            "number": 441,
            "state": "OPEN",
            "headRefName": "feat/task-108",
            "headRefOid": "a" * 40,
            "baseRefName": "main",
            "author": {"login": "worker"},
            "reviews": [{"author": {"login": "reviewer"}, "state": "CHANGES_REQUESTED", "commit": {"oid": "a" * 40}}],
            "statusCheckRollup": [{"name": "test", "conclusion": "SUCCESS"}],
        },
        {"data": {"repository": {"pullRequest": {"reviewThreads": {"nodes": [{"isResolved": False}, {"isResolved": True}], "pageInfo": {"hasNextPage": False, "endCursor": None}}}}}},
        [{"id": 7, "enforcement": "active"}],
        {"id": 7, "current_user_can_bypass": "never"},
    ])
    monkeypatch.setattr("scripts.score2gp_orca_control.run_json", lambda command: next(responses))
    snapshot = capture_live_state("tticom/score2gp", 441)
    assert snapshot["pull_request"]["unresolved_threads"] == 1
    assert snapshot["pull_request"]["reviews"][0]["head_sha"] == "a" * 40
    assert snapshot["protection"]["active_rulesets"] == 1
    assert snapshot["protection"]["current_user_can_bypass"] is False


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
        (lambda x: x["protection"].update(current_user_can_bypass=True), "merge_controller_can_bypass_ruleset"),
    ],
)
def test_merge_gate_fails_closed(mutation, failure: str) -> None:
    facts = deepcopy(merge_ready())
    mutation(facts)
    assert failure in verify_merge_gate(authority(), facts)["failures"]


def test_multiple_reviews_by_same_author_resolves_latest() -> None:
    # If the same author first requests changes and then approves the head, state is APPROVED
    reviews = [
        {"author": "reviewer-a", "state": "CHANGES_REQUESTED", "head_sha": "a" * 40},
        {"author": "reviewer-a", "state": "APPROVED", "head_sha": "a" * 40},
    ]
    assert current_head_review(live(reviews)["pull_request"]) == "APPROVED"

    # If they approve first and then request changes, it should resolve to CHANGES_REQUESTED
    reviews_reversed = [
        {"author": "reviewer-a", "state": "APPROVED", "head_sha": "a" * 40},
        {"author": "reviewer-a", "state": "CHANGES_REQUESTED", "head_sha": "a" * 40},
    ]
    assert current_head_review(live(reviews_reversed)["pull_request"]) == "CHANGES_REQUESTED"


def test_advance_cli_uses_schema_v2_authority_without_legacy_pointer(
    tmp_path: Path,
) -> None:
    config = authority()
    config["schema_version"] = 2
    config["task"].update(
        objective="Apply the bounded repair.",
        base_branch="main",
        validation_commands=["python3 -m pytest"],
        dependencies=[],
        stop_conditions=[],
        reviewer_role="reviewer",
        delivery_action="pull_request",
    )
    authority_path = tmp_path / "authority.json"
    live_path = tmp_path / "live.json"
    authority_path.write_text(json.dumps(config), encoding="utf-8")
    live_path.write_text(json.dumps(live()), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/score2gp_orca_control.py",
            "advance",
            "--authority",
            str(authority_path),
            "--live",
            str(live_path),
        ],
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["action"] == "AWAIT_REVIEW"


def test_completed_task_rejects_unrelated_open_pr() -> None:
    config = authority()
    config["task"]["status"] = "MERGED"
    config["next_task_proposal"] = {"id": "109", "status": "PROPOSED", "repository": "tticom/score2gp-agentops", "branch": "feat/task-109"}
    facts = {"snapshot": {"repository": "tticom/score2gp-agentops"}, "pull_request": {"number": 613, "state": "OPEN", "head_branch": "fix/unrelated", "head_sha": "a" * 40, "reviews": []}}
    assert resolve_state(config, facts)["state"] == "COMPLETE"


def test_completed_task_allows_scoped_control_plane_bootstrap_review() -> None:
    config = authority()
    config["task"]["status"] = "MERGED"
    facts = {"snapshot": {"repository": "tticom/score2gp-agentops"}, "control_plane_repair": True, "pull_request": {"number": 613, "state": "OPEN", "head_branch": "fix/control-plane-repair", "head_sha": "a" * 40, "reviews": []}}
    resolved = resolve_state(config, facts)
    assert resolved["state"] == "REVIEW_REQUIRED"
    assert resolved["dispatch_role"] == "reviewer"
    assignment = build_assignment(config, facts, resolved, RuntimeIdentity("tticom", "reviewer"), "b" * 40)
    assert assignment["work"]["pull_request"] == 613
    assert assignment["work"]["branch"] == "fix/control-plane-repair"


def test_promoted_active_task_allows_isolated_control_plane_bootstrap_review() -> None:
    config = authority()
    facts = {
        "snapshot": {"repository": "tticom/score2gp-agentops"},
        "control_plane_repair": True,
        "pull_request": {
            "number": 620,
            "state": "OPEN",
            "head_branch": "codex/control-plane-bootstrap-repair",
            "head_sha": "a" * 40,
            "reviews": [],
        },
    }

    resolved = resolve_state(config, facts)

    assert resolved["state"] == "REVIEW_REQUIRED"
    assert resolved["dispatch_role"] == "reviewer"
    assignment = build_assignment(
        config,
        facts,
        resolved,
        RuntimeIdentity("tticom", "reviewer"),
        "b" * 40,
    )
    assert assignment["authority"]["task_id"] == "108"
    assert assignment["work"]["pull_request"] == 620
    assert assignment["work"]["branch"] == "codex/control-plane-bootstrap-repair"


def test_promotion_branch_matching_ignores_identifier_hyphens() -> None:
    config = authority()
    config["task"]["status"] = "MERGED"
    config["next_task_proposal"] = {"id": "REC-02", "status": "PROPOSED", "repository": "tticom/score2gp"}
    facts = {"snapshot": {"repository": "tticom/score2gp-agentops"}, "pull_request": {"number": 612, "state": "OPEN", "head_branch": "gov/promote-rec02", "head_sha": "a" * 40, "reviews": []}}
    assert resolve_state(config, facts)["state"] == "REVIEW_REQUIRED"


@pytest.mark.parametrize(
    "branch",
    [
        "gov/promote-rec-02",
        "chore/promote-rec-02",
        "codex/promote-rec-02",
        "governance/promote-rec-02",
        "gov/rec-02",
        "chore/rec-02",
    ],
)
def test_promotion_branch_matching_accepts_supported_prefixes(branch: str) -> None:
    config = authority()
    config["task"]["status"] = "MERGED"
    config["next_task_proposal"] = {
        "id": "REC-02",
        "status": "PROPOSED",
        "repository": "tticom/score2gp",
    }
    facts = {
        "snapshot": {"repository": "tticom/score2gp-agentops"},
        "pull_request": {
            "number": 612,
            "state": "OPEN",
            "head_branch": branch,
            "head_sha": "a" * 40,
            "reviews": [],
        },
    }
    assert resolve_state(config, facts)["state"] == "REVIEW_REQUIRED"


def test_promoted_authority_routes_standard_governance_pr_for_review() -> None:
    config = authority()
    config["task"].update({"id": "REC-02", "status": "PROMOTED", "pull_request": None})
    config["next_task_proposal"] = {
        "id": "REC-03",
        "title": "Canonical observations",
        "status": "PROPOSED",
        "repository": "tticom/score2gp",
        "branch": "feat/rec-03-vector-text-observations",
        "owner_role": "implementation",
        "reviewer_role": "reviewer",
        "allowed_paths": ["src/a.py"],
    }
    facts = {
        "snapshot": {"repository": "tticom/score2gp-agentops"},
        "pull_request": {
            "number": 619,
            "state": "OPEN",
            "head_branch": "gov/promote-rec-03",
            "head_sha": "a" * 40,
            "reviews": [],
        },
    }

    resolved = resolve_state(config, facts)

    assert resolved == {
        "schema_version": 1,
        "state": "REVIEW_REQUIRED",
        "reason": "current_head_requires_review",
        "task_id": "REC-03",
        "dispatch_role": "reviewer",
    }
    assignment = build_assignment(
        config,
        facts,
        resolved,
        RuntimeIdentity("tticom", "reviewer"),
        "b" * 40,
    )
    assert assignment["authority"]["task_id"] == "REC-03"
    assert assignment["work"]["pull_request"] == 619
    assert assignment["work"]["branch"] == "gov/promote-rec-03"


def test_control_plane_bootstrap_always_uses_independent_reviewer_role() -> None:
    config = authority()
    config["task"]["status"] = "MERGED"
    config["task"]["reviewer_role"] = "governance"
    facts = {"snapshot": {"repository": "tticom/score2gp-agentops"}, "control_plane_repair": True, "pull_request": {"number": 613, "state": "OPEN", "head_branch": "fix/control-plane-repair", "head_sha": "a" * 40, "reviews": []}}
    assert resolve_state(config, facts)["dispatch_role"] == "reviewer"


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
def test_resolve_state_handles_missing_or_invalid_authority_pull_request(
    invalid_pr: Any, expected_reason: str
) -> None:
    config = authority()
    config["task"]["status"] = "RUNNING"
    config["task"]["pull_request"] = invalid_pr
    facts = live()
    res = resolve_state(config, facts)
    assert res["state"] == "BLOCKED"
    assert res["reason"] == expected_reason


def test_resolve_state_handles_string_integer_pull_request() -> None:
    config = authority()
    config["task"]["status"] = "RUNNING"
    config["task"]["pull_request"] = "441"
    facts = live()
    res = resolve_state(config, facts)
    assert res["state"] == "REVIEW_REQUIRED"


def test_promoted_task_without_pr_resolves_to_ready_with_owner_role() -> None:
    config = authority()
    config["task"]["status"] = "PROMOTED"
    config["task"]["pull_request"] = None
    config["task"]["owner_role"] = "implementation"
    res = resolve_state(config, {})
    assert res["state"] == "READY"
    assert res["reason"] == "authorised_task_without_pr"
    assert res["dispatch_role"] == "implementation"


def test_promotion_pr_reconciliation_transition_resolves_correctly() -> None:
    config = authority()
    config["task"]["status"] = "MERGED"
    config["next_task_proposal"] = {
        "id": "REC-03",
        "status": "PROPOSED",
        "repository": "tticom/score2gp",
        "branch": "feat/rec-03-vector-text-observations",
        "owner_role": "implementation",
        "reviewer_role": "reviewer",
    }
    # Live PR on agentops promoting REC-03
    facts = {
        "snapshot": {"repository": "tticom/score2gp-agentops"},
        "pull_request": {
            "number": 619,
            "state": "OPEN",
            "head_branch": "gov/promote-rec-03",
            "head_sha": "a" * 40,
            "reviews": [],
        },
    }
    res_no_review = resolve_state(config, facts)
    assert res_no_review["state"] == "REVIEW_REQUIRED"
    assert res_no_review["dispatch_role"] == "reviewer"

    # With changes requested
    facts_changes = deepcopy(facts)
    facts_changes["pull_request"]["reviews"] = [
        {"author": "reviewer", "state": "CHANGES_REQUESTED", "head_sha": "a" * 40}
    ]
    res_changes = resolve_state(config, facts_changes)
    assert res_changes["state"] == "RUNNING"
    assert res_changes["dispatch_role"] == "implementation"

    # With approval
    facts_approved = deepcopy(facts)
    facts_approved["pull_request"]["reviews"] = [
        {"author": "reviewer", "state": "APPROVED", "head_sha": "a" * 40}
    ]
    res_approved = resolve_state(config, facts_approved)
    assert res_approved["state"] == "GOVERNANCE_REQUIRED"
    assert res_approved["dispatch_role"] == "governance"


def test_governance_pr_reconciling_completed_task_resolves_with_advanced_authority() -> None:
    # Checked-in authority on PR 619: active task is REC-04 PROMOTED, proposal is REC-05,
    # completed_tasks includes REC-03 MERGED.
    config = authority()
    config["task"] = {
        "id": "REC-04",
        "title": "Local Scale Model",
        "status": "PROMOTED",
        "repository": "tticom/score2gp",
        "branch": "feat/rec-04-local-scale-model",
        "pull_request": None,
        "owner_role": "implementation",
        "allowed_paths": ["src/score2gp/recognition/scale.py"],
    }
    config["next_task_proposal"] = {
        "id": "REC-05",
        "status": "PROPOSED",
        "repository": "tticom/score2gp",
        "branch": "feat/rec-05-raster-observation-adapter",
        "owner_role": "implementation",
        "reviewer_role": "reviewer",
    }
    config["completed_tasks"] = [
        {
            "id": "REC-03",
            "title": "Canonical Vector and Text Observations",
            "status": "MERGED",
            "repository": "tticom/score2gp",
            "branch": "feat/rec-03-vector-text-observations",
            "pull_request": 458,
            "owner_role": "implementation",
            "reviewer_role": "reviewer",
        }
    ]
    # Live governance PR #619 on score2gp-agentops (branch gov/promote-rec-03)
    facts = {
        "snapshot": {"repository": "tticom/score2gp-agentops"},
        "pull_request": {
            "number": 619,
            "state": "OPEN",
            "head_branch": "gov/promote-rec-03",
            "head_sha": "a" * 40,
            "reviews": [
                {"author": "reviewer", "state": "CHANGES_REQUESTED", "head_sha": "a" * 40}
            ],
        },
    }
    res = resolve_state(config, facts)
    assert res["state"] == "RUNNING"
    assert res["reason"] == "current_head_changes_requested"
    assert res["task_id"] == "REC-03"
    assert res["dispatch_role"] == "implementation"
    assign_running = build_assignment(config, facts, res, RuntimeIdentity("tticom", "worker"), "a" * 40)
    assert assign_running["work"]["pull_request"] == 619
    assert assign_running["work"]["branch"] == "gov/promote-rec-03"
    assert assign_running["authority"]["task_id"] == "REC-03"
    assert assign_running["worker"]["role"] == "implementation"

    # When approved
    facts_approved = deepcopy(facts)
    facts_approved["pull_request"]["reviews"] = [
        {"author": "reviewer", "state": "APPROVED", "head_sha": "a" * 40}
    ]
    res_approved = resolve_state(config, facts_approved)
    assert res_approved["state"] == "GOVERNANCE_REQUIRED"
    assert res_approved["reason"] == "current_head_review_approved"
    assert res_approved["task_id"] == "REC-03"
    assert res_approved["dispatch_role"] == "governance"
    assign_approved = build_assignment(config, facts_approved, res_approved, RuntimeIdentity("tticom", "governor"), "a" * 40)
    assert assign_approved["work"]["pull_request"] == 619
    assert assign_approved["work"]["branch"] == "gov/promote-rec-03"
    assert assign_approved["authority"]["task_id"] == "REC-03"
    assert assign_approved["worker"]["role"] == "governance"

    # When review required
    facts_no_review = deepcopy(facts)
    facts_no_review["pull_request"]["reviews"] = []
    res_no_review = resolve_state(config, facts_no_review)
    assert res_no_review["state"] == "REVIEW_REQUIRED"
    assert res_no_review["reason"] == "current_head_requires_review"
    assert res_no_review["task_id"] == "REC-03"
    assert res_no_review["dispatch_role"] == "reviewer"
    assign_review = build_assignment(config, facts_no_review, res_no_review, RuntimeIdentity("tticom", "reviewer"), "a" * 40)
    assert assign_review["work"]["pull_request"] == 619
    assert assign_review["work"]["branch"] == "gov/promote-rec-03"
    assert assign_review["authority"]["task_id"] == "REC-03"
    assert assign_review["worker"]["role"] == "reviewer"


def test_build_assignment_with_checked_in_authority_and_authorized_reviewer_identity() -> None:
    import json
    from pathlib import Path
    auth_file = Path(__file__).resolve().parent.parent / "projects" / "score2gp" / "ORCHESTRATION_STATE.json"
    auth_data = json.loads(auth_file.read_text(encoding="utf-8"))

    live_facts = {
        "snapshot": {"repository": "tticom/score2gp-agentops"},
        "pull_request": {
            "number": 619,
            "state": "OPEN",
            "head_branch": "gov/promote-rec-03",
            "head_sha": "a" * 40,
            "reviews": [],
        },
    }
    resolved = resolve_state(auth_data, live_facts)
    assert resolved["state"] == "REVIEW_REQUIRED"
    assert resolved["dispatch_role"] == "reviewer"
    assert resolved["task_id"] == "REC-03"

    assignment = build_assignment(
        auth_data,
        live_facts,
        resolved,
        RuntimeIdentity("tticom", "tticom-codex"),
        "a" * 40,
    )
    assert assignment["work"]["pull_request"] == 619
    assert assignment["work"]["branch"] == "gov/promote-rec-03"
    assert assignment["authority"]["task_id"] == "REC-03"
    assert assignment["worker"]["role"] == "reviewer"
    assert assignment["worker"]["github_login"] == "tticom-codex"


def schema2_authority(status: str = "RUNNING") -> dict:
    return {
        "schema_version": 2,
        "authority_revision": 5,
        "task": {
            "id": "108",
            "title": "Bounded repair",
            "objective": "Apply the bounded repair.",
            "status": status,
            "repository": "tticom/score2gp",
            "base_branch": "main",
            "branch": "feat/task-108",
            "pull_request": 441,
            "owner_role": "implementation",
            "prompt": "prompt.md",
            "allowed_paths": ["src/a.py", "tests/test_a.py"],
            "acceptance": ["prove repair"],
            "validation_commands": ["python3 -m pytest"],
            "dependencies": [],
            "stop_conditions": [],
            "reviewer_role": "reviewer",
            "delivery_action": "pull_request",
        },
        "next_task_proposal": {
            "id": "109",
            "title": "Next step",
            "objective": "Apply next step.",
            "status": "PROPOSED",
            "repository": "tticom/score2gp",
            "base_branch": "main",
            "branch": "feat/task-109",
            "pull_request": None,
            "owner_role": "implementation",
            "prompt": "prompt-109.md",
            "allowed_paths": ["src/b.py"],
            "acceptance": ["prove next step"],
            "validation_commands": ["python3 -m pytest"],
            "dependencies": ["108"],
            "stop_conditions": [],
            "reviewer_role": "reviewer",
            "delivery_action": "pull_request",
        },
        "incidents": [],
        "roles": {
            "implementation": {
                "github_logins": ["worker"],
                "allowed_actions": ["edit", "test"],
                "forbidden_actions": ["merge"],
            },
        },
        "merge_policy": {
            "required_checks": ["test"],
            "minimum_approvals": 1,
            "require_governance_go": True,
            "require_reviewed_head": True,
            "require_resolved_threads": True,
            "allow_admin_bypass": False,
        },
    }


def live_merged_orca(
    *,
    head_sha: str = "a" * 40,
    merge_commit: str = "b" * 40,
    pr_number: int = 441,
    branch: str = "feat/task-108",
    repo: str = "tticom/score2gp",
) -> dict:
    return {
        "snapshot": {"repository": repo},
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


def test_reconcile_post_merge_updates_authority_and_active_task_view(tmp_path: Path) -> None:
    auth = schema2_authority("RUNNING")
    authority_path = tmp_path / "ORCHESTRATION_STATE.json"
    active_task_path = tmp_path / "ACTIVE_TASK.md"

    from scripts.score2gp_orchestrator import render_active_task
    authority_path.write_text(json.dumps(auth, indent=2) + "\n", encoding="utf-8")
    active_task_path.write_text(render_active_task(auth), encoding="utf-8")

    facts = live_merged_orca(head_sha="1" * 40, merge_commit="2" * 40)
    res = reconcile_post_merge(auth, facts, authority_path, active_task_path)

    assert res["reconciled"] is True
    assert res["status"] == "MERGED"
    assert res["task_id"] == "108"
    assert res["head_sha"] == "1" * 40
    assert res["merge_commit"] == "2" * 40

    saved_auth = json.loads(authority_path.read_text(encoding="utf-8"))
    assert saved_auth["task"]["status"] == "MERGED"
    assert len(saved_auth["completed_tasks"]) == 1
    completed = saved_auth["completed_tasks"][0]
    assert completed["id"] == "108"
    assert completed["status"] == "MERGED"
    assert completed["head_sha"] == "1" * 40
    assert completed["merge_commit"] == "2" * 40
    assert completed["allowed_paths"] == ["src/a.py", "tests/test_a.py"]
    assert saved_auth["next_task_proposal"]["status"] == "PROPOSED"

    saved_active = active_task_path.read_text(encoding="utf-8")
    assert "**Status**: MERGED" in saved_active
    assert "**Status**: APPROVED" not in saved_active
    assert "**Status**: PROMOTED" not in saved_active

    validate_legacy_alignment(saved_auth, saved_active)


def test_reconcile_dry_run_leaves_files_byte_for_byte_unchanged(tmp_path: Path) -> None:
    auth = schema2_authority("RUNNING")
    authority_path = tmp_path / "ORCHESTRATION_STATE.json"
    active_task_path = tmp_path / "ACTIVE_TASK.md"

    from scripts.score2gp_orchestrator import render_active_task
    authority_path.write_text(json.dumps(auth, indent=2) + "\n", encoding="utf-8")
    active_task_path.write_text(render_active_task(auth), encoding="utf-8")

    auth_bytes = authority_path.read_bytes()
    active_bytes = active_task_path.read_bytes()

    facts = live_merged_orca()
    res = reconcile_post_merge(auth, facts, authority_path, active_task_path, dry_run=True)

    assert res["dry_run"] is True
    assert res["reconciled"] is True
    assert authority_path.read_bytes() == auth_bytes
    assert active_task_path.read_bytes() == active_bytes


@pytest.mark.parametrize("mutator,match_err", [
    (lambda l: l["pull_request"].update(state="OPEN"), "expected 'MERGED'"),
    (lambda l: l["pull_request"].update(state="CLOSED"), "expected 'MERGED'"),
    (lambda l: l["pull_request"].update(number=999), "PR number mismatch"),
    (lambda l: l["pull_request"].update(head_branch="wrong"), "branch mismatch"),
    (lambda l: l["pull_request"].update(head_sha="short"), "invalid or missing product head SHA"),
    (lambda l: l["pull_request"].update(head_sha="z" * 40), "invalid or missing product head SHA"),
    (lambda l: l["pull_request"].update(head_sha=None), "invalid or missing product head SHA"),
    (lambda l: l["pull_request"].pop("merge_commit"), "invalid or missing merge commit SHA"),
    (lambda l: l["pull_request"].update(merge_commit="invalid"), "invalid or missing merge commit SHA"),
    (lambda l: l["pull_request"].update(merge_commit=None), "invalid or missing merge commit SHA"),
    (lambda l: l.pop("pull_request"), "live pull_request missing or invalid"),
    (lambda l: (l.pop("snapshot", None), l.pop("repository", None)), "missing repository in live state"),
    (lambda l: l.update(snapshot={"repository": "wrong/repo"}), "repository mismatch"),
    (lambda l: l.update(task_id="wrong-task"), "task ID mismatch"),
    (lambda l: l.update(expected_task_id="wrong-task"), "task ID mismatch"),
    (lambda l: l.update(expected_branch="wrong"), "branch mismatch"),
    (lambda l: l.update(expected_pull_request=999), "PR number mismatch"),
    (lambda l: l.update(governance={"reviewed_head_sha": "b" * 40}), "does not match reviewed head"),
    (lambda l: l.update(expected_head_sha="b" * 40), "does not match expected head"),
    (lambda l: l.update(expected_head_sha=""), "does not match expected head"),
    (lambda l: l.update(expected_merge_commit="c" * 40), "does not match expected merge commit"),
    (lambda l: l.update(expected_merge_commit=""), "does not match expected merge commit"),
])
def test_reconcile_fails_closed_and_leaves_files_byte_for_byte_unchanged(
    tmp_path: Path, mutator: Any, match_err: str
) -> None:
    auth = schema2_authority("RUNNING")
    authority_path = tmp_path / "ORCHESTRATION_STATE.json"
    active_task_path = tmp_path / "ACTIVE_TASK.md"

    from scripts.score2gp_orchestrator import render_active_task
    authority_path.write_text(json.dumps(auth, indent=2) + "\n", encoding="utf-8")
    active_task_path.write_text(render_active_task(auth), encoding="utf-8")

    auth_bytes = authority_path.read_bytes()
    active_bytes = active_task_path.read_bytes()

    facts = live_merged_orca()
    mutator(facts)

    with pytest.raises(ControlError, match=match_err):
        reconcile_post_merge(auth, facts, authority_path, active_task_path)

    assert authority_path.read_bytes() == auth_bytes
    assert active_task_path.read_bytes() == active_bytes


def test_reconcile_cli_command_success_and_idempotent_replay(tmp_path: Path) -> None:
    auth = schema2_authority("RUNNING")
    authority_path = tmp_path / "ORCHESTRATION_STATE.json"
    active_task_path = tmp_path / "ACTIVE_TASK.md"
    live_path = tmp_path / "live.json"

    from scripts.score2gp_orchestrator import render_active_task
    authority_path.write_text(json.dumps(auth, indent=2) + "\n", encoding="utf-8")
    active_task_path.write_text(render_active_task(auth), encoding="utf-8")
    live_path.write_text(json.dumps(live_merged_orca()), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/score2gp_orca_control.py",
            "reconcile",
            "--authority",
            str(authority_path),
            "--live",
            str(live_path),
        ],
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    first_result = json.loads(completed.stdout)
    assert first_result["reconciled"] is True
    assert first_result["status"] == "MERGED"

    saved_auth = json.loads(authority_path.read_text(encoding="utf-8"))
    assert len(saved_auth["completed_tasks"]) == 1
    assert saved_auth["task"]["status"] == "MERGED"

    # Replaying the exact same merge must be idempotent without writes or duplicate
    completed2 = subprocess.run(
        [
            sys.executable,
            "scripts/score2gp_orca_control.py",
            "reconcile",
            "--authority",
            str(authority_path),
            "--live",
            str(live_path),
        ],
        capture_output=True,
        text=True,
    )
    assert completed2.returncode == 0, completed2.stderr
    second_result = json.loads(completed2.stdout)
    assert second_result["reconciled"] is False
    assert second_result["idempotent"] is True

    saved_auth_second = json.loads(authority_path.read_text(encoding="utf-8"))
    assert len(saved_auth_second["completed_tasks"]) == 1


def test_reconcile_cli_command_dry_run(tmp_path: Path) -> None:
    auth = schema2_authority("RUNNING")
    authority_path = tmp_path / "ORCHESTRATION_STATE.json"
    active_task_path = tmp_path / "ACTIVE_TASK.md"
    live_path = tmp_path / "live.json"

    from scripts.score2gp_orchestrator import render_active_task
    authority_path.write_text(json.dumps(auth, indent=2) + "\n", encoding="utf-8")
    active_task_path.write_text(render_active_task(auth), encoding="utf-8")
    live_path.write_text(json.dumps(live_merged_orca()), encoding="utf-8")

    auth_bytes = authority_path.read_bytes()
    active_bytes = active_task_path.read_bytes()

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/score2gp_orca_control.py",
            "reconcile",
            "--authority",
            str(authority_path),
            "--live",
            str(live_path),
            "--dry-run",
        ],
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    res = json.loads(completed.stdout)
    assert res["dry_run"] is True
    assert res["reconciled"] is True
    assert authority_path.read_bytes() == auth_bytes
    assert active_task_path.read_bytes() == active_bytes


def test_capture_live_state_normalizes_merge_commit(monkeypatch) -> None:
    responses = iter([
        {
            "number": 441,
            "state": "MERGED",
            "headRefName": "feat/task-108",
            "headRefOid": "a" * 40,
            "baseRefName": "main",
            "author": {"login": "worker"},
            "reviews": [],
            "statusCheckRollup": [{"name": "test", "conclusion": "SUCCESS"}],
            "mergeCommit": {"oid": "b" * 40},
        },
        {"data": {"repository": {"pullRequest": {"reviewThreads": {"nodes": [], "pageInfo": {"hasNextPage": False, "endCursor": None}}}}}},
        [{"id": 7, "enforcement": "active"}],
        {"id": 7, "current_user_can_bypass": "never"},
    ])
    monkeypatch.setattr("scripts.score2gp_orca_control.run_json", lambda command: next(responses))
    snapshot = capture_live_state("tticom/score2gp", 441)
    assert snapshot["pull_request"]["state"] == "MERGED"
    assert snapshot["pull_request"]["merge_commit"] == "b" * 40
    assert snapshot["pull_request"]["head_sha"] == "a" * 40


def test_resolve_state_merged_pr_requires_governance_reconciliation() -> None:
    config = schema2_authority("RUNNING")
    facts = live_merged_orca()
    res = resolve_state(config, facts)
    assert res["state"] == "GOVERNANCE_REQUIRED"
    assert res["reason"] == "merge_requires_governance_reconciliation"
    assert res["dispatch_role"] == "governance"
    assert res["task_id"] == "108"


def test_build_assignment_governance_reconciliation() -> None:
    config = schema2_authority("RUNNING")
    config["roles"]["governance"] = {
        "github_logins": ["gov-worker"],
        "allowed_actions": ["reconcile"],
        "forbidden_actions": ["merge"],
    }
    facts = live_merged_orca()
    resolved = resolve_state(config, facts)
    assignment = build_assignment(
        config,
        facts,
        resolved,
        RuntimeIdentity("agent", "gov-worker"),
        "a" * 40,
    )
    assert assignment["worker"]["role"] == "governance"
    assert assignment["authority"]["reason"] == "merge_requires_governance_reconciliation"
    assert assignment["completion_contract"]["may_merge"] is False
    assert assignment["completion_contract"]["may_select_next_task"] is False


def test_reconcile_cli_with_custom_active_task_path(tmp_path: Path) -> None:
    auth = schema2_authority("RUNNING")
    authority_path = tmp_path / "ORCHESTRATION_STATE.json"
    custom_active_path = tmp_path / "CUSTOM_ACTIVE.md"
    live_path = tmp_path / "live.json"

    from scripts.score2gp_orchestrator import render_active_task
    authority_path.write_text(json.dumps(auth, indent=2) + "\n", encoding="utf-8")
    custom_active_path.write_text(render_active_task(auth), encoding="utf-8")
    live_path.write_text(json.dumps(live_merged_orca()), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/score2gp_orca_control.py",
            "reconcile",
            "--authority",
            str(authority_path),
            "--live",
            str(live_path),
            "--active-task",
            str(custom_active_path),
        ],
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    res = json.loads(completed.stdout)
    assert res["reconciled"] is True
    assert "**Status**: MERGED" in custom_active_path.read_text(encoding="utf-8")


def test_reconcile_post_merge_picks_correct_task_when_multiple_completed(tmp_path: Path) -> None:
    auth = schema2_authority("RUNNING")
    auth["completed_tasks"] = [
        {"id": "099", "status": "MERGED", "head_sha": "9" * 40, "merge_commit": "8" * 40}
    ]
    authority_path = tmp_path / "ORCHESTRATION_STATE.json"
    active_task_path = tmp_path / "ACTIVE_TASK.md"

    from scripts.score2gp_orchestrator import render_active_task
    authority_path.write_text(json.dumps(auth, indent=2) + "\n", encoding="utf-8")
    active_task_path.write_text(render_active_task(auth), encoding="utf-8")

    facts = live_merged_orca(head_sha="1" * 40, merge_commit="2" * 40)
    res = reconcile_post_merge(auth, facts, authority_path, active_task_path)

    assert res["task_id"] == "108"
    assert res["head_sha"] == "1" * 40
    assert res["merge_commit"] == "2" * 40
    assert len(res["completed_tasks"]) == 2
    assert res["completed_tasks"][0]["id"] == "108"
    assert res["completed_tasks"][1]["id"] == "099"


def test_reconcile_fails_when_existing_active_task_is_split_brain(tmp_path: Path) -> None:
    auth = schema2_authority("RUNNING")
    authority_path = tmp_path / "ORCHESTRATION_STATE.json"
    active_task_path = tmp_path / "ACTIVE_TASK.md"

    authority_path.write_text(json.dumps(auth, indent=2) + "\n", encoding="utf-8")
    # Divergent active task file
    active_task_path.write_text(
        "# Active Task\n**Task**: WRONG-999\n**Status**: IN_PROGRESS\n**Repository**: tticom/score2gp\n**PR Branch**: `feat/wrong`\n",
        encoding="utf-8",
    )

    auth_bytes = authority_path.read_bytes()
    active_bytes = active_task_path.read_bytes()

    facts = live_merged_orca()
    with pytest.raises(ControlError, match="ACTIVE_TASK.md diverges from orchestration authority"):
        reconcile_post_merge(auth, facts, authority_path, active_task_path)

    assert authority_path.read_bytes() == auth_bytes
    assert active_task_path.read_bytes() == active_bytes


def test_reconcile_cli_with_repo_and_pull_request_args(tmp_path: Path, monkeypatch) -> None:
    auth = schema2_authority("RUNNING")
    authority_path = tmp_path / "ORCHESTRATION_STATE.json"
    active_task_path = tmp_path / "ACTIVE_TASK.md"

    from scripts.score2gp_orchestrator import render_active_task
    authority_path.write_text(json.dumps(auth, indent=2) + "\n", encoding="utf-8")
    active_task_path.write_text(render_active_task(auth), encoding="utf-8")

    captured_facts = live_merged_orca()

    import scripts.score2gp_orca_control as orca_ctrl
    monkeypatch.setattr(orca_ctrl, "capture_live_state", lambda repo, pr: captured_facts)

    # Use python CLI invocation with monkeypatch by invoking main with sys.argv
    test_argv = [
        "score2gp_orca_control.py",
        "reconcile",
        "--authority",
        str(authority_path),
        "--repository",
        "tticom/score2gp",
        "--pull-request",
        "441",
    ]
    monkeypatch.setattr(sys, "argv", test_argv)

    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        orca_ctrl.main()

    res = json.loads(buf.getvalue())
    assert res["reconciled"] is True
    assert res["status"] == "MERGED"
    saved = json.loads(authority_path.read_text(encoding="utf-8"))
    assert saved["task"]["status"] == "MERGED"


def test_verify_merge_gate_handles_non_dict_governance_and_protection() -> None:
    facts = merge_ready()
    facts["governance"] = "invalid"
    facts["protection"] = "invalid"
    decision = verify_merge_gate(authority(), facts)
    assert decision["decision"] == "DENY"
    assert "governance_go_missing" in decision["failures"]
    assert "active_main_ruleset_missing" in decision["failures"]
