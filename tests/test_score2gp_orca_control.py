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
