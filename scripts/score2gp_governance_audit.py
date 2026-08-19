#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys

try:
    from scripts.score2gp_orchestrator import load_authority, render_active_task
except ModuleNotFoundError:
    from score2gp_orchestrator import load_authority, render_active_task

try:
    from scripts.score2gp_task_status import (
        EXECUTABLE_TASK_STATUSES,
        KNOWN_TASK_STATUSES,
        PR_LIFECYCLE_TASK_STATUSES,
    )
except ModuleNotFoundError:
    from score2gp_task_status import (
        EXECUTABLE_TASK_STATUSES,
        KNOWN_TASK_STATUSES,
        PR_LIFECYCLE_TASK_STATUSES,
    )

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

FULL_SHA_METADATA = re.compile(r"`?[0-9a-f]{40}`?")
REAPPROVED_HEAD_METADATA = re.compile(
    r"`?[0-9a-f]{40}`?\s+"
    r"\(Re-approved head SHA:\s*`?[0-9a-f]{40}`?\)"
)
REVIEW_ID = re.compile(r"Review ID `?(?:\d+|PRR_[A-Za-z0-9_-]+)`?")


def is_valid_sha_metadata(field_name: str, raw_value: str) -> bool:
    value = raw_value.strip()
    if FULL_SHA_METADATA.fullmatch(value):
        return True
    return (
        field_name == "Product Head SHA"
        and REAPPROVED_HEAD_METADATA.fullmatch(value) is not None
    )


def has_valid_review_id(text: str) -> bool:
    return REVIEW_ID.search(text) is not None


def main():
    print("Running Score2GP Governance Audit...")
    violations = []

    # 1. Check skill files exist
    required_skills = [
        "projects/score2gp/skills/architect/SKILL.md",
        "projects/score2gp/skills/developer/SKILL.md",
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

        authority_path = "projects/score2gp/ORCHESTRATION_STATE.json"
        generated_marker = "Generated from ORCHESTRATION_STATE.json; do not edit directly."
        if generated_marker in content and os.path.exists(authority_path):
            try:
                authority = load_authority(authority_path)
                if authority.get("schema_version") == 2:
                    generated = render_active_task(authority)
                    if content != generated:
                        violations.append(
                            "ACTIVE_TASK.md diverges from generated ORCHESTRATION_STATE.json view."
                        )
            except Exception as error:
                violations.append(f"Cannot validate orchestration authority: {error}")

        if not status:
            violations.append("ACTIVE_TASK.md has no parseable status.")
        elif status not in KNOWN_TASK_STATUSES:
            violations.append(
                f"ACTIVE_TASK.md has unsupported status '{status}'; expected one of: "
                f"{', '.join(sorted(KNOWN_TASK_STATUSES))}."
            )

        branch_relevant_statuses = (
            EXECUTABLE_TASK_STATUSES | PR_LIFECYCLE_TASK_STATUSES
        )

        if status in branch_relevant_statuses and not branch_name:
            violations.append(
                "ACTIVE_TASK.md has an executable status but no parseable PR Branch; "
                "refusing to skip merged-task replay verification."
            )

        if status in branch_relevant_statuses and branch_name:
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

    # 5. Check run record provenance integrity
    runs_dir = "projects/score2gp/runs"
    if os.path.exists(runs_dir):
        for root, _, files in os.walk(runs_dir):
            for f in files:
                if not f.endswith(".md"):
                    continue
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as file_obj:
                    text = file_obj.read()

                # Check for slash-combined reviewer identities
                if re.search(r"tticom-codex\s*/\s*tticomgov-code", text, re.IGNORECASE) or \
                   re.search(r"tticomgov-code\s*/\s*tticom-codex", text, re.IGNORECASE):
                    violations.append(
                        f"Run record {path} combines distinct reviewer identities ('tticom-codex / tticomgov-code'); "
                        "independent reviewer identity must be isolated and distinct from governance publisher."
                    )

                # Check that Independent Reviewer and Governance Publisher are distinct
                reviewer_match = re.search(r"^\*\*Independent Reviewer\*\*:\s*`?(\S+?)`?\s*$", text, re.MULTILINE)
                publisher_match = re.search(r"^\*\*Governance Publisher\*\*:\s*`?(\S+?)`?\s*$", text, re.MULTILINE)
                if reviewer_match and publisher_match:
                    rev_id = reviewer_match.group(1).strip("`")
                    pub_id = publisher_match.group(1).strip("`")
                    if rev_id == pub_id:
                        violations.append(
                            f"Run record {path} sets Independent Reviewer identical to Governance Publisher ('{rev_id}'); "
                            "independent reviewer identity must be distinct from governance publisher."
                        )

                # Check that SHA metadata fields are full 40-character lowercase hex strings
                sha_matches = re.findall(
                    r"^\*\*(Product Main SHA|Product Head SHA|AgentOps Main SHA|Skills Lock SHA)\*\*:\s*(.+?)\s*$",
                    text,
                    re.MULTILINE,
                )
                for field_name, raw_val in sha_matches:
                    if not is_valid_sha_metadata(field_name, raw_val):
                        violations.append(
                            f"Run record {path} field '{field_name}' contains invalid SHA value ('{raw_val.strip()}'); "
                            "SHA metadata must use full lowercase 40-character values and approved syntax."
                        )

                # Check that cited Review ID is present and valid if an approval is claimed
                if "**Review Verdict**: APPROVED" in text and not has_valid_review_id(text):
                    violations.append(
                        f"Run record {path} claims APPROVED review verdict but lacks a valid numeric or GitHub node Review ID citation."
                    )

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
