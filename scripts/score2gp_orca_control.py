#!/usr/bin/env python3
"""Deterministic Score2GP state, assignment, and merge-gate resolver.

Policy and task authority come from ORCHESTRATION_STATE.json at a pinned
AgentOps revision. Live PR facts are input data. This module is the only place
where those inputs are reduced to an operational state for Orca.
"""
from __future__ import annotations

import argparse
import getpass
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

STATES = {
    "BLOCKED",
    "READY",
    "RUNNING",
    "REVIEW_REQUIRED",
    "GOVERNANCE_REQUIRED",
    "COMPLETE",
}
ACTIVE_INCIDENT_STATUSES = {"OPEN", "BLOCKING"}


class ControlError(RuntimeError):
    pass


@dataclass(frozen=True)
class RuntimeIdentity:
    os_user: str
    github_login: str


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ControlError(f"cannot load JSON from {path}: {error}") from error
    if not isinstance(value, dict):
        raise ControlError(f"expected JSON object in {path}")
    return value


def validate_authority(authority: dict[str, Any]) -> None:
    if authority.get("schema_version") != 1:
        raise ControlError("unsupported authority schema_version")
    task = authority.get("task")
    if not isinstance(task, dict):
        raise ControlError("authority task is missing")
    required = {"id", "status", "repository", "branch", "owner_role", "allowed_paths"}
    missing = sorted(required - task.keys())
    if missing:
        raise ControlError(f"authority task fields missing: {', '.join(missing)}")
    if not isinstance(task["allowed_paths"], list) or not task["allowed_paths"]:
        raise ControlError("task allowed_paths must be a non-empty list")
    incidents = authority.get("incidents")
    if not isinstance(incidents, list):
        raise ControlError("authority incidents must be a list")
    seen: set[str] = set()
    for incident in incidents:
        incident_id = str(incident.get("id", ""))
        if not incident_id or incident_id in seen:
            raise ControlError("incident IDs must be present and unique")
        seen.add(incident_id)
        status = str(incident.get("status", "")).upper()
        if status not in ACTIVE_INCIDENT_STATUSES | {"RESOLVED"}:
            raise ControlError(f"incident {incident_id} has unsupported status {status}")
        if status == "RESOLVED" and not incident.get("resolved_by"):
            raise ControlError(f"resolved incident {incident_id} lacks resolved_by")


def validate_legacy_alignment(authority: dict[str, Any], active_task_text: str) -> None:
    """Reject split-brain authority while ACTIVE_TASK.md remains in migration use."""
    fields: dict[str, str] = {}
    for line in active_task_text.splitlines():
        match = re.match(r"^\*\*([^*]+)\*\*:\s*`?([^`]+?)`?\s*$", line.strip())
        if match:
            fields[match.group(1).strip().lower()] = match.group(2).strip()
    task = authority["task"]
    legacy_status = fields.get("status", "").upper()
    compatible_statuses = {
        "READY": {"APPROVED", "PROMOTED"},
        "RUNNING": {"IN_PROGRESS", "PR_OPEN"},
        "BLOCKED": {"BLOCKED"},
        "COMPLETE": {"COMPLETED", "MERGED", "RESOLVED"},
    }
    checks = {
        "task": str(task["id"]) in fields.get("task", ""),
        "repository": fields.get("repository") == str(task["repository"]),
        "branch": fields.get("pr branch") == str(task["branch"]),
        "status": legacy_status in compatible_statuses.get(str(task["status"]).upper(), set()),
    }
    if task.get("pull_request") is not None and fields.get("pull request", "").upper() != "TBD":
        checks["pull_request"] = fields.get("pull request") == str(task["pull_request"])
    mismatches = sorted(name for name, matches in checks.items() if not matches)
    if mismatches:
        raise ControlError(f"ACTIVE_TASK.md diverges from orchestration authority: {', '.join(mismatches)}")


def active_incidents(authority: dict[str, Any]) -> list[str]:
    return [
        str(item["id"])
        for item in authority["incidents"]
        if str(item["status"]).upper() in ACTIVE_INCIDENT_STATUSES
    ]


