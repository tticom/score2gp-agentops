#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys

def run_cmd(args):
    try:
        res = subprocess.run(args, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return ""

def main():
    print("Running Score2GP Governance Audit...")
    violations = []

    # 1. Check skill files exist
    required_skills = [
        "projects/score2gp/skills/architect/SKILL.md",
        "projects/score2gp/skills/developer/SKILL.md",
        "projects/score2gp/skills/reviewer/SKILL.md",
        "skills/score2gp-developer.md",
        "skills/score2gp-pr-hard-review.md",
        "skills/score2gp-task-orchestration.md"
    ]
    for skill in required_skills:
        if not os.path.exists(skill):
            violations.append(f"Missing required skill file: {skill}")

    # 2. Check tracked files in agentops
    tracked_files = run_cmd(["git", "ls-files"]).splitlines()
    banned_extensions = (".pdf", ".gp", ".mxl", ".musicxml", ".png", ".html")
    for file in tracked_files:
        if file.startswith("work/") or file.startswith("inspect/") or file.startswith("overlays/"):
            violations.append(f"Banned path tracked in governance repo: {file}")
        if any(file.endswith(ext) for ext in banned_extensions):
            # Verify if it's in templates or allowed docs
            if not file.startswith("projects/score2gp/templates/") and not file.startswith("docs/"):
                violations.append(f"Banned binary/artifact file tracked in governance repo: {file}")

    # 3. Check product automation mentioned in policy docs
    policy_files = ["AGENT-RULES.md", "projects/score2gp/AGENT_CONTROL.md"]
    required_mentions = ["agent_verify.py", "artifact_audit.py", "pr_body.py"]
    for pf in policy_files:
        if not os.path.exists(pf):
            violations.append(f"Policy file missing: {pf}")
            continue
        with open(pf, "r", encoding="utf-8") as f:
            content = f.read()
        for mention in required_mentions:
            if mention not in content:
                violations.append(f"Policy file {pf} does not mention product automation script: {mention}")

    # 4. Check ACTIVE_TASK.md for stale status
    active_task_path = "projects/score2gp/ACTIVE_TASK.md"
    if os.path.exists(active_task_path):
        with open(active_task_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Robust status parsing
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

        # Robust branch parsing
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

        if status in ("APPROVED", "IN_PROGRESS", "PR_OPEN", "CHANGES_REQUESTED") and branch_name:
            # Query gh to see if this branch has a merged PR on product repo
            gh_res = run_cmd(["gh", "pr", "view", branch_name, "--repo", "tticom/score2gp", "--json", "state,merged"])
            if gh_res:
                try:
                    pr_info = json.loads(gh_res)
                    if pr_info.get("state") == "MERGED" or pr_info.get("merged") is True:
                        violations.append(f"ACTIVE_TASK.md status is stale ({status}) for branch '{branch_name}' which is already MERGED on product repo.")
                except Exception:
                    pass

    if violations:
        print("\n=== GOVERNANCE AUDIT FAIL ===")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)

    print("\n=== GOVERNANCE AUDIT PASS ===")
    print("All governance safety and automation reference checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
