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

try:
    from scripts.score2gp_control_plane import (
        materialize_and_activate_skills,
        read_skills_pin,
        sync_main,
    )
except ModuleNotFoundError:  # Direct execution: python scripts/score2gp_go_bootstrap.py
    from score2gp_control_plane import (
        materialize_and_activate_skills,
        read_skills_pin,
        sync_main,
    )


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


def verify_identity_and_workspace(agentops_path: Path, product_path: Path) -> None:
    """Enforce strict Linux user, home, GitHub CLI, Git identity and WSL workspace gates for tticom-automation."""
    try:
        whoami = subprocess.run(["whoami"], capture_output=True, text=True, check=True).stdout.strip()
    except Exception as e:
        fail_closed(f"Failed to check whoami: {e}", state="IDENTITY_GATE_FAILED")
    if whoami != "tticom-automation":
        fail_closed(f"Linux user must be 'tticom-automation', got '{whoami}'", state="IDENTITY_GATE_FAILED")

    home = os.environ.get("HOME", "")
    if home != "/home/tticom-automation":
        fail_closed(f"HOME must be '/home/tticom-automation', got '{home}'", state="IDENTITY_GATE_FAILED")

    try:
        gh_user = subprocess.run(["gh", "api", "user", "--jq", ".login"], capture_output=True, text=True, check=True).stdout.strip()
    except Exception as e:
        fail_closed(f"Failed to verify gh CLI user: {e}", state="IDENTITY_GATE_FAILED")
    if gh_user != "tticom-automation":
        fail_closed(f"GitHub CLI account must be 'tticom-automation', got '{gh_user}'", state="IDENTITY_GATE_FAILED")

    git_user = run_git(agentops_path, ["config", "--global", "--get", "user.name"], check=False)
    if git_user != "tticom-automation":
        fail_closed(f"Git global user.name must be 'tticom-automation', got '{git_user}'", state="IDENTITY_GATE_FAILED")

    git_email = run_git(agentops_path, ["config", "--global", "--get", "user.email"], check=False)
    if git_email != "tticomautomation@gmail.com":
        fail_closed(f"Git global user.email must be 'tticomautomation@gmail.com', got '{git_email}'", state="IDENTITY_GATE_FAILED")

    canonical_root = Path("/home/tticom-automation/work/score2gp-workspace").resolve()
    for name, path in [("agentops", agentops_path), ("product", product_path)]:
        real_path = path.resolve()
        try:
            real_path.relative_to(canonical_root)
        except ValueError:
            fail_closed(
                f"Workspace path for {name} ({real_path}) is not within canonical workspace root '{canonical_root}'",
                state="WORKSPACE_GATE_FAILED",
            )


def query_github_pr_state(declared_repo: str, pr_branch: str) -> dict[str, Any] | None:
    """Query GitHub API for exact PR state, failing closed on API/auth/network errors."""
    try:
        res_pr = subprocess.run(
            ["gh", "pr", "view", pr_branch, "--repo", declared_repo, "--json", "number,state,headRefOid"],
            capture_output=True, text=True
        )
    except Exception as e:
        fail_closed(f"GitHub CLI execution failed for {declared_repo} {pr_branch}: {e}", state="GITHUB_STATE_UNAVAILABLE")

    if res_pr.returncode == 0:
        if not res_pr.stdout.strip():
            fail_closed(f"GitHub CLI returned empty output for PR query on {declared_repo} {pr_branch}", state="GITHUB_STATE_UNAVAILABLE")
        try:
            return json.loads(res_pr.stdout)
        except Exception as e:
            fail_closed(f"Failed to parse GitHub PR JSON response: {e}", state="GITHUB_STATE_UNAVAILABLE")

    stderr = res_pr.stderr.strip().lower()
    if "no pull requests match" in stderr or "no open pull requests" in stderr or "could not resolve to a pull request" in stderr:
        return None

    fail_closed(f"GitHub PR lookup failed with exit code {res_pr.returncode}: {res_pr.stderr.strip()}", state="GITHUB_STATE_UNAVAILABLE")
    return None