def current_head_review(pr: dict[str, Any]) -> str:
    head = str(pr.get("head_sha", ""))
    verdicts = [
        str(review.get("state", "")).upper()
        for review in pr.get("reviews", [])
        if str(review.get("head_sha", "")) == head
    ]
    if "CHANGES_REQUESTED" in verdicts:
        return "CHANGES_REQUESTED"
    if "APPROVED" in verdicts:
        return "APPROVED"
    return "NONE"


def resolve_state(authority: dict[str, Any], live: dict[str, Any]) -> dict[str, Any]:
    validate_authority(authority)
    task = authority["task"]
    blockers = active_incidents(authority)
    if blockers:
        return result("BLOCKED", "active_incident", task, blockers=blockers)

    declared = str(task["status"]).upper()
    if declared == "BLOCKED":
        return result("BLOCKED", "task_declared_blocked", task)
    if declared in {"COMPLETE", "MERGED", "RESOLVED"}:
        return result("COMPLETE", "task_declared_complete", task)

    pr = live.get("pull_request")
    if not isinstance(pr, dict):
        if declared in {"READY", "PROMOTED", "APPROVED"}:
            return result("READY", "authorised_task_without_pr", task, dispatch_role=task["owner_role"])
        return result("RUNNING", "authorised_task_not_published", task, dispatch_role=task["owner_role"])

    if int(pr.get("number", -1)) != int(task.get("pull_request", -2)):
        return result("BLOCKED", "live_pr_does_not_match_authority", task)
    if str(pr.get("head_branch", "")) != str(task["branch"]):
        return result("BLOCKED", "live_branch_does_not_match_authority", task)

    pr_state = str(pr.get("state", "")).upper()
    if pr_state == "MERGED":
        return result("GOVERNANCE_REQUIRED", "merge_requires_governance_reconciliation", task, dispatch_role="governance")
    if pr_state != "OPEN":
        return result("BLOCKED", "authorised_pr_is_not_open", task)

    review = current_head_review(pr)
    if review == "CHANGES_REQUESTED":
        return result("RUNNING", "current_head_changes_requested", task, dispatch_role=task["owner_role"])
    if review == "NONE":
        return result("REVIEW_REQUIRED", "current_head_requires_review", task, dispatch_role="reviewer")
    return result("GOVERNANCE_REQUIRED", "current_head_review_approved", task, dispatch_role="governance")


def result(state: str, reason: str, task: dict[str, Any], **extra: Any) -> dict[str, Any]:
    if state not in STATES:
        raise ControlError(f"invalid operational state {state}")
    return {
        "schema_version": 1,
        "state": state,
        "reason": reason,
        "task_id": str(task["id"]),
        **extra,
    }


def authorize_role(authority: dict[str, Any], role: str, identity: RuntimeIdentity) -> None:
    role_policy = authority.get("roles", {}).get(role)
    if not isinstance(role_policy, dict):
        raise ControlError(f"unknown role {role}")
    allowed = role_policy.get("github_logins", [])
    if identity.github_login not in allowed:
        raise ControlError(
            f"identity {identity.github_login or '<none>'} is not authorised for role {role}"
        )


def build_assignment(
    authority: dict[str, Any],
    live: dict[str, Any],
    resolved: dict[str, Any],
    identity: RuntimeIdentity,
    agentops_sha: str,
) -> dict[str, Any]:
    role = resolved.get("dispatch_role")
    if resolved["state"] not in {"READY", "RUNNING", "REVIEW_REQUIRED", "GOVERNANCE_REQUIRED"} or not role:
        raise ControlError(f"state {resolved['state']} is not dispatchable")
    authorize_role(authority, str(role), identity)
    task = authority["task"]
    pr = live.get("pull_request") or {}
    role_policy = authority["roles"][role]
    return {
        "schema_version": 1,
        "assignment_type": "score2gp_bounded_worker",
        "authority": {
            "agentops_sha": agentops_sha,
            "authority_revision": authority["authority_revision"],
            "task_id": str(task["id"]),
            "operational_state": resolved["state"],
            "reason": resolved["reason"],
        },
        "worker": {
            "role": role,
            "os_user": identity.os_user,
            "github_login": identity.github_login,
        },
        "work": {
            "goal": task["title"],
            "repository": task["repository"],
            "branch": task["branch"],
            "pull_request": task.get("pull_request"),
            "expected_head_sha": pr.get("head_sha"),
            "prompt": task.get("prompt"),
            "allowed_paths": task["allowed_paths"],
            "acceptance": task.get("acceptance", []),
            "required_evidence": task.get("required_evidence", []),
        },
        "capabilities": {
            "allowed_actions": role_policy["allowed_actions"],
            "forbidden_actions": role_policy["forbidden_actions"],
        },
        "completion_contract": {
            "return_exact_head": True,
            "return_validation_receipts": True,
            "return_unresolved_risks": True,
            "may_select_next_task": False,
            "may_merge": False,
        },
    }


