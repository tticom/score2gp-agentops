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


def parse_active_task_state(content: str) -> tuple[str, str, str]:
    """Return normalized status, repository, and branch from the task contract.

    ACTIVE_TASK.md uses bold metadata fields.  Keep legacy section parsing for
    older task records, but do not silently skip the current ``**PR Branch**``
    spelling: doing so can allow an already-merged task to be promoted again.
    """
    status_match = re.search(r"^\*\*Status\*\*:\s*(.+?)\s*$", content, re.MULTILINE)
    branch_match = re.search(
        r"^\*\*PR Branch\*\*:\s*`([^`]+)`\s*$", content, re.MULTILINE
    )
    repository_match = re.search(
        r"^\*\*Repository\*\*:\s*(\S+)\s*$", content, re.MULTILINE
    )
    status = status_match.group(1).strip().upper() if status_match else ""
    branch_name = branch_match.group(1).strip() if branch_match else ""
    repository = (
        repository_match.group(1).strip()
        if repository_match
        else "tticom/score2gp"
    )

    lines = content.splitlines()
    if not status:
        for idx, line in enumerate(lines):
            if "## Status" in line:
                for next_line in lines[idx + 1:idx + 5]:
                    value = next_line.strip()
                    if value and not value.startswith("#"):
                        status = value.upper()
                        break
                if status:
                    break

    if not branch_name:
        for idx, line in enumerate(lines):
            if "Branch Suggestion" in line or "**Branch**" in line:
                match = re.search(r"`([^`]+)`", line)
                if match:
                    branch_name = match.group(1).strip()
                    break
                for next_line in lines[idx + 1:idx + 3]:
                    value = next_line.strip()
                    if not value:
                        continue
                    nested_match = re.search(r"`([^`]+)`", value)
                    branch_name = (
                        nested_match.group(1).strip() if nested_match else value
                    )
                    break
                if branch_name:
                    break

    return status, repository, branch_name

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
        file_lower = file.lower()
        if file_lower.startswith("work/") or file_lower.startswith("inspect/") or file_lower.startswith("overlays/"):
            violations.append(f"Banned path tracked in governance repo: {file}")
        if any(file_lower.endswith(ext) for ext in banned_extensions):
            # Verify if it's in templates or allowed docs
            if not file_lower.startswith("projects/score2gp/templates/") and not file_lower.startswith("docs/"):
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

        status, repository, branch_name = parse_active_task_state(content)

        if status in ("APPROVED", "IN_PROGRESS", "PR_OPEN", "CHANGES_REQUESTED") and not branch_name:
            violations.append(
                "ACTIVE_TASK.md has an executable status but no parseable PR Branch; "
                "refusing to skip merged-task replay verification."
            )

        if status in ("APPROVED", "IN_PROGRESS", "PR_OPEN", "CHANGES_REQUESTED") and branch_name:
            # Query gh to see if a PR exists for this branch and whether it is already merged
            try:
                res = subprocess.run(
                    ["gh", "pr", "list", "--repo", repository, "--head", branch_name, "--state", "all", "--json", "number,state"],
                    capture_output=True, text=True
                )
                if res.returncode != 0:
                    violations.append(f"Unable to verify active task branch against GitHub: {branch_name} ({res.stderr.strip()})")
                elif res.stdout.strip():
                    try:
                        matches = json.loads(res.stdout)
                        for pr_info in matches:
                            if pr_info.get("state") == "MERGED":
                                violations.append(
                                    f"ACTIVE_TASK.md status is stale ({status}) for branch '{branch_name}' which is already MERGED on {repository}."
                                )
                                break
                    except Exception as json_err:
                        violations.append(f"Unable to verify active task branch against GitHub: {branch_name} (JSON parse error: {json_err})")
            except Exception as e:
                violations.append(f"Unable to verify active task branch against GitHub: {branch_name} (subprocess error: {e})")

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
