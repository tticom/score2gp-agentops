#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys

def run_git(cwd, args, check=True):
    try:
        res = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, check=check)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        if check:
            raise
        return ""
    except Exception as e:
        if check:
            raise RuntimeError(f"Failed to run git command {args} in {cwd}: {e}")
        return ""

def get_repo_slug(cwd):
    remote_url = run_git(cwd, ["config", "--get", "remote.origin.url"], check=False)
    if remote_url:
        m = re.search(r"github\.com[:/]([^/]+/[^/.]+)", remote_url)
        if m:
            return m.group(1)
    return ""

def run_cmd(args):
    try:
        res = subprocess.run(args, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return ""

def get_prs(repo_slug):
    if not repo_slug:
        return [], []
    open_prs = []
    merged_prs = []

    # Open PRs
    res_open = run_cmd(["gh", "pr", "list", "--repo", repo_slug, "--limit", "5", "--json", "number,title,state,headRefName"])
    if res_open:
        try:
            open_prs = json.loads(res_open)
        except Exception:
            pass

    # Merged PRs
    res_merged = run_cmd(["gh", "pr", "list", "--repo", repo_slug, "--state", "merged", "--limit", "5", "--json", "number,title,state,mergeCommit,headRefName"])
    if res_merged:
        try:
            merged_prs = json.loads(res_merged)
        except Exception:
            pass

    return open_prs, merged_prs

def parse_active_task(agentops_path):
    active_task_path = os.path.join(agentops_path, "projects/score2gp/ACTIVE_TASK.md")
    if not os.path.exists(active_task_path):
        return None, None

    with open(active_task_path, "r", encoding="utf-8") as f:
        content = f.read()

    status = ""
    lines = content.splitlines()
    for idx, line in enumerate(lines):
        if "## Status" in line or "**Status**" in line:
            for next_line in lines[idx+1:idx+5]:
                nl = next_line.strip()
                if nl and not nl.startswith("#"):
                    status = nl.upper()
                    break
            if status:
                break

    branch_name = ""
    for idx, line in enumerate(lines):
        if "Branch Suggestion" in line or "Branch:" in line or "**Branch**" in line:
            m = re.search(r"`([^`]+)`", line)
            if m:
                branch_name = m.group(1)
                break
            for next_line in lines[idx+1:idx+3]:
                nl = next_line.strip()
                if nl:
                    m2 = re.search(r"`([^`]+)`", nl)
                    if m2:
                        branch_name = m2.group(1)
                    else:
                        branch_name = nl
                    break
            if branch_name:
                break

    return status, branch_name

def parse_status_value(line: str) -> str:
    m = re.search(r"(?:Status|\*\*Status\*\*)\s*:\s*`?([^`\n\r\t]+)`?", line, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return ""

def get_next_approved_task(agentops_path):
    queue_path = os.path.join(agentops_path, "projects/score2gp/APPROVED_TASK_QUEUE.md")
    if not os.path.exists(queue_path):
        return None, []

    with open(queue_path, "r", encoding="utf-8") as f:
        content = f.read()

    tasks_sections = re.split(r"(?=^## Task \d+)", content, flags=re.MULTILINE)
    next_approved = None
    gated_tasks = []

    for section in tasks_sections:
        lines = section.splitlines()
        if not lines:
            continue
        title = lines[0].strip("# ")

        section_status = ""
        for line in lines:
            val = parse_status_value(line)
            if val:
                section_status = val
                break

        if section_status == "APPROVED":
            if not next_approved:
                next_approved = title
        elif "APPROVED" in section_status.upper():
            gated_tasks.append(f"{title} (Status: {section_status})")

    return next_approved, gated_tasks

def get_branch_sync_status(cwd, branch_name):
    if not branch_name or branch_name == "HEAD":
        return "Unknown"
    upstream = run_git(cwd, ["rev-parse", "--abbrev-ref", f"{branch_name}@{{u}}"], check=False)
    if not upstream:
        return "No Upstream"

    left_right = run_git(cwd, ["rev-list", "--left-right", "--count", f"{branch_name}...{upstream}"], check=False)
    if left_right:
        try:
            ahead, behind = map(int, left_right.split())
            if ahead == 0 and behind == 0:
                return "Synced"
            elif ahead > 0 and behind == 0:
                return f"Ahead {ahead} commits"
            elif ahead == 0 and behind > 0:
                return f"Behind {behind} commits"
            else:
                return f"Diverged (Ahead {ahead}, Behind {behind})"
        except Exception:
            pass
    return "Unknown"

def fail_closed(reason, action="stop: bootstrap failed"):
    bootstrap_data = {
        "ok": False,
        "suggested_next_action": {
            "action": action,
            "reason": reason
        }
    }
    if "--json" in sys.argv:
        print(json.dumps(bootstrap_data, indent=2))
    else:
        print("# Score2GP Workspace Bootstrap Status\n")
        print(f"## Suggested Next Action: `{action}`")
        print(f"**Reason**: {reason}\n")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Bootstrap and reconstruct Score2GP workspace state.")
    parser.add_argument("--product", type=str, default="../score2gp", help="Path to score2gp product repository")
    parser.add_argument("--agentops", type=str, default=".", help="Path to score2gp-agentops governance repository")
    parser.add_argument("--json", action="store_true", help="Output status in JSON format")
    args = parser.parse_args()

    prod_path = os.path.abspath(args.product)
    gov_path = os.path.abspath(args.agentops)

    # 1. Validate both repositories strictly (P1 blocker)
    for name, path, expected_slug in [("product", prod_path, "tticom/score2gp"), ("governance", gov_path, "tticom/score2gp-agentops")]:
        if not os.path.exists(path):
            fail_closed(f"The specified {name} path does not exist: {path}")
        if not os.path.isdir(path):
            fail_closed(f"The specified {name} path is not a directory: {path}")

        # Check if inside git work tree
        try:
            inside_worktree = run_git(path, ["rev-parse", "--is-inside-work-tree"])
            if inside_worktree != "true":
                fail_closed(f"The specified {name} path is not inside a git work tree: {path}")
        except Exception:
            fail_closed(f"Failed to verify git work tree for {name} repository at {path}")

        # Check remote origin slug
        slug = get_repo_slug(path)
        if not slug:
            fail_closed(f"Could not retrieve remote origin URL/slug for {name} repository at {path}")
        if slug.lower() != expected_slug.lower():
            fail_closed(f"Validation failed: expected slug '{expected_slug}' for {name} repository, got '{slug}' at {path}")

        # Refresh repo (fetch/prune) before reading state (P1 blocker)
        try:
            run_git(path, ["fetch", "--all", "--prune"])
        except Exception as e:
            fail_closed(f"Failed to fetch/prune upstream for {name} repository at {path}: {e}")

    # 2. Product Repo Git Details
    prod_branch = run_git(prod_path, ["branch", "--show-current"])
    if not prod_branch:
        prod_branch = run_git(prod_path, ["rev-parse", "--abbrev-ref", "HEAD"])
    prod_sha = run_git(prod_path, ["rev-parse", "HEAD"])
    prod_status = "Clean" if not run_git(prod_path, ["status", "--porcelain"]) else "Dirty"
    prod_commits = run_git(prod_path, ["log", "--oneline", "-3"]).splitlines()
    prod_sync = get_branch_sync_status(prod_path, prod_branch)

    # 3. Agentops Repo Git Details
    gov_branch = run_git(gov_path, ["branch", "--show-current"])
    if not gov_branch:
        gov_branch = run_git(gov_path, ["rev-parse", "--abbrev-ref", "HEAD"])
    gov_sha = run_git(gov_path, ["rev-parse", "HEAD"])
    gov_status = "Clean" if not run_git(gov_path, ["status", "--porcelain"]) else "Dirty"
    gov_commits = run_git(gov_path, ["log", "--oneline", "-3"]).splitlines()
    gov_sync = get_branch_sync_status(gov_path, gov_branch)

    # 4. Pull Requests
    prod_slug = get_repo_slug(prod_path)
    gov_slug = get_repo_slug(gov_path)

    prod_open_prs, prod_merged_prs = get_prs(prod_slug)
    gov_open_prs, gov_merged_prs = get_prs(gov_slug)

    # 5. Active Task & Approved Queue (P2 blocker)
    active_task_status, active_branch = parse_active_task(gov_path)
    next_approved, gated_queue = get_next_approved_task(gov_path)

    # 6. Product Artifact Audit
    audit_script = os.path.join(prod_path, "scripts/artifact_audit.py")
    if not os.path.exists(audit_script):
        fail_closed("Required artifact audit script (scripts/artifact_audit.py) is missing.", "stop: artifact audit unavailable")

    res = subprocess.run([sys.executable, audit_script], cwd=prod_path, capture_output=True, text=True)
    audit_pass = (res.returncode == 0)
    audit_output = res.stdout.strip() if audit_pass else res.stdout.strip() + "\n" + res.stderr.strip()

    if not audit_pass:
        fail_closed(f"Product artifact audit failed:\n{audit_output}", "stop: artifact audit failure")

    # 7. Suggested Action Logic
    suggested_action = "stop: no active task"
    reason = "No approved active task is set."

    if active_task_status in ("APPROVED", "IN_PROGRESS", "PR_OPEN", "CHANGES_REQUESTED") and active_branch:
        is_merged = False
        for pr in prod_merged_prs:
            if pr.get("headRefName") == active_branch:
                is_merged = True
                break
        if not is_merged:
            try:
                res = subprocess.run(
                    ["gh", "pr", "view", active_branch, "--repo", "tticom/score2gp", "--json", "state"],
                    capture_output=True, text=True
                )
                if res.returncode != 0 or not res.stdout.strip():
                    suggested_action = "review: state incomplete"
                    reason = f"Unable to verify active task branch status on GitHub: {active_branch}"
                    is_merged = None
                else:
                    try:
                        pr_info = json.loads(res.stdout)
                        if pr_info.get("state") == "MERGED":
                            is_merged = True
                    except Exception:
                        suggested_action = "review: state incomplete"
                        reason = f"Unable to verify active task branch status on GitHub: {active_branch} (JSON parse error)"
                        is_merged = None
            except Exception as e:
                suggested_action = "review: state incomplete"
                reason = f"Unable to verify active task branch status on GitHub: {active_branch} (subprocess error: {e})"
                is_merged = None

        if is_merged is True:
            suggested_action = "stop: stale active task"
            reason = f"Active task branch '{active_branch}' is already merged in the product repository."
        elif is_merged is False:
            suggested_action = "continue: active approved task"
            reason = f"Active task is in progress on branch '{active_branch}'."
    else:
        if prod_open_prs or gov_open_prs:
            suggested_action = "review: PR open"
            reason = "Open Pull Requests exist that require conformance review or verification."
        elif next_approved:
            suggested_action = "continue: active approved task"
            reason = f"Next approved task '{next_approved}' is ready to be promoted."

    # Hint for product test command
    test_hints = ["make verify", "python3 scripts/agent_verify.py"]

    bootstrap_data = {
        "ok": True,
        "product_repo": {
            "branch": prod_branch,
            "sha": prod_sha,
            "status": prod_status,
            "sync_status": prod_sync,
            "commits": prod_commits,
            "open_prs": prod_open_prs,
            "latest_merged_prs": prod_merged_prs,
        },
        "agentops_repo": {
            "branch": gov_branch,
            "sha": gov_sha,
            "status": gov_status,
            "sync_status": gov_sync,
            "commits": gov_commits,
            "open_prs": gov_open_prs,
            "latest_merged_prs": gov_merged_prs,
        },
        "active_task": {
            "status": active_task_status,
            "branch": active_branch,
        },
        "next_approved_queue_item": next_approved,
        "gated_queue_items": gated_queue,
        "artifact_audit": {
            "pass": audit_pass,
            "output": audit_output,
        },
        "suggested_next_action": {
            "action": suggested_action,
            "reason": reason,
        },
        "test_command_hints": test_hints,
    }

    if args.json:
        print(json.dumps(bootstrap_data, indent=2))
        return

    # Print Markdown output
    print("# Score2GP Workspace Bootstrap Status\n")
    print(f"## Suggested Next Action: `{suggested_action}`")
    print(f"**Reason**: {reason}\n")

    print("## 1. Product Repository (`score2gp`)")
    print(f"- **Branch**: `{prod_branch}` ({prod_sync})")
    print(f"- **SHA**: `{prod_sha}`")
    print(f"- **Working Tree Status**: `{prod_status}`")
    print("- **Recent Commits**:")
    for c in prod_commits:
        print(f"  - {c}")
    print("- **Open PRs**:")
    for pr in prod_open_prs:
        print(f"  - PR #{pr['number']}: {pr['title']} (`{pr['headRefName']}`)")
    if not prod_open_prs:
        print("  - None.")

    print("\n## 2. Governance Repository (`score2gp-agentops`)")
    print(f"- **Branch**: `{gov_branch}` ({gov_sync})")
    print(f"- **SHA**: `{gov_sha}`")
    print(f"- **Working Tree Status**: `{gov_status}`")
    print("- **Recent Commits**:")
    for c in gov_commits:
        print(f"  - {c}")
    print("- **Open PRs**:")
    for pr in gov_open_prs:
        print(f"  - PR #{pr['number']}: {pr['title']} (`{pr['headRefName']}`)")
    if not gov_open_prs:
        print("  - None.")

    print("\n## 3. Governance Status")
    print(f"- **Active Task Status**: `{active_task_status}`")
    print(f"- **Active Task Branch**: `{active_branch}`")
    print(f"- **Next Approved Queue Item**: `{next_approved}`")
    print("- **Gated Queue Items**:")
    for item in gated_queue:
        print(f"  - {item}")
    if not gated_queue:
        print("  - None.")

    print("\n## 4. Safety & Verification Audit")
    print(f"- **Artifact Audit Status**: `{'🟢 PASS' if audit_pass else '🔴 FAIL'}`")
    print(f"- **Test Command Hints**: `{', '.join(test_hints)}`")

if __name__ == "__main__":
    main()