def verify_merge_gate(authority: dict[str, Any], live: dict[str, Any]) -> dict[str, Any]:
    validate_authority(authority)
    blockers = active_incidents(authority)
    policy = authority["merge_policy"]
    task = authority["task"]
    pr = live.get("pull_request") or {}
    failures: list[str] = []
    if blockers:
        failures.append("active_incident")
    if str(pr.get("state", "")).upper() != "OPEN":
        failures.append("pr_not_open")
    if str(pr.get("head_branch", "")) != str(task["branch"]):
        failures.append("branch_mismatch")
    head = str(pr.get("head_sha", ""))
    reviewed_head = str(live.get("governance", {}).get("reviewed_head_sha", ""))
    if policy["require_reviewed_head"] and (not head or reviewed_head != head):
        failures.append("reviewed_head_mismatch")
    if current_head_review(pr) != "APPROVED":
        failures.append("current_head_not_approved")
    approvals = {
        str(r.get("author", ""))
        for r in pr.get("reviews", [])
        if str(r.get("head_sha", "")) == head and str(r.get("state", "")).upper() == "APPROVED"
    }
    if len(approvals) < int(policy["minimum_approvals"]):
        failures.append("insufficient_independent_approvals")
    checks = {str(c.get("name")): str(c.get("conclusion", "")).upper() for c in pr.get("checks", [])}
    for required in policy["required_checks"]:
        if checks.get(required) != "SUCCESS":
            failures.append(f"required_check_not_success:{required}")
    if policy["require_resolved_threads"] and int(pr.get("unresolved_threads", 0)) != 0:
        failures.append("unresolved_review_threads")
    if policy["require_governance_go"] and live.get("governance", {}).get("decision") != "GO":
        failures.append("governance_go_missing")
    controller_login = str(live.get("merge_controller_login", ""))
    if controller_login not in authority["roles"]["merge_controller"]["github_logins"]:
        failures.append("merge_controller_identity_not_configured")
    if bool(live.get("admin_bypass", False)):
        failures.append("admin_bypass_forbidden")
    return {
        "schema_version": 1,
        "decision": "ALLOW" if not failures else "DENY",
        "repository": task["repository"],
        "pull_request": task.get("pull_request"),
        "head_sha": head or None,
        "failures": failures,
        "dry_run": True,
    }


def git_head(root: Path) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True
    )
    if completed.returncode:
        raise ControlError(completed.stderr.strip() or "cannot resolve AgentOps HEAD")
    return completed.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("resolve", "assign", "merge-check"))
    parser.add_argument("--authority", type=Path, default=Path("projects/score2gp/ORCHESTRATION_STATE.json"))
    parser.add_argument("--live", type=Path, required=True, help="Live-state JSON captured by the supervisor")
    parser.add_argument("--github-login", default="")
    args = parser.parse_args()
    authority = load_json(args.authority)
    live = load_json(args.live)
    active_task_path = args.authority.parent / "ACTIVE_TASK.md"
    validate_legacy_alignment(authority, active_task_path.read_text(encoding="utf-8"))
    resolved = resolve_state(authority, live)
    if args.command == "resolve":
        output = resolved
    elif args.command == "assign":
        identity = RuntimeIdentity(getpass.getuser(), args.github_login)
        output = build_assignment(authority, live, resolved, identity, git_head(Path.cwd()))
    else:
        output = verify_merge_gate(authority, live)
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except ControlError as error:
        raise SystemExit(f"ORCA_CONTROL_DENIED: {error}") from error
