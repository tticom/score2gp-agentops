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
    reconcile_task,
    resolve_state,
    validate_assignment,
    validate_authority,
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
                "github_logins": ["reviewer", "reviewer-a", "reviewer-b"],
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
            "base_branch": "main",
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


def test_completed_legacy_active_task_alignment_passes() -> None:
    text = """# Active Task
**Task**: 108 — Bounded repair
**Status**: COMPLETED
**Repository**: tticom/score2gp
**PR Branch**: `feat/task-108`
**Pull Request**: 441
"""
    auth = authority()
    auth["task"]["status"] = "COMPLETED"
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


def test_explicit_review_allows_unrelated_open_pr() -> None:
    config = authority()
    facts = {
        "snapshot": {"repository": "tticom/score2gp-agentops"},
        "explicit_review": True,
        "pull_request": {
            "number": 667,
            "state": "OPEN",
            "head_branch": "chore/prepare-first-agy-cycle",
            "head_sha": "a" * 40,
            "author": "tticom-codex",
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
        RuntimeIdentity("tticom-automation", "reviewer"),
        "b" * 40,
    )
    assert assignment["work"]["pull_request"] == 667
    assert assignment["work"]["branch"] == "chore/prepare-first-agy-cycle"


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


def test_gov_can_review_product_pr_460() -> None:
    auth_file = Path(__file__).resolve().parent.parent / "projects" / "score2gp" / "ORCHESTRATION_STATE.json"
    auth_data = json.loads(auth_file.read_text(encoding="utf-8"))

    live_facts = {
        "snapshot": {"repository": "tticom/score2gp"},
        "pull_request": {
            "number": 460,
            "state": "OPEN",
            "head_branch": "feat/rec-05-raster-observation-adapter",
            "head_sha": "27216115bdc0192ab90bc74f226b8c7d835ccf41",
            "author": "tticom-automation",
            "reviews": [],
        },
    }
    resolved = resolve_state(auth_data, live_facts)
    assert resolved["state"] == "REVIEW_REQUIRED"
    assert resolved["dispatch_role"] == "reviewer"
    assert resolved["task_id"] == "REC-05"

    assignment = build_assignment(
        auth_data,
        live_facts,
        resolved,
        RuntimeIdentity("tticom-gov", "tticomgov-code"),
        "a" * 40,
    )
    assert assignment["work"]["pull_request"] == 460
    assert assignment["work"]["branch"] == "feat/rec-05-raster-observation-adapter"
    assert assignment["authority"]["task_id"] == "REC-05"
    assert assignment["worker"]["role"] == "reviewer"
    assert assignment["worker"]["github_login"] == "tticomgov-code"
    assert assignment["work"]["allowed_paths"] == []
    assert assignment["completion_contract"]["may_merge"] is False


def test_automation_cannot_review_own_pr_460() -> None:
    auth_file = Path(__file__).resolve().parent.parent / "projects" / "score2gp" / "ORCHESTRATION_STATE.json"
    auth_data = json.loads(auth_file.read_text(encoding="utf-8"))

    live_facts = {
        "snapshot": {"repository": "tticom/score2gp"},
        "pull_request": {
            "number": 460,
            "state": "OPEN",
            "head_branch": "feat/rec-05-raster-observation-adapter",
            "head_sha": "27216115bdc0192ab90bc74f226b8c7d835ccf41",
            "author": "tticom-automation",
            "reviews": [],
        },
    }
    resolved = resolve_state(auth_data, live_facts)
    with pytest.raises(ControlError, match="self-review is forbidden"):
        build_assignment(
            auth_data,
            live_facts,
            resolved,
            RuntimeIdentity("tticom-automation", "tticom-automation"),
            "a" * 40,
        )


def test_automation_can_review_gov_authored_governance_pr() -> None:
    auth_file = Path(__file__).resolve().parent.parent / "projects" / "score2gp" / "ORCHESTRATION_STATE.json"
    auth_data = json.loads(auth_file.read_text(encoding="utf-8"))

    live_facts = {
        "snapshot": {"repository": "tticom/score2gp-agentops"},
        "pull_request": {
            "number": 619,
            "state": "OPEN",
            "head_branch": "gov/promote-rec-03",
            "head_sha": "a" * 40,
            "author": "tticomgov-code",
            "reviews": [],
        },
    }
    resolved = resolve_state(auth_data, live_facts)
    assert resolved["state"] == "REVIEW_REQUIRED"
    assert resolved["dispatch_role"] == "reviewer"

    assignment = build_assignment(
        auth_data,
        live_facts,
        resolved,
        RuntimeIdentity("tticom-automation", "tticom-automation"),
        "a" * 40,
    )
    assert assignment["work"]["pull_request"] == 619
    assert assignment["worker"]["role"] == "reviewer"
    assert assignment["worker"]["github_login"] == "tticom-automation"
    assert assignment["work"]["allowed_paths"] == []
    assert assignment["completion_contract"]["may_merge"] is False


def test_gov_cannot_review_own_governance_pr() -> None:
    auth_file = Path(__file__).resolve().parent.parent / "projects" / "score2gp" / "ORCHESTRATION_STATE.json"
    auth_data = json.loads(auth_file.read_text(encoding="utf-8"))

    live_facts = {
        "snapshot": {"repository": "tticom/score2gp-agentops"},
        "pull_request": {
            "number": 619,
            "state": "OPEN",
            "head_branch": "gov/promote-rec-03",
            "head_sha": "a" * 40,
            "author": "tticomgov-code",
            "reviews": [],
        },
    }
    resolved = resolve_state(auth_data, live_facts)
    with pytest.raises(ControlError, match="self-review is forbidden"):
        build_assignment(
            auth_data,
            live_facts,
            resolved,
            RuntimeIdentity("tticom-gov", "tticomgov-code"),
            "a" * 40,
        )


def test_cross_task_branch_reuse_in_authority_fails_closed() -> None:
    config = authority()
    config["task_registry"] = {
        "OTHER-01": {
            "id": "OTHER-01",
            "status": "RUNNING",
            "branch": "feat/task-108",
        }
    }
    with pytest.raises(ControlError, match="cross-task branch reuse detected"):
        validate_authority(config)


def test_reconcile_task_success_and_idempotence() -> None:
    config = authority()
    config["task"]["status"] = "MERGED"
    config["next_task_proposal"] = {
        "id": "TASK-109",
        "status": "PROPOSED",
    }
    head = "c" * 40
    merge_sha = "d" * 40
    live_facts = {
        "pull_request": {
            "number": 441,
            "state": "MERGED",
            "head_branch": "feat/task-108",
            "head_sha": head,
            "merge_commit": merge_sha,
        }
    }
    # Initial reconciliation
    res = reconcile_task(config, live_facts)
    assert res["status"] == "RECONCILED"
    assert res["idempotent"] is False
    assert res["task_id"] == "108"
    new_auth = res["authority"]
    assert new_auth["task"]["status"] == "COMPLETED"
    assert new_auth["task"]["reconciled"] is True
    assert new_auth["task"]["merge_commit"] == merge_sha
    assert new_auth["task"]["head_sha"] == head
    assert new_auth["next_task_proposal"]["status"] == "PROPOSED"
    completed = new_auth.get("completed_tasks", [])
    assert any(c["id"] == "108" for c in completed)

    # Replay reconciliation (idempotent)
    replay = reconcile_task(new_auth, live_facts)
    assert replay["status"] == "ALREADY_RECONCILED"
    assert replay["idempotent"] is True
    assert replay["task_id"] == "108"
    matching = [c for c in replay["authority"]["completed_tasks"] if c["id"] == "108"]
    assert len(matching) == 1
    assert replay["authority"]["next_task_proposal"]["status"] == "PROPOSED"


def test_reconcile_task_fails_closed_on_unmerged_or_mismatched_pr() -> None:
    config = authority()
    head = "c" * 40
    merge_sha = "d" * 40

    # PR is OPEN, not MERGED
    open_facts = {
        "pull_request": {
            "number": 441,
            "state": "OPEN",
            "head_branch": "feat/task-108",
            "head_sha": head,
            "merge_commit": merge_sha,
        }
    }
    with pytest.raises(ControlError, match="reconciliation requires a MERGED pull request"):
        reconcile_task(config, open_facts)

    # Branch mismatch
    bad_branch_facts = {
        "pull_request": {
            "number": 441,
            "state": "MERGED",
            "head_branch": "feat/wrong-branch",
            "head_sha": head,
            "merge_commit": merge_sha,
        }
    }
    with pytest.raises(ControlError, match="branch mismatch"):
        reconcile_task(config, bad_branch_facts)

    # Invalid merge commit SHA
    bad_sha_facts = {
        "pull_request": {
            "number": 441,
            "state": "MERGED",
            "head_branch": "feat/task-108",
            "head_sha": head,
            "merge_commit": "short",
        }
    }
    with pytest.raises(ControlError, match="reconciliation requires a 40-character merge_commit"):
        reconcile_task(config, bad_sha_facts)


# --- GOV-01: sanctioned merge executor, per-repository checks, governance PRs, receipt audit ---

from scripts.score2gp_orca_control import (  # noqa: E402
    AGENTOPS_REPOSITORY,
    audit_merge_receipts,
    derive_governance_go,
    execute_merge,
    format_merge_receipt,
    parse_merge_receipts,
    required_checks_for,
)

HEAD = "a" * 40
MERGE_COMMIT = "m" * 40


def executor_authority() -> dict:
    config = authority()
    config["merge_policy"]["minimum_approvals"] = 1
    config["merge_policy"]["required_checks_by_repository"] = {
        "tticom/score2gp": ["test"],
        AGENTOPS_REPOSITORY: ["deterministic-control-plane"],
    }
    config["roles"]["merge_controller"]["github_logins"] = ["merge-app"]
    return config


def open_pr(repository: str = "tticom/score2gp", branch: str = "feat/task-108", author: str = "worker") -> dict:
    check = "test" if repository == "tticom/score2gp" else "deterministic-control-plane"
    return {
        "snapshot": {"repository": repository},
        "pull_request": {
            "number": 441,
            "state": "OPEN",
            "head_branch": branch,
            "base_branch": "main",
            "head_sha": HEAD,
            "author": author,
            "reviews": [{"author": "reviewer-a", "state": "APPROVED", "head_sha": HEAD}],
            "checks": [{"name": check, "conclusion": "SUCCESS"}],
            "unresolved_threads": 0,
            "merge_commit": "",
        },
        "protection": {"active_rulesets": 1, "current_user_can_bypass": False},
        "admin_bypass": False,
    }


def gated(facts: dict, login: str = "merge-app", config: dict | None = None) -> dict:
    facts = deepcopy(facts)
    facts["governance"] = derive_governance_go(config or executor_authority(), facts)
    facts["merge_controller_login"] = login
    return facts


def test_executor_gate_allows_a_non_author_exact_head_approval() -> None:
    decision = verify_merge_gate(executor_authority(), gated(open_pr()))
    assert decision["decision"] == "ALLOW", decision["failures"]


def test_required_checks_are_per_repository() -> None:
    config = executor_authority()
    assert required_checks_for(config["merge_policy"], AGENTOPS_REPOSITORY) == ["deterministic-control-plane"]
    assert required_checks_for(config["merge_policy"], "tticom/score2gp") == ["test"]
    assert required_checks_for(authority()["merge_policy"], AGENTOPS_REPOSITORY) == ["test"]
    facts = gated(open_pr(AGENTOPS_REPOSITORY, "governance/promote-x"))
    decision = verify_merge_gate(config, facts)
    assert decision["decision"] == "ALLOW", decision["failures"]
    assert "required_check_not_success:test" not in decision["failures"]
    facts["pull_request"]["checks"] = []
    assert "required_check_not_success:deterministic-control-plane" in verify_merge_gate(config, facts)["failures"]


def test_governance_pr_skips_only_the_task_branch_match() -> None:
    decision = verify_merge_gate(executor_authority(), gated(open_pr(AGENTOPS_REPOSITORY, "architect/propose-y")))
    assert decision["decision"] == "ALLOW", decision["failures"]
    assert decision["governance_pr"] is True
    # The same branch prefix in the product repository gets no governance path.
    product = verify_merge_gate(executor_authority(), gated(open_pr("tticom/score2gp", "governance/promote-x")))
    assert "branch_mismatch" in product["failures"]


@pytest.mark.parametrize(
    ("mutation", "failure"),
    [
        (lambda x: x["pull_request"].update(reviews=[]), "insufficient_independent_approvals"),
        (lambda x: x["pull_request"]["checks"].clear(), "required_check_not_success:deterministic-control-plane"),
        (lambda x: x["pull_request"].update(unresolved_threads=2), "unresolved_review_threads"),
        (lambda x: x["pull_request"]["reviews"].append(
            {"author": "reviewer-b", "state": "CHANGES_REQUESTED", "head_sha": HEAD}), "current_head_not_approved"),
    ],
)
def test_governance_pr_path_keeps_approval_check_and_thread_requirements(mutation, failure) -> None:
    facts = open_pr(AGENTOPS_REPOSITORY, "governance/promote-x")
    mutation(facts)
    assert failure in verify_merge_gate(executor_authority(), gated(facts))["failures"]


def test_repository_mismatch_is_denied_for_task_prs() -> None:
    facts = gated(open_pr("tticom/other-repo"))
    assert "repository_mismatch" in verify_merge_gate(executor_authority(), facts)["failures"]


def test_author_and_non_reviewer_approvals_do_not_count() -> None:
    facts = open_pr(author="worker")
    facts["pull_request"]["reviews"] = [
        {"author": "worker", "state": "APPROVED", "head_sha": HEAD},
        {"author": "outsider", "state": "APPROVED", "head_sha": HEAD},
    ]
    decision = verify_merge_gate(executor_authority(), gated(facts))
    assert "insufficient_independent_approvals" in decision["failures"]
    assert "governance_go_missing" in decision["failures"]


def test_self_authored_pr_cannot_be_merged_by_its_author() -> None:
    config = executor_authority()
    facts = gated(open_pr(author="merge-app"), login="merge-app", config=config)
    assert "merge_controller_is_pr_author" in verify_merge_gate(config, facts)["failures"]


def test_governance_go_requires_a_current_non_author_approval() -> None:
    config = executor_authority()
    assert derive_governance_go(config, open_pr()) == {"decision": "GO", "reviewed_head_sha": HEAD}
    stale = open_pr()
    stale["pull_request"]["reviews"][0]["head_sha"] = "b" * 40
    assert derive_governance_go(config, stale)["decision"] == "NO_GO"


class FakeGitHub:
    """Records every gh command; the merge result and post-merge state are scripted."""

    def __init__(self, before: dict, after: dict | None = None, merge_returncode: int = 0, comment_returncode: int = 0):
        self.captures = [before, after]
        self.commands: list[list[str]] = []
        self.merge_returncode = merge_returncode
        self.comment_returncode = comment_returncode

    def capture(self, repository: str, pull_request: int) -> dict:
        return deepcopy(self.captures.pop(0))

    def run(self, command: list[str]):
        self.commands.append(command)
        code = self.merge_returncode if command[:3] == ["gh", "pr", "merge"] else self.comment_returncode
        return subprocess.CompletedProcess(command, code, "", "simulated failure" if code else "")

    def merge_commands(self) -> list[list[str]]:
        return [c for c in self.commands if c[:3] == ["gh", "pr", "merge"]]


def merged_state(head: str = HEAD, merge_commit: str = MERGE_COMMIT, merged_by: str = "merge-app") -> dict:
    after = open_pr()
    after["pull_request"].update(state="MERGED", head_sha=head, merge_commit=merge_commit, merged_by=merged_by)
    return after


def test_executor_merges_exact_head_and_posts_a_receipt() -> None:
    gh = FakeGitHub(open_pr(), merged_state())
    receipt = execute_merge(executor_authority(), "tticom/score2gp", 441, "merge-app", capture=gh.capture, run=gh.run)
    assert gh.merge_commands() == [[
        "gh", "pr", "merge", "441", "--repo", "tticom/score2gp", "--merge", "--match-head-commit", HEAD,
    ]]
    assert all("--admin" not in command for command in gh.commands)
    assert receipt["head_sha"] == HEAD and receipt["merge_commit"] == MERGE_COMMIT and receipt["merged_by"] == "merge-app"
    comment = gh.commands[-1]
    assert comment[:3] == ["gh", "pr", "comment"]
    assert parse_merge_receipts([{"author": "merge-app", "body": comment[-1]}])[0]["merge_commit"] == MERGE_COMMIT


@pytest.mark.parametrize(
    ("mutation", "login", "failure"),
    [
        (lambda x: x["pull_request"].update(reviews=[{"author": "reviewer-a", "state": "APPROVED", "head_sha": "b" * 40}]),
         "merge-app", "current_head_not_approved"),
        (lambda x: None, "tticom-codex", "merge_controller_identity_not_configured"),
        (lambda x: x["pull_request"].update(author="merge-app"), "merge-app", "merge_controller_is_pr_author"),
        (lambda x: x["protection"].update(current_user_can_bypass=True), "merge-app", "merge_controller_can_bypass_ruleset"),
        (lambda x: x.update(admin_bypass=True), "merge-app", "admin_bypass_forbidden"),
        (lambda x: x["pull_request"]["checks"].clear(), "merge-app", "required_check_not_success:test"),
        (lambda x: x["pull_request"].update(unresolved_threads=1), "merge-app", "unresolved_review_threads"),
        (lambda x: x["pull_request"].update(head_branch="feat/other"), "merge-app", "branch_mismatch"),
        (lambda x: x["pull_request"].update(state="CLOSED"), "merge-app", "pr_not_open"),
        (lambda x: x["protection"].update(active_rulesets=0), "merge-app", "active_main_ruleset_missing"),
    ],
)
def test_executor_never_merges_on_deny(mutation, login: str, failure: str) -> None:
    before = open_pr()
    mutation(before)
    gh = FakeGitHub(before)
    with pytest.raises(ControlError, match=failure):
        execute_merge(executor_authority(), "tticom/score2gp", 441, login, capture=gh.capture, run=gh.run)
    assert gh.commands == []


def test_executor_never_merges_during_an_active_incident() -> None:
    config = executor_authority()
    config["incidents"] = [{"id": "incident-1", "status": "OPEN", "opened_by": "report.md"}]
    gh = FakeGitHub(open_pr())
    with pytest.raises(ControlError, match="active_incident"):
        execute_merge(config, "tticom/score2gp", 441, "merge-app", capture=gh.capture, run=gh.run)
    assert gh.commands == []


def test_head_change_between_gate_and_merge_fails_closed_without_a_receipt() -> None:
    # GitHub refuses --match-head-commit when the head moved after the gate.
    gh = FakeGitHub(open_pr(), merge_returncode=1)
    with pytest.raises(ControlError, match="gh pr merge failed"):
        execute_merge(executor_authority(), "tticom/score2gp", 441, "merge-app", capture=gh.capture, run=gh.run)
    assert [c[:3] for c in gh.commands] == [["gh", "pr", "merge"]]


def test_merged_head_differing_from_the_gated_head_fails_closed() -> None:
    gh = FakeGitHub(open_pr(), merged_state(head="c" * 40))
    with pytest.raises(ControlError, match="merged head differs"):
        execute_merge(executor_authority(), "tticom/score2gp", 441, "merge-app", capture=gh.capture, run=gh.run)
    assert not any(c[:3] == ["gh", "pr", "comment"] for c in gh.commands)


def test_merge_that_did_not_complete_fails_closed() -> None:
    gh = FakeGitHub(open_pr(), open_pr())
    with pytest.raises(ControlError, match="not MERGED"):
        execute_merge(executor_authority(), "tticom/score2gp", 441, "merge-app", capture=gh.capture, run=gh.run)


def receipt_for(head: str = HEAD, merge_commit: str = MERGE_COMMIT, merged_by: str = "tticom-codex",
                posted_by: str | None = None) -> dict:
    body = format_merge_receipt({"head_sha": head, "merge_commit": merge_commit, "merged_by": merged_by})
    return parse_merge_receipts([{"author": posted_by or merged_by, "body": body}])[0]


def delegated_merge(receipts: list[dict] | None = None) -> dict:
    return {
        "repository": "tticom/score2gp", "number": 7, "merged_by": "tticom-codex",
        "head_sha": HEAD, "merge_commit": MERGE_COMMIT,
        "receipts": [receipt_for()] if receipts is None else receipts,
    }


def test_receipt_audit_accepts_a_matching_executor_receipt() -> None:
    assert audit_merge_receipts([delegated_merge()], ["tticom-codex", "tticomgov-code"]) == []


@pytest.mark.parametrize(
    "receipts",
    [
        [],
        [receipt_for(head="c" * 40)],
        [receipt_for(merge_commit="d" * 40)],
        [receipt_for(merged_by="tticomgov-code")],
        [receipt_for(posted_by="tticom-automation")],
    ],
    ids=["missing", "wrong-head", "wrong-merge-commit", "wrong-merger", "posted-by-another-login"],
)
def test_receipt_audit_flags_delegated_merges_without_a_matching_receipt(receipts) -> None:
    violations = audit_merge_receipts([delegated_merge(receipts)], ["tticom-codex", "tticomgov-code"])
    assert violations == [
        "tticom/score2gp#7 merged by delegated login tticom-codex without a matching merge-executor receipt"
    ]


def test_receipt_audit_ignores_merges_by_non_delegated_logins() -> None:
    maintainer_merge = dict(delegated_merge([]), merged_by="tticom")
    assert audit_merge_receipts([maintainer_merge], ["tticom-codex", "tticomgov-code"]) == []


def test_non_receipt_comments_are_not_parsed_as_receipts() -> None:
    assert parse_merge_receipts([
        {"author": "tticom-codex", "body": "LGTM"},
        {"author": "tticom-codex", "body": "note\n<!-- score2gp-merge-receipt -->\n```json\n{}\n```"},
    ]) == []


# --- GOV-01 review 5307413925: base branch and merger identity ---

@pytest.mark.parametrize(
    ("repository", "branch"),
    [(AGENTOPS_REPOSITORY, "governance/misc"), ("tticom/score2gp", "feat/task-108")],
    ids=["governance-pr", "task-pr"],
)
def test_executor_never_merges_a_pr_that_does_not_target_main(repository: str, branch: str) -> None:
    before = open_pr(repository, branch)
    before["pull_request"]["base_branch"] = "scratch"
    gh = FakeGitHub(before)
    with pytest.raises(ControlError, match="base_branch_mismatch"):
        execute_merge(executor_authority(), repository, 441, "merge-app", capture=gh.capture, run=gh.run)
    assert gh.commands == []


def test_task_pr_must_target_the_task_base_branch() -> None:
    config = executor_authority()
    config["task"]["base_branch"] = "release"
    assert "base_branch_mismatch" in verify_merge_gate(config, gated(open_pr(), config=config))["failures"]
    facts = open_pr()
    facts["pull_request"]["base_branch"] = "release"
    assert "base_branch_mismatch" not in verify_merge_gate(config, gated(facts, config=config))["failures"]


@pytest.mark.parametrize("merged_by", [None, "", "   ", 42])
def test_receipt_audit_fails_closed_on_missing_merger_identity(merged_by) -> None:
    pr = dict(delegated_merge([]), merged_by=merged_by)
    assert audit_merge_receipts([pr], ["tticom-codex"]) == [
        "tticom/score2gp#7 has no merger identity; cannot verify it against merge-executor receipts"
    ]


# --- GOV-01 review 5307639542: the task PR number binds the task path ---

def test_executor_never_merges_a_different_pr_on_the_task_branch() -> None:
    config = executor_authority()
    assert config["task"]["pull_request"] == 441
    before = open_pr()
    before["pull_request"]["number"] = 442
    gh = FakeGitHub(before)
    with pytest.raises(ControlError, match="pull_request_mismatch"):
        execute_merge(config, "tticom/score2gp", 442, "merge-app", capture=gh.capture, run=gh.run)
    assert gh.commands == []


def test_task_pr_without_a_recorded_number_is_not_number_bound() -> None:
    config = executor_authority()
    config["task"]["pull_request"] = None
    facts = open_pr()
    facts["pull_request"]["number"] = 442
    assert "pull_request_mismatch" not in verify_merge_gate(config, gated(facts, config=config))["failures"]


def test_governance_pr_path_is_not_bound_to_the_task_pr_number() -> None:
    facts = open_pr(AGENTOPS_REPOSITORY, "governance/promote-x")
    facts["pull_request"]["number"] = 999
    decision = verify_merge_gate(executor_authority(), gated(facts))
    assert decision["decision"] == "ALLOW", decision["failures"]


# --- GOV-01 review 5308044291: the receipt names GitHub's actual merger ---

@pytest.mark.parametrize("actual_merger", ["outsider", "tticom", ""])
def test_executor_posts_no_receipt_when_another_login_merged(actual_merger: str) -> None:
    gh = FakeGitHub(open_pr(), merged_state(merged_by=actual_merger))
    with pytest.raises(ControlError, match="no receipt posted"):
        execute_merge(executor_authority(), "tticom/score2gp", 441, "merge-app", capture=gh.capture, run=gh.run)
    assert not any(c[:3] == ["gh", "pr", "comment"] for c in gh.commands)


def test_live_capture_records_githubs_merger_login(monkeypatch) -> None:
    raw = {
        "number": 441, "state": "MERGED", "headRefName": "feat/task-108", "headRefOid": HEAD,
        "baseRefName": "main", "author": {"login": "worker"}, "reviews": [], "statusCheckRollup": [],
        "mergeCommit": {"oid": MERGE_COMMIT}, "mergedBy": {"login": "tticom-codex"},
    }
    threads = {"data": {"repository": {"pullRequest": {"reviewThreads": {
        "nodes": [], "pageInfo": {"hasNextPage": False, "endCursor": None}}}}}}
    responses = iter([raw, threads, [], ])
    requested = []

    def fake_run_json(command):
        requested.append(command)
        return next(responses)

    monkeypatch.setattr("scripts.score2gp_orca_control.run_json", fake_run_json)
    snapshot = capture_live_state("tticom/score2gp", 441)
    assert snapshot["pull_request"]["merged_by"] == "tticom-codex"
    assert "mergedBy" in requested[0][requested[0].index("--json") + 1]


# --- GOV-03: active-task PR discovery and fail-closed binding ---

from scripts import score2gp_orca_control  # noqa: E402
from scripts.score2gp_orca_control import task_live_state  # noqa: E402

L3_01_BRANCH = "feat/l3-01-paired-staff-barline-acceptance"
L3_01_HEAD = "22048b6d16e44983991ea8da097a26ec80050424"


def l3_01_authority() -> dict:
    """The 2026-09-25 authority (revision 46): L3-01 PROMOTED with no recorded PR."""
    config = authority()
    config["authority_revision"] = 46
    config["task"] = {
        "id": "L3-01",
        "title": "Paired-staff barline acceptance for the Lesson 3 first system",
        "status": "PROMOTED",
        "repository": "tticom/score2gp",
        "base_branch": "main",
        "branch": L3_01_BRANCH,
        "pull_request": None,
        "owner_role": "implementation",
        "reviewer_role": "reviewer",
        "prompt": "projects/score2gp/prompts/next/l3-01-paired-staff-barline-acceptance.md",
        "allowed_paths": ["src/score2gp/pdf.py", "tests/test_pdf.py"],
        "acceptance": ["Lesson 3 page 1 system 1 yields exactly 4 boundaries and 3 bar boxes."],
        "required_evidence": [],
    }
    config["roles"]["implementation"]["github_logins"] = ["tticom-automation", "tticom-codex"]
    config["roles"]["reviewer"]["github_logins"] = ["tticom-codex", "tticomgov-code", "tticom-automation"]
    return config


def listed_pr(number: int = 464, state: str = "OPEN", base: str = "main",
              author: str = "tticom-automation", branch: str = L3_01_BRANCH, cross: bool = False) -> dict:
    return {"number": number, "state": state, "headRefName": branch, "baseRefName": base,
            "author": {"login": author}, "isCrossRepository": cross}


def viewed_pr(listed: dict, head: str = L3_01_HEAD, reviews: list | None = None) -> dict:
    return {
        "number": listed["number"], "state": listed["state"], "title": "L3-01: paired-staff barline acceptance",
        "headRefName": listed["headRefName"], "headRefOid": head, "baseRefName": listed["baseRefName"],
        "author": listed["author"], "reviews": reviews or [], "statusCheckRollup": [],
        "mergeCommit": None, "mergedBy": None,
    }


# #464 at 22048b6: tticom-codex had requested changes at that exact head (and at earlier heads).
L3_01_REVIEWS = [
    {"author": {"login": "tticom-codex"}, "state": "CHANGES_REQUESTED",
     "commit": {"oid": "30609cf5f703ec6dbb4ea8ee520ab40f845f5edf"}},
    {"author": {"login": "tticom-codex"}, "state": "CHANGES_REQUESTED", "commit": {"oid": L3_01_HEAD}},
]


class FakeGh:
    """Answers the gh queries discovery and capture make; records every command."""

    def __init__(self, listed: list[dict], viewed: dict | None = None, ref_exists: bool = False, ahead_by: int = 0):
        self.listed, self.viewed = listed, viewed or {}
        self.ref_exists, self.ahead_by = ref_exists, ahead_by
        self.commands: list[list[str]] = []

    def __call__(self, command: list[str]):
        self.commands.append(command)
        if command[:3] == ["gh", "pr", "list"]:
            return deepcopy(self.listed)
        if command[:3] == ["gh", "pr", "view"]:
            return deepcopy(self.viewed[int(command[3])])
        if command[:3] == ["gh", "api", "graphql"]:
            return {"data": {"repository": {"pullRequest": {"reviewThreads": {
                "nodes": [], "pageInfo": {"hasNextPage": False, "endCursor": None}}}}}}
        if "matching-refs" in command[-1]:
            branch = command[-1].split("matching-refs/heads/", 1)[1]
            return [{"ref": f"refs/heads/{branch}"}] if self.ref_exists else []
        if "/compare/" in command[-1]:
            return {"ahead_by": self.ahead_by}
        if command[-1].endswith("/rulesets"):
            return [{"id": 7, "enforcement": "active"}]
        if "/rulesets/" in command[-1]:
            return {"id": 7, "current_user_can_bypass": "never"}
        raise AssertionError(f"unexpected gh command {command}")


def discovered(monkeypatch, gh: FakeGh, config: dict | None = None) -> dict:
    monkeypatch.setattr("scripts.score2gp_orca_control.run_json", gh)
    return task_live_state((config or l3_01_authority())["task"])


def replay_live(monkeypatch) -> dict:
    only = listed_pr()
    return discovered(monkeypatch, FakeGh([only], {464: viewed_pr(only, reviews=L3_01_REVIEWS)}))


def assert_replay_resolves_to_changes_requested(live_state: dict) -> dict:
    resolved = resolve_state(l3_01_authority(), live_state)
    assert resolved["state"] != "READY"
    assert resolved["state"] == "RUNNING"
    assert resolved["reason"] == "current_head_changes_requested"
    assert resolved["dispatch_role"] == "implementation"
    assert resolved["binding_required"] is True
    assert resolved["pr_binding"] == "discovered"
    assert resolved["pull_request"] == 464
    assert "464" in resolved["next_action"] and "governance" in resolved["next_action"]
    return resolved


def test_replay_of_l3_01_discovers_464_and_routes_the_blocking_review(monkeypatch) -> None:
    live_state = replay_live(monkeypatch)
    assert live_state["pull_request"]["head_sha"] == L3_01_HEAD
    assert_replay_resolves_to_changes_requested(live_state)
    config = l3_01_authority()
    resolved = resolve_state(config, live_state)
    identity = RuntimeIdentity("niall", "tticom-automation")
    assignment = build_assignment(config, live_state, resolved, identity, "b" * 40)
    assert assignment["work"]["pull_request"] == 464
    assert assignment["work"]["expected_head_sha"] == L3_01_HEAD
    assert assignment["authority"]["binding_required"] is True
    assert assignment["authority"]["pr_binding"] == "discovered"
    assert "464" in assignment["authority"]["next_action"]
    validate_assignment(config, live_state, assignment, identity, "b" * 40)


def test_disabling_discovery_makes_the_replay_fail(monkeypatch) -> None:
    monkeypatch.setattr(score2gp_orca_control, "discover_live_state", lambda task: {})
    live_state = replay_live(monkeypatch)
    assert resolve_state(l3_01_authority(), live_state)["state"] == "READY"  # the 2026-09-25 fail-open
    with pytest.raises(AssertionError):
        assert_replay_resolves_to_changes_requested(live_state)


def test_discovery_lists_the_task_branch_in_all_states(monkeypatch) -> None:
    gh = FakeGh([], ref_exists=False)
    discovered(monkeypatch, gh)
    listing = gh.commands[0]
    assert listing[:3] == ["gh", "pr", "list"]
    assert listing[listing.index("--repo") + 1] == "tticom/score2gp"
    assert listing[listing.index("--head") + 1] == L3_01_BRANCH
    assert listing[listing.index("--state") + 1] == "all"


def test_recorded_pull_request_is_captured_without_discovery(monkeypatch) -> None:
    config = l3_01_authority()
    config["task"]["pull_request"] = 464
    only = listed_pr()
    gh = FakeGh([], {464: viewed_pr(only, reviews=L3_01_REVIEWS)})
    live_state = discovered(monkeypatch, gh, config)
    assert not [c for c in gh.commands if c[:3] == ["gh", "pr", "list"]]
    assert "discovery" not in live_state
    resolved = resolve_state(config, live_state)
    assert resolved["state"] == "RUNNING" and "binding_required" not in resolved


def test_terminal_task_is_not_discovered(monkeypatch) -> None:
    config = l3_01_authority()
    config["task"]["status"] = "COMPLETED"
    gh = FakeGh([listed_pr()])
    assert discovered(monkeypatch, gh, config) == {}
    assert gh.commands == []


def test_two_pull_requests_on_the_task_branch_fail_closed(monkeypatch) -> None:
    live_state = discovered(monkeypatch, FakeGh([listed_pr(464), listed_pr(470)]))
    resolved = resolve_state(l3_01_authority(), live_state)
    assert (resolved["state"], resolved["reason"]) == ("BLOCKED", "active_task_multiple_pull_requests")
    assert resolved["discovered_pull_requests"] == [464, 470]
    assert "dispatch_role" not in resolved


def test_wrong_base_is_not_bound(monkeypatch) -> None:
    only = listed_pr(base="release")
    live_state = discovered(monkeypatch, FakeGh([only], {464: viewed_pr(only, reviews=L3_01_REVIEWS)}))
    resolved = resolve_state(l3_01_authority(), live_state)
    assert (resolved["state"], resolved["reason"]) == ("BLOCKED", "active_task_pr_wrong_base")
    assert "binding_required" not in resolved and "dispatch_role" not in resolved


def test_author_outside_the_implementation_role_is_not_bound(monkeypatch) -> None:
    only = listed_pr(author="tticomgov-code")
    live_state = discovered(monkeypatch, FakeGh([only], {464: viewed_pr(only, reviews=L3_01_REVIEWS)}))
    resolved = resolve_state(l3_01_authority(), live_state)
    assert (resolved["state"], resolved["reason"]) == ("BLOCKED", "active_task_pr_author_not_implementation")
    assert "binding_required" not in resolved and "dispatch_role" not in resolved


def test_cross_repository_pr_is_not_bound(monkeypatch) -> None:
    only = listed_pr(cross=True)
    live_state = discovered(monkeypatch, FakeGh([only], {464: viewed_pr(only)}))
    resolved = resolve_state(l3_01_authority(), live_state)
    assert (resolved["state"], resolved["reason"]) == ("BLOCKED", "active_task_pr_cross_repository")


def test_branch_with_commits_but_no_pr_fails_closed(monkeypatch) -> None:
    gh = FakeGh([], ref_exists=True, ahead_by=3)
    live_state = discovered(monkeypatch, gh)
    compare = [c for c in gh.commands if "/compare/" in c[-1]]
    assert compare and compare[0][-1] == f"repos/tticom/score2gp/compare/main...{L3_01_BRANCH}"
    resolved = resolve_state(l3_01_authority(), live_state)
    assert (resolved["state"], resolved["reason"]) == ("BLOCKED", "active_task_branch_without_pr")


@pytest.mark.parametrize(("ref_exists", "ahead_by"), [(False, 0), (True, 0)])
def test_no_pr_and_no_new_commits_is_ready(monkeypatch, ref_exists, ahead_by) -> None:
    live_state = discovered(monkeypatch, FakeGh([], ref_exists=ref_exists, ahead_by=ahead_by))
    resolved = resolve_state(l3_01_authority(), live_state)
    assert (resolved["state"], resolved["reason"]) == ("READY", "authorised_task_without_pr")
    assert resolved["dispatch_role"] == "implementation"


def test_closed_unmerged_pr_fails_closed(monkeypatch) -> None:
    only = listed_pr(state="CLOSED")
    live_state = discovered(monkeypatch, FakeGh([only], {464: viewed_pr(only)}))
    resolved = resolve_state(l3_01_authority(), live_state)
    assert (resolved["state"], resolved["reason"]) == ("BLOCKED", "active_task_pr_closed_unmerged")


def test_merged_discovered_pr_routes_to_governance(monkeypatch) -> None:
    only = listed_pr(state="MERGED")
    live_state = discovered(monkeypatch, FakeGh([only], {464: viewed_pr(only)}))
    resolved = resolve_state(l3_01_authority(), live_state)
    assert (resolved["state"], resolved["reason"]) == ("GOVERNANCE_REQUIRED", "merge_requires_governance_reconciliation")
    assert resolved["dispatch_role"] == "governance"
    assert resolved["binding_required"] is True


@pytest.mark.parametrize(
    ("reviews", "state", "role"),
    [
        ([], "REVIEW_REQUIRED", "reviewer"),
        ([{"author": {"login": "tticom-codex"}, "state": "APPROVED", "commit": {"oid": L3_01_HEAD}}],
         "GOVERNANCE_REQUIRED", "governance"),
    ],
)
def test_discovered_pr_routes_like_a_bound_pr(monkeypatch, reviews, state, role) -> None:
    only = listed_pr()
    live_state = discovered(monkeypatch, FakeGh([only], {464: viewed_pr(only, reviews=reviews)}))
    resolved = resolve_state(l3_01_authority(), live_state)
    assert (resolved["state"], resolved["dispatch_role"]) == (state, role)
    assert resolved["binding_required"] is True


@pytest.mark.parametrize(
    ("field", "value"),
    [("number", 470), ("head_branch", "feat/other"), ("base_branch", "release"), ("author", "tticomgov-code"),
     ("state", "MERGED")],
)
def test_snapshot_disagreeing_with_the_discovered_candidate_fails_closed(monkeypatch, field, value) -> None:
    live_state = replay_live(monkeypatch)
    live_state["pull_request"][field] = value
    resolved = resolve_state(l3_01_authority(), live_state)
    assert resolved["state"] == "BLOCKED"
    assert "dispatch_role" not in resolved


def test_discovery_for_another_branch_is_not_trusted(monkeypatch) -> None:
    live_state = replay_live(monkeypatch)
    live_state["discovery"]["branch"] = "feat/other"
    resolved = resolve_state(l3_01_authority(), live_state)
    assert (resolved["state"], resolved["reason"]) == ("BLOCKED", "active_task_discovery_mismatch")


def test_pr_without_discovery_facts_still_fails_closed() -> None:
    config = l3_01_authority()
    facts = live()
    facts["pull_request"]["head_branch"] = L3_01_BRANCH
    facts["pr_binding"] = "discovered"
    assert resolve_state(config, facts)["reason"] == "active_task_missing_pull_request"


def test_merge_gate_denies_while_the_authority_pr_number_is_null() -> None:
    config = executor_authority()
    config["task"]["pull_request"] = None
    facts = open_pr()
    facts["pr_binding"] = "discovered"
    decision = verify_merge_gate(config, gated(facts, config=config))
    assert decision["decision"] == "DENY"
    assert decision["failures"] == ["task_pull_request_not_recorded"]
    recorded = executor_authority()
    assert verify_merge_gate(recorded, gated(facts, config=recorded))["decision"] == "ALLOW"


def test_executor_never_merges_a_discovered_but_unrecorded_pr() -> None:
    config = executor_authority()
    config["task"]["pull_request"] = None
    gh = FakeGitHub(open_pr())
    with pytest.raises(ControlError, match="task_pull_request_not_recorded"):
        execute_merge(config, "tticom/score2gp", 441, "merge-app", capture=gh.capture, run=gh.run)
    assert gh.merge_commands() == []


def explicit_review_facts(number: int = 465, branch: str = "feat/l3-02-other-task", title: str = "L3-02: other work") -> dict:
    return {
        "snapshot": {"repository": "tticom/score2gp"},
        "explicit_review": True,
        "pull_request": {
            "number": number, "state": "OPEN", "title": title, "head_branch": branch,
            "base_branch": "main", "head_sha": "c" * 40, "author": "tticom-automation", "reviews": [],
        },
    }


def test_explicit_review_of_another_pr_carries_that_prs_own_context() -> None:
    config = authority()
    facts = explicit_review_facts()
    resolved = resolve_state(config, facts)
    assignment = build_assignment(config, facts, resolved, RuntimeIdentity("niall", "reviewer"), "b" * 40)
    work = assignment["work"]
    assert work["goal"] == "L3-02: other work"
    assert work["repository"] == "tticom/score2gp"
    assert work["branch"] == "feat/l3-02-other-task"
    assert work["pull_request"] == 465
    assert work["linked_task"] is None
    assert work["prompt"] is None
    assert work["acceptance"] == [] and work["required_evidence"] == []
    active = config["task"]
    rendered = json.dumps(work)
    for leaked in (active["title"], active["prompt"], *active["acceptance"]):
        assert leaked not in rendered


def test_explicit_review_of_a_registered_task_pr_names_the_linked_task() -> None:
    config = authority()
    config["task_registry"] = {"L3-02": {
        "id": "L3-02", "title": "Other task", "status": "COMPLETED", "repository": "tticom/score2gp",
        "branch": "feat/l3-02-other-task", "owner_role": "implementation", "allowed_paths": ["src/b.py"],
        "prompt": "l3-02.md", "acceptance": ["other acceptance"],
    }}
    facts = explicit_review_facts()
    resolved = resolve_state(config, facts)
    work = build_assignment(config, facts, resolved, RuntimeIdentity("niall", "reviewer"), "b" * 40)["work"]
    assert work["linked_task"] == "L3-02"
    assert work["goal"] == "L3-02: other work"
    assert work["acceptance"] == ["other acceptance"] and work["prompt"] == "l3-02.md"
    assert "prove repair" not in json.dumps(work)


def test_explicit_review_of_the_active_task_pr_keeps_the_task_context() -> None:
    config = authority()
    facts = explicit_review_facts(number=441, branch="feat/task-108", title="Task 108")
    resolved = resolve_state(config, facts)
    work = build_assignment(config, facts, resolved, RuntimeIdentity("niall", "reviewer"), "b" * 40)["work"]
    assert work["goal"] == "Bounded repair"
    assert work["acceptance"] == ["prove repair"]
    assert work["linked_task"] == "108"


def _assert_own_review_context(config: dict, facts: dict, repository: str, number: int) -> None:
    resolved = resolve_state(config, facts)
    assert (resolved["state"], resolved["dispatch_role"]) == ("REVIEW_REQUIRED", "reviewer")
    work = build_assignment(config, facts, resolved, RuntimeIdentity("niall", "reviewer"), "b" * 40)["work"]
    assert (work["repository"], work["pull_request"], work["goal"]) == (repository, number, "Same-branch collision")
    assert work["linked_task"] is None and work["prompt"] is None and work["acceptance"] == []
    active = config["task"]
    rendered = json.dumps(work)
    for leaked in (active["title"], active["prompt"], *active["acceptance"]):
        assert leaked not in rendered


def test_explicit_review_of_another_repositorys_pr_on_the_active_branch_name_gets_its_own_context() -> None:
    config = authority()
    facts = explicit_review_facts(number=12, branch="feat/task-108", title="Same-branch collision")
    facts["snapshot"]["repository"] = "tticom/score2gp-agentops"
    _assert_own_review_context(config, facts, "tticom/score2gp-agentops", 12)


def test_explicit_review_of_another_pr_number_on_the_active_repository_and_branch_gets_its_own_context() -> None:
    config = authority()
    facts = explicit_review_facts(number=442, branch="feat/task-108", title="Same-branch collision")
    _assert_own_review_context(config, facts, "tticom/score2gp", 442)


def test_explicit_review_on_the_unrecorded_active_branch_still_requires_validated_discovery() -> None:
    config = authority()
    config["task"]["pull_request"] = None
    facts = explicit_review_facts(number=442, branch="feat/task-108", title="Same-branch collision")
    assert resolve_state(config, facts)["reason"] == "active_task_missing_pull_request"


def test_a_non_explicit_snapshot_of_another_pr_on_the_active_branch_still_fails_closed() -> None:
    config = authority()
    facts = explicit_review_facts(number=442, branch="feat/task-108")
    del facts["explicit_review"]
    assert resolve_state(config, facts)["reason"] == "live_pr_does_not_match_authority"
