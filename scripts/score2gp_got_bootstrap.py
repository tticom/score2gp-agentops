#!/usr/bin/env python3
"""Executable Codex `got` dispatcher bootstrap."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

try:
    from scripts.score2gp_control_plane import (
        GateError,
        materialize_and_activate_skills,
        read_skills_pin,
        sync_main,
    )
    from scripts.score2gp_go_bootstrap import parse_active_task_content
    from scripts.score2gp_pr_review_state import query_reviews, resolve_current_head_review
except ModuleNotFoundError:  # Direct execution: python3 scripts/score2gp_got_bootstrap.py
    from score2gp_control_plane import (
        GateError,
        materialize_and_activate_skills,
        read_skills_pin,
        sync_main,
    )
    from score2gp_go_bootstrap import parse_active_task_content
    from score2gp_pr_review_state import query_reviews, resolve_current_head_review


class GotError(RuntimeError):
    pass


def query_pr(repo: str, branch: str) -> dict[str, Any] | None:
    result = subprocess.run(
        [
            "gh", "pr", "list", "--repo", repo,
            "--head", branch, "--state", "all", "--limit", "1",
            "--json", "number,state,headRefOid,mergedAt",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise GotError(result.stderr.strip() or "PR query failed")
    try:
        matches = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise GotError("invalid PR JSON") from error
    if not isinstance(matches, list):
        raise GotError("PR query returned non-list JSON")
    return matches[0] if matches else None


def resolve_got_state(pr: dict[str, Any] | None, reviews: list[dict[str, Any]]) -> dict[str, Any]:
    if pr is None:
        return {"state": "AWAITING_AGY_IMPLEMENTATION", "current_review": None}
    state = str(pr.get("state", "")).upper()
    head = str(pr.get("headRefOid", ""))
    if state == "MERGED":
        dispatch = "MERGED_AWAITING_GOVERNANCE_PROMOTION"
        current_review = None
    elif state == "CLOSED":
        dispatch = "BLOCKED"
        current_review = None
    elif state == "OPEN":
        current_review = resolve_current_head_review(reviews, head, "tticom-codex")
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
    pr = query_pr(repo, branch)
    reviews = (
        query_reviews(repo, int(pr["number"]))
        if pr is not None and pr["state"].upper() == "OPEN"
        else []
    )
    resolved = resolve_got_state(pr, reviews)
    print(json.dumps({
        "ok": True,
        **resolved,
        "agentops_sha": agentops_sha,
        "product_main_sha": product_sha,
        "skills_sha": skills_sha,
        "task": task.get("task"),
        "repository": repo,
        "pr_branch": branch,
        "pr": pr,
    }, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (GateError, GotError, KeyError) as error:
        raise SystemExit(f"GOT_DISPATCH_FAILED: {error}") from error
