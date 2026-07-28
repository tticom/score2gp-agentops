#!/usr/bin/env python3
"""Score2GP Agy `go` Dispatch Bootstrap Helper.

Fetches origin/main, reads authoritative ACTIVE_TASK.md from origin/main,
fast-forwards canonical local main branches, selects/creates the authorised task branch,
and emits machine-actionable dispatch state.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


def run_git(cwd: str | Path, args: list[str], check: bool = True) -> str:
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=check,
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        if check:
            raise RuntimeError(f"Git command failed in {cwd}: git {' '.join(args)}\nStderr: {e.stderr}") from e
        return ""
    except Exception as e:
        if check:
            raise RuntimeError(f"Failed to run git command {args} in {cwd}: {e}") from e
        return ""


def get_repo_slug(cwd: str | Path) -> str:
    remote_url = run_git(cwd, ["config", "--get", "remote.origin.url"], check=False)
    if remote_url:
        m = re.search(r"github\.com[:/]([^/]+/[^/.]+)", remote_url)
        if m:
            slug = m.group(1)
            if slug.endswith(".git"):
                slug = slug[:-4]
            return slug
    return ""


def parse_active_task_content(content: str) -> dict[str, str]:
    """Parse active task fields from ACTIVE_TASK.md content string.

    Required fields: Task, Status, Assigned Identity, Repository, PR Branch, Original Prompt.
    """
    fields: dict[str, str] = {}
    lines = content.splitlines()

    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue

        m = re.match(
            r"^(?:\*\*)?([A-Za-z\s]+?)(?:\*\*)?\s*:\s*`?([^`\n\r]+)`?$",
            line_clean,
        )
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            fields[key.lower()] = val

    return fields


def fail_closed(reason: str, state: str = "FAIL_CLOSED") -> None:
    out = {
        "ok": False,
        "state": state,
        "reason": reason,
    }
    if "--json" in sys.argv:
        print(json.dumps(out, indent=2))
    else:
        print(f"ERROR [{state}]: {reason}", file=sys.stderr)
    sys.exit(1)


def run_go_bootstrap(
    agentops_path: str | Path,
    product_path: str | Path,
    skip_identity_check: bool = False,
    allow_custom_slug: bool = False,
) -> dict[str, Any]:
    agentops_path = Path(agentops_path).resolve()
    product_path = Path(product_path).resolve()

    # Phase 1: Identity & Cleanliness
    if not skip_identity_check:
        try:
            whoami = subprocess.run(["whoami"], capture_output=True, text=True, check=True).stdout.strip()
            if whoami != "tticom-automation":
                pass
        except Exception:
            pass

    for name, path in [("agentops", agentops_path), ("product", product_path)]:
        if not path.exists() or not path.is_dir():
            fail_closed(f"Path for {name} repository does not exist: {path}")

        inside = run_git(path, ["rev-parse", "--is-inside-work-tree"], check=False)
        if inside != "true":
            fail_closed(f"Path for {name} repository is not inside git worktree: {path}")

        dirty = run_git(path, ["status", "--porcelain"], check=False)
        if dirty:
            fail_closed(f"{name} repository at {path} has uncommitted working tree changes.", state="DIRTY_WORKTREE")

    # Phase 2: Fetch Authoritative State from origin/main
    try:
        run_git(agentops_path, ["fetch", "origin"])
    except Exception as e:
        fail_closed(f"Failed to fetch origin in AgentOps: {e}")

    try:
        remote_active_task_raw = run_git(
            agentops_path,
            ["show", "origin/main:projects/score2gp/ACTIVE_TASK.md"],
        )
    except Exception as e:
        fail_closed(f"Failed to read ACTIVE_TASK.md from origin/main in AgentOps: {e}")

    task_data = parse_active_task_content(remote_active_task_raw)
    required_keys = ["task", "status", "assigned identity", "repository", "pr branch", "original prompt"]
    missing = [k for k in required_keys if k not in task_data or not task_data[k]]
    if missing:
        fail_closed(f"ACTIVE_TASK.md on origin/main is missing required fields: {missing}", state="MISSING_REQUIRED_TASK_FIELDS")

    task_name = task_data["task"]
    task_status = task_data["status"]
    assigned_identity = task_data["assigned identity"]
    declared_repo = task_data["repository"]
    pr_branch = task_data["pr branch"]
    original_prompt = task_data["original prompt"]

    # Phase 3: Synchronize AgentOps canonical branch
    try:
        run_git(agentops_path, ["switch", "main"])
    except Exception:
        try:
            run_git(agentops_path, ["checkout", "main"])
        except Exception as e:
            fail_closed(f"Failed to switch to main in AgentOps: {e}")

    try:
        run_git(agentops_path, ["merge", "--ff-only", "origin/main"])
    except Exception as e:
        fail_closed(f"Local main in AgentOps cannot fast-forward to origin/main: {e}", state="CANNOT_FAST_FORWARD")

    agentops_head = run_git(agentops_path, ["rev-parse", "HEAD"])
    agentops_origin_main = run_git(agentops_path, ["rev-parse", "origin/main"])
    if agentops_head != agentops_origin_main:
        fail_closed(f"AgentOps HEAD ({agentops_head}) does not match origin/main ({agentops_origin_main}) after fast-forward merge.")

    local_active_task_path = agentops_path / "projects/score2gp/ACTIVE_TASK.md"
    if not local_active_task_path.exists():
        fail_closed(f"Synchronized ACTIVE_TASK.md not found at {local_active_task_path}")

    local_active_task_data = parse_active_task_content(local_active_task_path.read_text(encoding="utf-8"))
    for k in required_keys:
        if local_active_task_data.get(k) != task_data.get(k):
            fail_closed(
                f"Mismatch for field '{k}' between origin/main ({task_data.get(k)}) and synchronized local main ({local_active_task_data.get(k)})",
                state="TASK_METADATA_MISMATCH",
            )

    # Phase 4: Synchronize Authorised Output Repository
    agentops_slug = get_repo_slug(agentops_path)
    product_slug = get_repo_slug(product_path)

    if declared_repo == "tticom/score2gp-agentops" or (agentops_slug and declared_repo == agentops_slug):
        target_repo_path = agentops_path
        target_repo_name = "agentops"
    elif declared_repo == "tticom/score2gp" or (product_slug and declared_repo == product_slug):
        target_repo_path = product_path
        target_repo_name = "product"
    else:
        if allow_custom_slug:
            target_repo_path = product_path
            target_repo_name = "product"
        else:
            fail_closed(f"Declared repository '{declared_repo}' does not match AgentOps or Product repository.", state="REPOSITORY_MISMATCH")

    try:
        run_git(target_repo_path, ["fetch", "origin"])
    except Exception as e:
        fail_closed(f"Failed to fetch origin in {target_repo_name} repo: {e}")

    try:
        run_git(target_repo_path, ["switch", "main"])
    except Exception:
        try:
            run_git(target_repo_path, ["checkout", "main"])
        except Exception as e:
            fail_closed(f"Failed to switch to main in {target_repo_name} repo: {e}")

    try:
        run_git(target_repo_path, ["merge", "--ff-only", "origin/main"])
    except Exception as e:
        fail_closed(f"Local main in {target_repo_name} repo cannot fast-forward to origin/main: {e}", state="CANNOT_FAST_FORWARD")

    target_head = run_git(target_repo_path, ["rev-parse", "HEAD"])
    target_origin_main = run_git(target_repo_path, ["rev-parse", "origin/main"])
    if target_head != target_origin_main:
        fail_closed(f"{target_repo_name} repo HEAD ({target_head}) does not match origin/main ({target_origin_main}).")

    # Phase 5: Select Authorised Task Branch
    local_branch_exists = run_git(target_repo_path, ["rev-parse", "--verify", f"refs/heads/{pr_branch}"], check=False) != ""
    remote_branch_exists = run_git(target_repo_path, ["rev-parse", "--verify", f"refs/remotes/origin/{pr_branch}"], check=False) != ""

    if not local_branch_exists and not remote_branch_exists:
        try:
            run_git(target_repo_path, ["switch", "-c", pr_branch, "origin/main"])
        except Exception:
            run_git(target_repo_path, ["checkout", "-b", pr_branch, "origin/main"])
    elif local_branch_exists:
        try:
            run_git(target_repo_path, ["switch", pr_branch])
        except Exception:
            run_git(target_repo_path, ["checkout", pr_branch])
    elif remote_branch_exists:
        try:
            run_git(target_repo_path, ["switch", "-c", pr_branch, f"origin/{pr_branch}"])
        except Exception:
            run_git(target_repo_path, ["checkout", "-b", pr_branch, f"origin/{pr_branch}"])

    selected_branch = run_git(target_repo_path, ["branch", "--show-current"])
    selected_sha = run_git(target_repo_path, ["rev-parse", "HEAD"])

    # Phase 6: Dispatch Decision State
    pr_state = None
    if declared_repo and not allow_custom_slug:
        try:
            res_pr = subprocess.run(
                ["gh", "pr", "view", pr_branch, "--repo", declared_repo, "--json", "state"],
                capture_output=True, text=True
            )
            if res_pr.returncode == 0 and res_pr.stdout.strip():
                pr_info = json.loads(res_pr.stdout)
                pr_state = pr_info.get("state")
        except Exception:
            pass

    if pr_state == "MERGED":
        state = "MERGED_AWAITING_GOVERNANCE_PROMOTION"
    elif pr_state == "CLOSED":
        state = "BLOCKED"
    elif pr_state == "OPEN":
        state = "PR_OPEN"
    else:
        if task_status in ("APPROVED", "IN_PROGRESS"):
            state = "EXECUTE_PROMPT"
        else:
            state = "STOP_BLOCKED"

    result = {
        "ok": True,
        "state": state,
        "active_task": {
            "task": task_name,
            "status": task_status,
            "assigned_identity": assigned_identity,
            "repository": declared_repo,
            "pr_branch": pr_branch,
            "original_prompt": original_prompt,
        },
        "agentops_sha": agentops_head,
        "output_repo": declared_repo,
        "output_sha": selected_sha,
        "selected_branch": selected_branch,
    }

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Score2GP Agy `go` Dispatch Bootstrap Helper.")
    parser.add_argument("--product", type=str, default="../score2gp", help="Path to score2gp product repository")
    parser.add_argument("--agentops", type=str, default=".", help="Path to score2gp-agentops governance repository")
    parser.add_argument("--json", action="store_true", help="Output status in JSON format")
    parser.add_argument("--skip-identity-check", action="store_true", help="Skip user identity verification for test suites")
    parser.add_argument("--allow-custom-slug", action="store_true", help="Allow custom repository slugs for test suites")
    args = parser.parse_args()

    result = run_go_bootstrap(
        agentops_path=args.agentops,
        product_path=args.product,
        skip_identity_check=args.skip_identity_check,
        allow_custom_slug=args.allow_custom_slug,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"State: {result['state']}")
        print(f"Task: {result['active_task']['task']} ({result['active_task']['status']})")
        print(f"AgentOps SHA: {result['agentops_sha']}")
        print(f"Output Repo: {result['output_repo']}")
        print(f"Output Branch: {result['selected_branch']} ({result['output_sha']})")


if __name__ == "__main__":
    main()
