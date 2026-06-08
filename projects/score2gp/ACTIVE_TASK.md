# Active Task: score2gp

Status:
ACTIVE

Execution source:
`projects/score2gp/APPROVED_TASK_QUEUE.md`

Current product baseline after product PR #203:
`0b73bd90898bc1f5a1bda6f5e61920d1e952c7f9`

Agents may execute this task only inside its written scope.

Agents must stop at READY_FOR_HUMAN_MERGE for every product or governance PR. Human merge is still required for every PR.

Agents must not skip, reorder, invent, or materially edit queue items.

## Current Active Task

## Task 7 — Record post-#203 product baseline

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
review/post-schema-snapshot-product-baseline-v0.1

PR title:
docs(review): record post-schema-snapshot product baseline

Purpose:
Record the exact product baseline after PR #203 so later agents have a durable reference point.

Allowed governance files:
- projects/score2gp/reviews/2026-06-08-post-schema-snapshot-product-baseline.md
- projects/score2gp/APPROVED_TASK_QUEUE.md
- projects/score2gp/ACTIVE_TASK.md

Product repo access:
Read-only.

Required evidence:
- product main commit SHA
- recent merged PRs #197-#203
- fixture files present
- schema snapshot file present
- targeted tests
- full pytest if reasonable
- privacy/artifact check

Validation:
cd /home/tticom/work/score2gp-workspace/score2gp
git fetch --all --prune
git switch main
git pull --ff-only human main
git status --short
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py
.venv/bin/python -m pytest tests/test_pdf_staff_geometry_diagnostics.py
.venv/bin/python -m pytest

Acceptance criteria:
- baseline review record exists
- exact commit SHA recorded
- test evidence recorded
- known limitations recorded
- no product files changed

Stop conditions:
- product main is dirty
- tests fail
- product baseline cannot be verified
