#!/usr/bin/env python3
import argparse
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

def redact_sensitive_data(text):
    import re
    # Redact paths
    text = re.sub(r'/[a-zA-Z0-9_.-]+(?:/[a-zA-Z0-9_.-]+)+', '[REDACTED]', text)
    # Redact credentials/tokens/emails (key=value, key: value, emails)
    text = re.sub(r'([a-zA-Z0-9_-]*(?:token|password|secret|key|cred|auth|email)[a-zA-Z0-9_-]*\s*[\"=:]+\s*(?:Bearer\s+|Basic\s+)?).*', r'\g<1>[REDACTED]', text, flags=re.IGNORECASE)
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[REDACTED]', text)
    return text

def summarize_report(raw_text):
    sanitized = [
        "*Sanitized Verification Report*",
        "Raw stdout and stderr are omitted to prevent disclosure of private data.",
    ]

    counts = {"PASS": 0, "FAIL": 0, "WARNING": 0}
    has_table = any(line.startswith("|") and len(line.split("|")) >= 3 for line in raw_text.splitlines())
    for line in raw_text.splitlines():
        status_target = None
        if line.startswith("|") and len(line.split("|")) >= 3:
            parts = [p.strip() for p in line.split("|")]
            status_target = parts[2].upper()
        elif not has_table and line.startswith("- **Status**:"):
            status_target = line.split(":", 1)[1].upper()
        elif not has_table and (line.startswith("PASS:") or line.startswith("FAIL:") or line.startswith("WARNING:")):
            status_target = line.upper()

        if status_target:
            if "PASS" in status_target:
                counts["PASS"] += 1
            elif "FAIL" in status_target:
                counts["FAIL"] += 1
            elif "WARNING" in status_target:
                counts["WARNING"] += 1

    for status in ("PASS", "FAIL", "WARNING"):
        if counts[status]:
            sanitized.append(f"{status}: {counts[status]} reported")

    return "\n".join(sanitized)

def main():
    parser = argparse.ArgumentParser(description="Generate PR body for Score2GP.")
    parser.add_argument("--title", type=str, default="[PR Title]", help="Title of the PR")
    parser.add_argument("--summary", type=str, default="[PR Summary]", help="Detailed summary of changes")
    parser.add_argument("--limitations", type=str, default="None.", help="Known limitations or non-goals")
    parser.add_argument("--review-focus", type=str, default="Verification and correctness checks.", help="Instructions or focus areas for the reviewer")
    parser.add_argument("--base", type=str, default="main", help="Base branch for git diff checks")
    args = parser.parse_args()

    # Get changed files
    changed_files_raw = run_cmd(["git", "diff", "--name-only", args.base])
    changed_files = changed_files_raw.splitlines() if changed_files_raw else []

    # Get verification report
    verify_report = ""
    verify_md_path = "work/agent_verify.md"
    if os.path.exists(verify_md_path):
        try:
            with open(verify_md_path, "r", encoding="utf-8") as f:
                raw_report = f.read().strip()
                verify_report = summarize_report(raw_report)
        except OSError:
            verify_report = "Error reading verification report: I/O error occurred."
    else:
        verify_report = "*No verification report found. Run python scripts/agent_verify.py first.*"

    # Compile the final PR body
    lines = []
    lines.append(f"# {args.title}\n")
    lines.append("## Summary")
    lines.append(args.summary + "\n")

    lines.append("## Proposed Changes")
    if changed_files:
        for file in changed_files:
            lines.append(f"- `{file}`")
    else:
        lines.append("- *No files changed relative to base branch.*")
    lines.append("")

    lines.append("## Verification Output")
    # Nest verification report inside a collapsible details block for cleanliness
    lines.append("<details>")
    lines.append("<summary>View Verification Details</summary>\n")
    lines.append(verify_report)
    lines.append("</details>\n")

    lines.append("## Private-Safety & Repository Hygiene Audit")
    # Read artifact audit status
    python_bin = sys.executable
    audit_res = subprocess.run([python_bin, "scripts/artifact_audit.py"], capture_output=True, text=True)
    if audit_res.returncode == 0:
        lines.append("🟢 **PASS**: Repository hygiene checks succeeded. No private fixtures or generated artifacts are tracked.")
    else:
        lines.append("🔴 **FAIL**: Repository hygiene checks failed. The following tracked files violate privacy policy:")
        lines.append(
            "Raw audit output is intentionally omitted; inspect it only in the local workspace."
        )
    lines.append("")

    lines.append("## Known Limitations")
    lines.append(args.limitations + "\n")

    lines.append("## Reviewer Focus")
    lines.append(args.review_focus)

    print("\n".join(lines))

if __name__ == "__main__":
    main()
