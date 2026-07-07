# Pull Request Description Template

This template outlines the PR structure generated automatically by `scripts/pr_body.py`. When opening a PR, run:
```bash
python scripts/pr_body.py --title "PR Title" --summary "Summary details"
```

## Structure Overview

### 1. Title
Format: `type(scope): description` (e.g. `feat(bridge): add parallel timing`)

### 2. Summary
High-level explanation of changes and design decisions.

### 3. Proposed Changes
List of modified file paths relative to `main`.

### 4. Verification Output
A collapsible details section nesting the contents of `work/agent_verify.md` (pytest results, schemas exported/validated, check diff status).

### 5. Private-Safety & Repository Hygiene Audit
The outcome of running `scripts/artifact_audit.py` (which must be 🟢 PASS).

### 6. Known Limitations & Reviewer Focus
Any non-goals or specific focus points for reviewers.
