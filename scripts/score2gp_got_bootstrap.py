#!/usr/bin/env python3
"""Executable Codex `got` dispatcher bootstrap."""
from __future__ import annotations

import argparse
import getpass
import json
import os
import subprocess
from pathlib import Path
from typing import Any

try:
    from scripts.score2gp_control_plane import (
        GateError,
        materialize_review_head,
        materialize_and_activate_skills,
        read_skills_pin,
        sync_main,
    )
    from scripts.score2gp_go_bootstrap import parse_active_task_content, query_github_pr_state
    from scripts.score2gp_pr_review_state import (
        TRUSTED_REVIEWERS,
        query_reviews,
        resolve_current_head_review,
    )
except ModuleNotFoundError:  # Direct execution: python3 scripts/score2gp_got_bootstrap.py
    from score2gp_control_plane import (
        GateError,
        materialize_review_head,
        materialize_and_activate_skills,
        read_skills_pin,
        sync_main,
    )
    from score2gp_go_bootstrap import parse_active_task_content, query_github_pr_state
    from score2gp_pr_review_state import (
        TRUSTED_REVIEWERS,
        query_reviews,
        resolve_current_head_review,
    )


class GotError(RuntimeError):
    pass


REVIEW_LEVEL_RANK = {"basic": 0, "hard": 1, "devils-advocate": 2}
REVIEW_SKILL = {
    "basic": "code-review",
    "hard": "hard-review",
    "devils-advocate": "devils-advocate-review",
}


def _declared_review_level(value: str | None) -> str | None:
    if value is None or not value.strip():
        return None
    normalized = value.strip().lower().replace("_", "-").replace(" ", "-")
    aliases = {
        "basic": "basic",
        "code-review": "basic",
        "hard": "hard",
        "hard-review": "hard",
        "devils-advocate": "devils-advocate",
        "devil's-advocate": "devils-advocate",
        "devils-advocate-review": "devils-advocate",
        "real-review": "devils-advocate",
    }
    if normalized not in aliases:
        raise GotError(f"unsupported Review Level: {value}")
    return aliases[normalized]


def select_review_level(
    *,
    repository: str,
    changed_paths: list[str],
    task: str = "",
    authorised_role: str = "",
    title: str = "",
    live_head: str = "",
    reviews: list[dict[str, Any]] | None = None,
    declared_level: str | None = None,
) -> dict[str, Any]:
    """Select the minimum review level; declarations may escalate, never weaken it."""
    level = "basic"
    reasons: list[str] = []

    def escalate(candidate: str, reason: str) -> None:
        nonlocal level
        if REVIEW_LEVEL_RANK[candidate] > REVIEW_LEVEL_RANK[level]:
            level = candidate
        if reason not in reasons:
            reasons.append(reason)

    normalized_paths = [path.strip().lower() for path in changed_paths if path.strip()]
    context = " ".join((task, authorised_role, title, *normalized_paths)).lower()

    if repository == "tticom/score2gp-agentops":
        escalate("devils-advocate", "governance/control-plane repository change")
    if not normalized_paths:
        escalate("devils-advocate", "empty or unavailable changed-path inventory")

    architecture_markers = (
        "architect",
        "research",
        "docs/design/",
        "architecture",
        "migration-map",
        "active_task.md",
        "skills_lock.md",
        "workflow_skills_profile.md",
    )
    if any(marker in context for marker in architecture_markers):
        escalate("devils-advocate", "architecture, research, or authority translation")

    high_risk_markers = (
        "conversion",
        "musicxml",
        "scoreir",
        "gpif",
        "omr",
        "pdf",
        "timing",
        "duration",
        "grouping",
        "geometry",
        "parser",
        "recognition",
        "private",
        "privacy",
        "fallback",
        "fail-closed",
    )
    if any(marker in context for marker in high_risk_markers):
        escalate("devils-advocate", "high-risk conversion or evidence claim")

    domain_prefixes = ("src/", "tests/", "fixtures/", "scripts/")
    if any(path.startswith(domain_prefixes) for path in normalized_paths):
        escalate("hard", "code, test, fixture, or executable-script change")
    if any(not path.endswith((".md", ".txt", ".rst")) for path in normalized_paths):
        escalate("hard", "non-documentation change")

    trusted = set(TRUSTED_REVIEWERS)
    if any(
        (review.get("user") or review.get("author") or {}).get("login") in trusted
        and review.get("commit_id")
        and review.get("commit_id") != live_head
        for review in reviews or []
    ):
        escalate("devils-advocate", "re-review after a trusted review on an earlier head")

    declared = _declared_review_level(declared_level)
    if declared is not None and REVIEW_LEVEL_RANK[declared] > REVIEW_LEVEL_RANK[level]:
        escalate(declared, f"ACTIVE_TASK declared minimum review level {declared}")

    return {
        "level": level,
        "skill": REVIEW_SKILL[level],
        "reasons": reasons or ["low-risk documentation-only change"],
    }


