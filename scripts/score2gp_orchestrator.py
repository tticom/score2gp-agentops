#!/usr/bin/env python3
"""Side-effect-free autonomous decision module for the Score2GP loop.

``advance`` is the external seam. It reduces versioned authority and a live
snapshot to one idempotent action. Adapters may execute that action, but this
module never mutates Git, GitHub, files, reviews, or task authority.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


ACTIONS = {
    "EXECUTE_ASSIGNMENT",
    "REMEDIATE_CURRENT_PR",
    "AWAIT_REVIEW",
    "AWAIT_HUMAN_MERGE",
    "REQUEST_MUSICAL_ADJUDICATION",
    "PROPOSE_NEXT_TASK",
    "BLOCKED",
}
ACTIVE_INCIDENT_STATUSES = {"OPEN", "BLOCKING"}
TASK_REQUIRED_FIELDS = {
    "id",
    "title",
    "objective",
    "status",
    "repository",
    "base_branch",
    "branch",
    "owner_role",
    "allowed_paths",
    "validation_commands",
    "dependencies",
    "stop_conditions",
    "reviewer_role",
    "delivery_action",
}


class OrchestrationError(RuntimeError):
    """Authority or live state cannot be reduced safely."""


def load_authority(path: str | Path) -> dict[str, Any]:
    """Load machine authority without consulting legacy pointer prose."""
    authority_path = Path(path)
    try:
        value = json.loads(authority_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise OrchestrationError(f"cannot load authority from {authority_path}: {error}") from error
    if not isinstance(value, dict):
        raise OrchestrationError("authority must be a JSON object")
    return value


def advance(authority: dict[str, Any], live_state: dict[str, Any]) -> dict[str, Any]:
    """Return the next permitted action without producing side effects."""
    _validate_authority(authority)
    task = authority["task"]

    blockers = _active_incidents(authority)
    if blockers:
        return _decision(authority, live_state, "BLOCKED", "active_incident", blockers=blockers)

    declared = str(task["status"]).upper()
    if declared == "BLOCKED":
        return _decision(authority, live_state, "BLOCKED", "task_declared_blocked")
    if declared in {"COMPLETE", "COMPLETED", "MERGED", "RESOLVED"}:
        pull_request = live_state.get("pull_request")
        snapshot = live_state.get("snapshot") or {}
        proposal = authority.get("next_task_proposal")
        is_promotion = (
            isinstance(pull_request, dict)
            and str(pull_request.get("state", "")).upper() == "OPEN"
            and isinstance(proposal, dict)
            and str(proposal.get("status", "")).upper() == "PROPOSED"
            and snapshot.get("repository") == proposal.get("repository")
            and str(pull_request.get("head_branch", ""))
            == f"gov/promote-{str(proposal.get('id', '')).lower()}"
        )
        is_repair = (
            isinstance(pull_request, dict)
            and str(pull_request.get("state", "")).upper() == "OPEN"
            and snapshot.get("repository") == "tticom/score2gp-agentops"
            and live_state.get("control_plane_repair") is True
        )
        if is_promotion or is_repair:
            review = _current_head_review(pull_request)
            if review == "CHANGES_REQUESTED":
                return _decision(authority, live_state, "REMEDIATE_CURRENT_PR", "current_head_changes_requested")
            if review == "NONE":
                return _decision(authority, live_state, "AWAIT_REVIEW", "current_head_requires_review")
            return _decision(authority, live_state, "AWAIT_HUMAN_MERGE", "current_head_review_approved")
        return _decision(
            authority,
            live_state,
            "PROPOSE_NEXT_TASK",
            "task_declared_complete",
            may_execute_next_task=False,
        )

    triggered_stops = sorted(
        set(str(item) for item in live_state.get("stop_conditions", []))
        & set(str(item) for item in task["stop_conditions"])
    )
    if triggered_stops:
        return _decision(
            authority,
            live_state,
            "BLOCKED",
            "task_stop_condition_triggered",
            blockers=triggered_stops,
        )

    adjudication = live_state.get("adjudication")
    if isinstance(adjudication, dict) and str(adjudication.get("status", "")).upper() == "REQUIRED":
        packet = str(adjudication.get("packet", ""))
        if not packet:
            raise OrchestrationError("required adjudication lacks packet")
        return _decision(
            authority,
            live_state,
            "REQUEST_MUSICAL_ADJUDICATION",
            "musical_evidence_requires_human_adjudication",
            adjudication_packet=packet,
            reason_codes=list(adjudication.get("reason_codes", [])),
        )

    pull_request = live_state.get("pull_request")
    if pull_request is None:
        if declared not in {"READY", "PROMOTED", "APPROVED", "RUNNING", "IN_PROGRESS"}:
            return _decision(authority, live_state, "BLOCKED", "task_not_authorized")
        return _decision(
            authority,
            live_state,
            "EXECUTE_ASSIGNMENT",
            "authorized_task_without_pr",
            dispatch_role=str(task["owner_role"]),
            assignment=_assignment(task, expected_head_sha=None),
        )
    if not isinstance(pull_request, dict):
        raise OrchestrationError("pull_request must be an object or null")

    mismatch = _pr_mismatch(task, pull_request)
    if mismatch:
        return _decision(authority, live_state, "BLOCKED", mismatch)

    pr_state = str(pull_request.get("state", "")).upper()
    if pr_state == "MERGED":
        return _decision(
            authority,
            live_state,
            "PROPOSE_NEXT_TASK",
            "merged_task_requires_next_proposal",
            may_execute_next_task=False,
        )
    if pr_state != "OPEN":
        return _decision(authority, live_state, "BLOCKED", "authorized_pr_is_not_open")

    failed_checks = sorted(
        str(check.get("name", "<unnamed>"))
        for check in pull_request.get("checks", [])
        if str(check.get("conclusion", "")).upper() not in {"SUCCESS", "SKIPPED", "NEUTRAL"}
    )
    if failed_checks:
        return _decision(
            authority,
            live_state,
            "BLOCKED",
            "required_validation_not_successful",
            blockers=failed_checks,
        )

    review = _current_head_review(pull_request)
    head_sha = str(pull_request.get("head_sha", "")) or None
    if review == "CHANGES_REQUESTED":
        return _decision(
            authority,
            live_state,
            "REMEDIATE_CURRENT_PR",
            "current_head_changes_requested",
            dispatch_role=str(task["owner_role"]),
            assignment=_assignment(task, expected_head_sha=head_sha),
        )
    if review == "NONE":
        return _decision(
            authority,
            live_state,
            "AWAIT_REVIEW",
            "current_head_requires_independent_review",
            dispatch_role=str(task["reviewer_role"]),
        )
    return _decision(
        authority,
        live_state,
        "AWAIT_HUMAN_MERGE",
        "current_head_approved",
    )


def _validate_authority(authority: dict[str, Any]) -> None:
    if authority.get("schema_version") != 2:
        raise OrchestrationError("unsupported authority schema_version")
    task = authority.get("task")
    if not isinstance(task, dict):
        raise OrchestrationError("authority task is missing")
    missing = sorted(TASK_REQUIRED_FIELDS - task.keys())
    if missing:
        raise OrchestrationError(f"authority task fields missing: {', '.join(missing)}")
    for field in (
        "allowed_paths",
        "validation_commands",
        "dependencies",
        "stop_conditions",
    ):
        value = task[field]
        if not isinstance(value, list):
            raise OrchestrationError(f"task {field} must be a list")
    if not task["allowed_paths"]:
        raise OrchestrationError("task allowed_paths must be non-empty")
    if not task["validation_commands"]:
        raise OrchestrationError("task validation_commands must be non-empty")
    if task["delivery_action"] != "pull_request":
        raise OrchestrationError("task delivery_action must be pull_request")
    incidents = authority.get("incidents")
    if not isinstance(incidents, list):
        raise OrchestrationError("authority incidents must be a list")
    incident_ids: set[str] = set()
    for incident in incidents:
        if not isinstance(incident, dict):
            raise OrchestrationError("authority incident must be an object")
        incident_id = str(incident.get("id", ""))
        if not incident_id or incident_id in incident_ids:
            raise OrchestrationError("incident IDs must be present and unique")
        incident_ids.add(incident_id)


def upgrade_authority(authority: dict[str, Any]) -> dict[str, Any]:
    """Translate legacy schema v1 at the compatibility seam.

    The adapter preserves legacy meaning but does not invent validation
    commands. Governance must fill those before the result can become active
    schema-v2 authority.
    """
    if authority.get("schema_version") == 2:
        return deepcopy(authority)
    if authority.get("schema_version") != 1:
        raise OrchestrationError("unsupported authority schema_version")
    upgraded = deepcopy(authority)
    task = upgraded.get("task")
    if not isinstance(task, dict):
        raise OrchestrationError("authority task is missing")
    task.setdefault("objective", str(task.get("title", "")))
    task.setdefault("base_branch", "main")
    task.setdefault("validation_commands", [])
    task.setdefault("dependencies", [])
    task.setdefault("stop_conditions", [])
    task.setdefault("reviewer_role", "reviewer")
    task.setdefault("delivery_action", "pull_request")
    upgraded["schema_version"] = 2
    return upgraded


def render_active_task(authority: dict[str, Any]) -> str:
    """Render the legacy pointer as a read-only human view of authority."""
    _validate_authority(authority)
    task = authority["task"]
    status_map = {
        "READY": "APPROVED",
        "PROMOTED": "PROMOTED",
        "APPROVED": "APPROVED",
        "RUNNING": "IN_PROGRESS",
        "IN_PROGRESS": "IN_PROGRESS",
        "BLOCKED": "BLOCKED",
        "COMPLETE": "COMPLETED",
        "COMPLETED": "COMPLETED",
        "MERGED": "MERGED",
        "RESOLVED": "RESOLVED",
    }
    status = status_map.get(str(task["status"]).upper())
    if status is None:
        raise OrchestrationError(f"cannot render unsupported task status {task['status']}")
    pull_request = task.get("pull_request")
    pr_value = "TBD" if pull_request is None else str(pull_request)
    allowed_paths = "\n".join(f"- `{path}`" for path in task["allowed_paths"])
    validations = "\n".join(f"- `{command}`" for command in task["validation_commands"])
    return (
        "# Active Task\n\n"
        "<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->\n\n"
        f"**Task**: {task['id']} — {task['title']}\n\n"
        f"**Status**: {status}\n\n"
        f"**Repository**: {task['repository']}\n\n"
        f"**PR Branch**: `{task['branch']}`\n\n"
        f"**Pull Request**: {pr_value}\n\n"
        f"**Owner Role**: {task['owner_role']}\n\n"
        "## Objective\n\n"
        f"{task['objective']}\n\n"
        "## Allowed paths\n\n"
        f"{allowed_paths}\n\n"
        "## Validation commands\n\n"
        f"{validations}\n"
    )


def _active_incidents(authority: dict[str, Any]) -> list[str]:
    return [
        str(item["id"])
        for item in authority["incidents"]
        if str(item.get("status", "")).upper() in ACTIVE_INCIDENT_STATUSES
    ]


def _pr_mismatch(task: dict[str, Any], pull_request: dict[str, Any]) -> str | None:
    expected_number = task.get("pull_request")
    if expected_number is not None:
        try:
            expected_int = int(expected_number)
            live_int = int(pull_request.get("number", -1))
            if live_int != expected_int:
                return "live_pr_does_not_match_authority"
        except (ValueError, TypeError):
            return "live_pr_invalid_number"
    if str(pull_request.get("head_branch", "")) != str(task["branch"]):
        return "live_branch_does_not_match_authority"
    return None


def _current_head_review(pull_request: dict[str, Any]) -> str:
    head = str(pull_request.get("head_sha", ""))
    latest_by_author: dict[str, str] = {}
    for review in pull_request.get("reviews", []):
        if str(review.get("head_sha", "")) != head:
            continue
        author = str(review.get("author", ""))
        if author:
            latest_by_author[author] = str(review.get("state", "")).upper()
    verdicts = set(latest_by_author.values())
    if "CHANGES_REQUESTED" in verdicts:
        return "CHANGES_REQUESTED"
    if "APPROVED" in verdicts:
        return "APPROVED"
    return "NONE"


def _assignment(task: dict[str, Any], expected_head_sha: str | None) -> dict[str, Any]:
    return {
        "task_id": str(task["id"]),
        "objective": str(task["objective"]),
        "repository": str(task["repository"]),
        "base_branch": str(task["base_branch"]),
        "branch": str(task["branch"]),
        "pull_request": task.get("pull_request"),
        "expected_head_sha": expected_head_sha,
        "allowed_paths": list(task["allowed_paths"]),
        "validation_commands": list(task["validation_commands"]),
        "dependencies": list(task["dependencies"]),
        "stop_conditions": list(task["stop_conditions"]),
        "delivery_action": str(task["delivery_action"]),
        "may_merge": False,
        "may_select_next_task": False,
    }


def _decision(
    authority: dict[str, Any],
    live_state: dict[str, Any],
    action: str,
    reason: str,
    **extra: Any,
) -> dict[str, Any]:
    if action not in ACTIONS:
        raise OrchestrationError(f"unsupported action {action}")
    stable_live = deepcopy(live_state)
    snapshot = stable_live.get("snapshot")
    if isinstance(snapshot, dict):
        snapshot.pop("captured_at", None)
    identity_material = {
        "authority_revision": authority["authority_revision"],
        "task_id": str(authority["task"]["id"]),
        "action": action,
        "reason": reason,
        "live_state": stable_live,
    }
    digest = hashlib.sha256(
        json.dumps(identity_material, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:20]
    return {
        "schema_version": 1,
        "decision_id": f"decision-{digest}",
        "action": action,
        "reason": reason,
        "task_id": str(authority["task"]["id"]),
        **extra,
    }
