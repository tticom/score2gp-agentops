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


def validate_governance_identity(
    *,
    linux_user: str,
    home: str,
    gh_user: str,
    git_user: str,
    agentops: Path,
    product: Path,
) -> None:
    if linux_user != "tticom-gov":
        raise GotError(f"Linux user must be 'tticom-gov', got '{linux_user}'")
    if home != "/home/tticom-gov":
        raise GotError(f"HOME must be '/home/tticom-gov', got '{home}'")
    if gh_user != "tticom-codex":
        raise GotError(f"GitHub CLI account must be 'tticom-codex', got '{gh_user}'")
    if git_user != "tticom-codex":
        raise GotError(f"Git global user.name must be 'tticom-codex', got '{git_user}'")

    workspace = Path("/home/tticom-gov/work/score2gp-workspace")
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

    validate_governance_identity(
        linux_user=getpass.getuser(),
        home=os.environ.get("HOME", ""),
        gh_user=output(["gh", "api", "user", "--jq", ".login"]),
        git_user=output(["git", "config", "--global", "--get", "user.name"]),
        agentops=agentops,
        product=product,
    )


def query_pr(repo: str, branch: str) -> dict[str, Any]:
    result = subprocess.run(
        [
            "gh", "pr", "view", branch, "--repo", repo,
            "--json", "number,state,headRefOid,mergedAt",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise GotError(result.stderr.strip() or "PR query failed")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise GotError("invalid PR JSON") from error


def resolve_got_state(pr: dict[str, Any], reviews: list[dict[str, Any]]) -> dict[str, Any]:
    state = str(pr.get("state", "")).upper()
    head = str(pr.get("headRefOid", ""))
    if state == "MERGED":
        dispatch = "PROMOTE_MERGED_TASK"
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
    pr = query_pr(repo, branch)
    reviews = query_reviews(repo, int(pr["number"])) if pr["state"].upper() == "OPEN" else []
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