def run_go_bootstrap(
    agentops_path: str | Path,
    product_path: str | Path,
    _skip_identity_check: bool = False,
    _allow_custom_slug: bool = False,
    _gh_runner: Any = None,
) -> dict[str, Any]:
    agentops_path = Path(agentops_path).resolve()
    product_path = Path(product_path).resolve()

    # Phase 1: Identity & Cleanliness
    if not _skip_identity_check:
        verify_identity_and_workspace(agentops_path, product_path)

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

    # Enforce Assigned Identity == tticom-automation
    if assigned_identity.lower() != "tticom-automation":
        fail_closed(
            f"Active task '{task_name}' is assigned to identity '{assigned_identity}', not 'tticom-automation'. Agy must not execute tasks assigned to other identities.",
            state="ASSIGNED_IDENTITY_MISMATCH",
        )

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
        if _allow_custom_slug:
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

    # Phase 5: Query Live GitHub PR State First
    pr_state = None
    pr_head_sha = None
    pr_number = None

    if _gh_runner is not None:
        try:
            pr_info = _gh_runner(declared_repo, pr_branch)
            if pr_info:
                pr_state = pr_info.get("state")
                pr_head_sha = pr_info.get("headRefOid")
                pr_number = pr_info.get("number")
        except Exception as e:
            fail_closed(f"GitHub runner failed: {e}", state="GITHUB_STATE_UNAVAILABLE")
    elif declared_repo and not _allow_custom_slug:
        pr_info = query_github_pr_state(declared_repo, pr_branch)
        if pr_info:
            pr_number = pr_info.get("number")
            pr_state = pr_info.get("state")
            pr_head_sha = pr_info.get("headRefOid")

    # Phase 6: Select Authorised Task Branch with strict reconciliation
    local_branch_exists = run_git(target_repo_path, ["rev-parse", "--verify", f"refs/heads/{pr_branch}"], check=False) != ""
    remote_branch_exists = run_git(target_repo_path, ["rev-parse", "--verify", f"refs/remotes/origin/{pr_branch}"], check=False) != ""

    if not local_branch_exists and not remote_branch_exists:
        try:
            run_git(target_repo_path, ["switch", "-c", pr_branch, "origin/main"])
        except Exception:
            run_git(target_repo_path, ["checkout", "-b", pr_branch, "origin/main"])
    elif local_branch_exists:
        merge_base = run_git(target_repo_path, ["merge-base", pr_branch, "origin/main"], check=False)
        origin_main_sha = run_git(target_repo_path, ["rev-parse", "origin/main"])

        if merge_base != origin_main_sha:
            local_sha = run_git(target_repo_path, ["rev-parse", pr_branch])
            if pr_head_sha and local_sha == pr_head_sha:
                pass
            else:
                fail_closed(
                    f"Existing local branch '{pr_branch}' is not descended from origin/main and has unexplained divergence.",
                    state="DIVERGENT_LOCAL_BRANCH",
                )

        try:
            run_git(target_repo_path, ["switch", pr_branch])
        except Exception:
            run_git(target_repo_path, ["checkout", pr_branch])

        if remote_branch_exists:
            try:
                run_git(target_repo_path, ["merge", "--ff-only", f"origin/{pr_branch}"])
            except Exception as e:
                local_sha = run_git(target_repo_path, ["rev-parse", pr_branch])
                remote_sha = run_git(target_repo_path, ["rev-parse", f"origin/{pr_branch}"])
                if pr_head_sha and local_sha == pr_head_sha:
                    pass
                else:
                    fail_closed(
                        f"Local branch '{pr_branch}' ({local_sha}) cannot fast-forward to origin/{pr_branch} ({remote_sha}): {e}",
                        state="CANNOT_FAST_FORWARD_TASK_BRANCH",
                    )
    elif remote_branch_exists:
        try:
            run_git(target_repo_path, ["switch", "-c", pr_branch, f"origin/{pr_branch}"])
        except Exception:
            run_git(target_repo_path, ["checkout", "-b", pr_branch, f"origin/{pr_branch}"])

    # Final reconciliation of selected branch and SHA
    selected_branch = run_git(target_repo_path, ["branch", "--show-current"])
    selected_sha = run_git(target_repo_path, ["rev-parse", "HEAD"])

    if selected_branch != pr_branch:
        fail_closed(
            f"Selected branch '{selected_branch}' does not match authorised task branch '{pr_branch}'",
            state="BRANCH_SELECTION_FAILED",
        )

    if pr_head_sha:
        if selected_sha != pr_head_sha:
            res_ancestor = subprocess.run(
                ["git", "merge-base", "--is-ancestor", pr_head_sha, selected_sha],
                cwd=str(target_repo_path),
                capture_output=True,
                text=True,
            )
            if res_ancestor.returncode == 0:
                fail_closed(
                    f"Selected local branch head ({selected_sha}) is ahead of live PR head SHA ({pr_head_sha}). Unpushed local commits present.",
                    state="LOCAL_BRANCH_AHEAD_OF_PR",
                )
            else:
                fail_closed(
                    f"Selected branch head ({selected_sha}) does not match live PR head SHA ({pr_head_sha}) and is not descended from it.",
                    state="MISMATCHED_PR_HEAD",
                )
    elif remote_branch_exists:
        remote_branch_sha = run_git(target_repo_path, ["rev-parse", f"origin/{pr_branch}"])
        if selected_sha != remote_branch_sha:
            res_ancestor = subprocess.run(
                ["git", "merge-base", "--is-ancestor", remote_branch_sha, selected_sha],
                cwd=str(target_repo_path),
                capture_output=True,
                text=True,
            )
            if res_ancestor.returncode == 0:
                fail_closed(
                    f"Selected local branch head ({selected_sha}) is ahead of remote branch SHA ({remote_branch_sha}). Unpushed local commits present.",
                    state="LOCAL_BRANCH_AHEAD_OF_REMOTE_BRANCH",
                )
            else:
                fail_closed(
                    f"Selected branch head ({selected_sha}) does not match remote branch SHA ({remote_branch_sha}) and is not descended from it.",
                    state="MISMATCHED_REMOTE_BRANCH_HEAD",
                )

    # Phase 7: Machine-Actionable Dispatch Decision
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
        "pr_number": pr_number,
    }

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Score2GP Agy `go` Dispatch Bootstrap Helper.")
    parser.add_argument("--product", type=str, default="../score2gp", help="Path to score2gp product repository")
    parser.add_argument("--agentops", type=str, default=".", help="Path to score2gp-agentops governance repository")
    parser.add_argument("--skills-repo", type=str, default="../../agy-skills", help="Path to identity-owned agy-skills repository")
    parser.add_argument("--json", action="store_true", help="Output status in JSON format")
    args = parser.parse_args()

    agentops_path = Path(args.agentops).resolve()
    product_path = Path(args.product).resolve()
    sync_main(agentops_path, "agentops")
    sync_main(product_path, "product")
    skills_sha = materialize_and_activate_skills(
        Path(args.skills_repo).resolve(), read_skills_pin(agentops_path)
    )

    result = run_go_bootstrap(
        agentops_path=agentops_path,
        product_path=product_path,
    )
    result["skills_sha"] = skills_sha

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"State: {result['state']}")
        print(f"Task: {result['active_task']['task']} ({result['active_task']['status']})")
        print(f"AgentOps SHA: {result['agentops_sha']}")
        print(f"Skills SHA: {result['skills_sha']}")
        print(f"Output Repo: {result['output_repo']}")
        print(f"Output Branch: {result['selected_branch']} ({result['output_sha']})")


if __name__ == "__main__":
    main()
