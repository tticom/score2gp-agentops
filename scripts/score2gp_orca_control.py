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
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from scripts.score2gp_orchestrator import advance as advance_orchestration
except ModuleNotFoundError:
    from score2gp_orchestrator import advance as advance_orchestration

STATES = {
    "BLOCKED",
    "READY",
    "PROMOTED",
    "APPROVED",
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


def run_json(command: list[str]) -> Any:
    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode:
        raise ControlError(completed.stderr.strip() or f"command failed: {' '.join(command)}")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise ControlError(f"invalid JSON from {' '.join(command)}") from error


def capture_live_state(repository: str, pull_request: int) -> dict[str, Any]:
    """Capture normalized GitHub facts under the caller's scoped credential."""
    raw = run_json([
        "gh", "pr", "view", str(pull_request), "--repo", repository, "--json",
        "number,state,headRefName,headRefOid,baseRefName,author,reviews,statusCheckRollup",
    ])
    reviews = []
    for review in raw.get("reviews", []):
        reviews.append({
            "author": str((review.get("author") or {}).get("login", "")),
            "state": str(review.get("state", "")),
            "head_sha": str((review.get("commit") or {}).get("oid", "")),
        })
    checks = []
    for check in raw.get("statusCheckRollup", []):
        name = check.get("name") or check.get("context")
        conclusion = check.get("conclusion") or check.get("state")
        if name:
            checks.append({"name": str(name), "conclusion": str(conclusion or "")})
    
    nodes = []
    cursor = None
    has_next = True
    owner = repository.split('/', 1)[0]
    name_repo = repository.split('/', 1)[1]
    while has_next:
        cursor_args = ["-F", f"cursor={cursor}"] if cursor else []
        query_str = "query($owner:String!,$name:String!,$number:Int!,$cursor:String){repository(owner:$owner,name:$name){pullRequest(number:$number){reviewThreads(first:100,after:$cursor){nodes{isResolved}pageInfo{hasNextPage endCursor}}}}}"
        threads = run_json([
            "gh", "api", "graphql", "-f", f"query={query_str}",
            "-F", f"owner={owner}",
            "-F", f"name={name_repo}",
            "-F", f"number={pull_request}",
            *cursor_args,
        ])
        pr_data = threads["data"]["repository"]["pullRequest"]
        if not pr_data:
            break
        nodes.extend(pr_data["reviewThreads"]["nodes"])
        page_info = pr_data["reviewThreads"]["pageInfo"]
        has_next = bool(page_info.get("hasNextPage"))
        cursor = page_info.get("endCursor")

    rulesets = run_json(["gh", "api", "--paginate", f"repos/{repository}/rulesets"])
    active_rulesets = [item for item in rulesets if item.get("enforcement") == "active"]
    rule_details = [
        run_json(["gh", "api", f"repos/{repository}/rulesets/{item['id']}"])
        for item in active_rulesets
    ]
    return {
        "snapshot": {
            "schema_version": 1,
            "collector_version": 1,
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "repository": repository,
        },
        "pull_request": {
            "number": raw["number"],
            "state": raw["state"],
            "head_branch": raw["headRefName"],
            "head_sha": raw["headRefOid"],
            "base_branch": raw["baseRefName"],
            "author": str((raw.get("author") or {}).get("login", "")),
            "reviews": reviews,
            "checks": checks,
            "unresolved_threads": sum(not bool(node.get("isResolved")) for node in nodes),
        },
        "protection": {
            "active_rulesets": len(active_rulesets),
            "current_user_can_bypass": any(
                detail.get("current_user_can_bypass") not in {None, "never"}
                for detail in rule_details
            ),
        },
        "admin_bypass": False,
    }


def validate_authority(authority: dict[str, Any]) -> None:
    if authority.get("schema_version") not in {1, 2}:
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
        "PROMOTED": {"PROMOTED"},
        "APPROVED": {"APPROVED"},
        "RUNNING": {"IN_PROGRESS", "PR_OPEN"},
        "BLOCKED": {"BLOCKED"},
        "COMPLETE": {"COMPLETED", "MERGED", "RESOLVED"},
        "MERGED": {"MERGED"},
        "RESOLVED": {"RESOLVED"},
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
    latest_by_author: dict[str, str] = {}
    for review in pr.get("reviews", []):
        if str(review.get("head_sha", "")) == head:
            author = review.get("author")
            state = str(review.get("state", "")).upper()
            if author:
                latest_by_author[author] = state
    verdicts = list(latest_by_author.values())
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


def validate_assignment(
    authority: dict[str, Any],
    live: dict[str, Any],
    assignment: dict[str, Any],
    identity: RuntimeIdentity,
    agentops_sha: str,
) -> None:
    assigned_head = str(assignment.get("work", {}).get("expected_head_sha", ""))
    live_head = str(live.get("pull_request", {}).get("head_sha", ""))
    if assigned_head != live_head:
        raise ControlError("assignment is stale: expected PR head no longer matches live head")
    assigned_sha = str(assignment.get("authority", {}).get("agentops_sha", ""))
    if assigned_sha != agentops_sha:
        raise ControlError("assignment is stale: AgentOps authority revision changed")
    resolved = resolve_state(authority, live)
    expected = build_assignment(authority, live, resolved, identity, agentops_sha)
    if assignment != expected:
        raise ControlError("assignment is stale or does not match current authority/live state")


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
    if int(live.get("protection", {}).get("active_rulesets", 0)) < 1:
        failures.append("active_main_ruleset_missing")
    if bool(live.get("protection", {}).get("current_user_can_bypass", False)):
        failures.append("merge_controller_can_bypass_ruleset")
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
    dirty = subprocess.run(
        ["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True
    )
    if dirty.returncode or dirty.stdout.strip():
        raise ControlError("AgentOps authority worktree must be clean before dispatch")
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True
    )
    if completed.returncode:
        raise ControlError(completed.stderr.strip() or "cannot resolve AgentOps HEAD")
    return completed.stdout.strip()


def authenticated_github_login() -> str:
    completed = subprocess.run(
        ["gh", "api", "user", "--jq", ".login"], capture_output=True, text=True
    )
    if completed.returncode:
        raise ControlError(completed.stderr.strip() or "cannot verify GitHub identity")
    login = completed.stdout.strip()
    if not login:
        raise ControlError("GitHub identity is empty")
    return login


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("snapshot", "advance", "resolve", "assign", "validate", "merge-check"),
    )
    parser.add_argument("--authority", type=Path, default=Path("projects/score2gp/ORCHESTRATION_STATE.json"))
    parser.add_argument("--live", type=Path, help="Live-state JSON captured by the supervisor")
    parser.add_argument("--assignment", type=Path)
    parser.add_argument("--repository")
    parser.add_argument("--pull-request", type=int)
    parser.add_argument("--github-login", default="")
    args = parser.parse_args()
    if args.command == "snapshot":
        if not args.repository or args.pull_request is None:
            raise ControlError("snapshot requires --repository and --pull-request")
        print(json.dumps(capture_live_state(args.repository, args.pull_request), indent=2, sort_keys=True))
        return
    if args.live is None:
        raise ControlError(f"{args.command} requires --live")
    authority = load_json(args.authority)
    live = load_json(args.live)
    if args.command == "advance":
        print(json.dumps(advance_orchestration(authority, live), indent=2, sort_keys=True))
        return
    active_task_path = args.authority.parent / "ACTIVE_TASK.md"
    validate_legacy_alignment(authority, active_task_path.read_text(encoding="utf-8"))
    resolved = resolve_state(authority, live)
    if args.command == "resolve":
        output = resolved
    elif args.command == "assign":
        login = authenticated_github_login()
        if args.github_login and args.github_login != login:
            raise ControlError(f"expected GitHub login {args.github_login}, authenticated as {login}")
        identity = RuntimeIdentity(getpass.getuser(), login)
        output = build_assignment(authority, live, resolved, identity, git_head(Path.cwd()))
    elif args.command == "validate":
        if args.assignment is None:
            raise ControlError("validate requires --assignment")
        login = authenticated_github_login()
        if args.github_login and args.github_login != login:
            raise ControlError(f"expected GitHub login {args.github_login}, authenticated as {login}")
        identity = RuntimeIdentity(getpass.getuser(), login)
        validate_assignment(
            authority, live, load_json(args.assignment), identity, git_head(Path.cwd())
        )
        output = {"ok": True, "state": resolved["state"], "assignment_valid": True}
    else:
        output = verify_merge_gate(authority, live)
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except ControlError as error:
        raise SystemExit(f"ORCA_CONTROL_DENIED: {error}") from error