def query_pr_review_context(repo: str, pr_number: int) -> dict[str, Any]:
    result = subprocess.run(
        [
            "gh", "pr", "view", str(pr_number), "--repo", repo,
            "--json", "title,author,files",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise GotError(result.stderr.strip() or "PR review-context query failed")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise GotError("invalid PR review-context JSON") from error
    files = payload.get("files")
    if not isinstance(files, list):
        raise GotError("PR review-context files must be a list")
    paths = [str(item.get("path", "")) for item in files if isinstance(item, dict)]
    return {
        "title": str(payload.get("title", "")),
        "author": str((payload.get("author") or {}).get("login", "")),
        "changed_paths": paths,
    }

HANDOFF_MARKERS = (
    "AWAITING_CODEX_REVIEW",
    "AWAITING_GOVERNANCE_REVIEW",
    "AWAITING_EXTERNAL_REVIEW",
)


def query_pr_comments(repo: str, pr_number: int) -> list[dict[str, Any]]:
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/issues/{pr_number}/comments?per_page=100"],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise GotError(result.stderr.strip() or "PR handback-comment query failed")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise GotError("invalid PR handback-comment JSON") from error
    if not isinstance(payload, list):
        raise GotError("PR handback-comment query must return a list")
    return [comment for comment in payload if isinstance(comment, dict)]


def find_current_head_handback(
    comments: list[dict[str, Any]], *, head: str, author: str
) -> dict[str, Any] | None:
    if len(head) != 40 or not author:
        return None
    eligible = []
    for comment in comments:
        body = str(comment.get("body", ""))
        login = str((comment.get("user") or {}).get("login", ""))
        if (
            login == author
            and head in body
            and any(marker in body for marker in HANDOFF_MARKERS)
        ):
            eligible.append(comment)
    if not eligible:
        return None
    return max(eligible, key=lambda comment: int(comment.get("id") or 0))


def gate_review_on_handback(
    resolved: dict[str, Any], handback: dict[str, Any] | None
) -> dict[str, Any]:
    if resolved.get("state") == "REVIEW_CURRENT_HEAD" and handback is None:
        return {"state": "AWAITING_AGY_HANDBACK", "current_review": None}
    return resolved


def validate_governance_identity(
    *,
    linux_user: str,
    home: str,
    gh_user: str,
    git_user: str,
    agentops: Path,
    product: Path,
) -> None:
    profiles = {
        "tticom-gov": ("/home/tticom-gov", "tticomgov-code"),
        "tticom-codex": ("/home/tticom-codex", "tticom-codex"),
        "tticom": ("/home/tticom", "tticom"),
    }
    if linux_user not in profiles:
        raise GotError(f"unsupported governance Linux user: '{linux_user}'")
    expected_home, expected_identity = profiles[linux_user]
    if home != expected_home:
        raise GotError(f"HOME must be '{expected_home}', got '{home}'")
    if linux_user == "tticom" and gh_user == "":
        # Personal account does not require authenticated GitHub CLI
        pass
    elif gh_user != expected_identity:
        raise GotError(f"GitHub CLI account must be '{expected_identity}', got '{gh_user}'")
    if git_user != expected_identity:
        raise GotError(f"Git global user.name must be '{expected_identity}', got '{git_user}'")

    workspace = Path(expected_home) / "work/score2gp-workspace"
    for label, path in (("AgentOps", agentops), ("product", product)):
        try:
            path.relative_to(workspace)
        except ValueError as error:
            raise GotError(
                f"{label} path must be within '{workspace}', got '{path}'"
            ) from error


def enforce_governance_identity(agentops: Path, product: Path) -> None:
    def output(command: list[str]) -> str:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode:
            raise GotError(result.stderr.strip() or f"command failed: {command}")
        return result.stdout.strip()

    linux_user = getpass.getuser()
    try:
        gh_user = output(["gh", "api", "user", "--jq", ".login"])
    except GotError:
        if linux_user == "tticom":
            gh_user = ""
        else:
            raise

    validate_governance_identity(
        linux_user=linux_user,
        home=os.environ.get("HOME", ""),
        gh_user=gh_user,
        git_user=output(["git", "config", "--global", "--get", "user.name"]),
        agentops=agentops,
        product=product,
    )


def query_pr(repo: str, branch: str) -> tuple[dict[str, Any] | None, str]:
    pr = query_github_pr_state(repo, branch)
    if pr is not None:
        return pr, repo
    alt_repo = "tticom/score2gp-agentops" if repo == "tticom/score2gp" else "tticom/score2gp"
    pr = query_github_pr_state(alt_repo, branch)
    if pr is not None:
        return pr, alt_repo
    return None, repo


def resolve_got_state(
    pr: dict[str, Any] | None,
    reviews: list[dict[str, Any]],
    active_task_status: str | None = None,
) -> dict[str, Any]:
    if pr is None:
        if active_task_status and active_task_status.upper() == "RESOLVED":
            return {"state": "PROMOTE_RESOLVED_TASK", "current_review": None}
        if active_task_status and active_task_status.upper() == "MERGED":
            return {"state": "NO_ACTIVE_TASK", "current_review": None}
        return {"state": "AWAITING_AGY_PUBLICATION", "current_review": None}
    state = str(pr.get("state", "")).upper()
    head = str(pr.get("headRefOid", ""))
    if state == "MERGED":
        if active_task_status and active_task_status.upper() == "MERGED":
            dispatch = "NO_ACTIVE_TASK"
        elif active_task_status and active_task_status.upper() == "RESOLVED":
            dispatch = "PROMOTE_RESOLVED_TASK"
        else:
            dispatch = "PROMOTE_MERGED_TASK"
        current_review = None
    elif state == "CLOSED":
        dispatch = "BLOCKED"
        current_review = None
    elif state == "OPEN":
        current_review = resolve_current_head_review(reviews, head, TRUSTED_REVIEWERS)
        verdict = str((current_review or {}).get("state", "")).upper()
        if verdict == "CHANGES_REQUESTED":
            dispatch = "AWAITING_AGY_FIXES"
        elif verdict == "APPROVED":
            dispatch = "READY_FOR_HUMAN_MERGE"
        else:
            dispatch = "REVIEW_CURRENT_HEAD"
    else:
        raise GotError(f"unsupported PR state: {state}")
    return {"state": dispatch, "current_review": current_review}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agentops", type=Path, default=Path("."))
    parser.add_argument("--product", type=Path, default=Path("../score2gp"))
    parser.add_argument("--skills-repo", type=Path, default=Path("../../agy-skills"))
    args = parser.parse_args()

    agentops = args.agentops.resolve()
    product = args.product.resolve()
    enforce_governance_identity(agentops, product)
    agentops_sha = sync_main(agentops, "agentops")
    product_sha = sync_main(product, "product")
    skills_sha = materialize_and_activate_skills(
        args.skills_repo.resolve(), read_skills_pin(agentops)
    )
    task = parse_active_task_content(
        (agentops / "projects/score2gp/ACTIVE_TASK.md").read_text(encoding="utf-8")
    )
    repo = task["repository"]
    branch = task["pr branch"]
    pr, actual_repo = query_pr(repo, branch)
    reviews = (
        query_reviews(actual_repo, int(pr["number"]))
        if pr is not None and pr["state"].upper() == "OPEN"
        else []
    )
    task_status = task.get("status")
    resolved = resolve_got_state(pr, reviews, active_task_status=task_status)
    review_selection = None
    review_worktree = None
    review_local_head = None
    review_context = None
    author_handback = None
    if pr is not None and str(pr.get("state", "")).upper() == "OPEN":
        review_context = query_pr_review_context(actual_repo, int(pr["number"]))
        comments = query_pr_comments(actual_repo, int(pr["number"]))
        author_handback = find_current_head_handback(
            comments,
            head=str(pr.get("headRefOid", "")),
            author=review_context["author"],
        )
        resolved = gate_review_on_handback(resolved, author_handback)
        review_selection = select_review_level(
            repository=actual_repo,
            changed_paths=review_context["changed_paths"],
            task=task.get("task", ""),
            authorised_role=task.get("authorised role", ""),
            title=review_context["title"],
            live_head=str(pr.get("headRefOid", "")),
            reviews=reviews,
            declared_level=task.get("review level"),
        )
        if resolved["state"] == "REVIEW_CURRENT_HEAD":
            review_repo = agentops if actual_repo == "tticom/score2gp-agentops" else product
            head = str(pr["headRefOid"])
            review_worktree_path = (
                review_repo.parent
                / f"{review_repo.name}-review-pr-{pr['number']}-{head[:12]}"
            )
            review_local_head = materialize_review_head(
                review_repo, review_worktree_path, head
            )
            review_worktree = str(review_worktree_path)
    print(json.dumps({
        "ok": True,
        **resolved,
        "agentops_sha": agentops_sha,
        "product_main_sha": product_sha,
        "skills_sha": skills_sha,
        "task": task.get("task"),
        "repository": repo,
        "actual_repository": actual_repo,
        "pr_branch": branch,
        "pr": pr,
        "review_level": (review_selection or {}).get("level"),
        "review_skill": (review_selection or {}).get("skill"),
        "review_reasons": (review_selection or {}).get("reasons", []),
        "review_changed_paths": (review_context or {}).get("changed_paths", []),
        "review_author": (review_context or {}).get("author"),
        "review_worktree": review_worktree,
        "review_local_head": review_local_head,
        "author_handback": author_handback,
    }, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (GateError, GotError, KeyError) as error:
        raise SystemExit(f"GOT_DISPATCH_FAILED: {error}") from error
