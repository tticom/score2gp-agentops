## Current Active Task

## Task 63 — Execute raster diagnostics corpus review against private fixtures

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-63-raster-diagnostics-corpus-review-v0.1`

PR title:
`docs(score2gp): execute raster diagnostics corpus review against private fixtures`

Context:
Task 63 is a read-only evaluation task in the governance repo.
Task 63 must review the locally generated, untracked smoke-script JSON outputs for the raster diagnostics across private fixtures.
Task 63 evaluates these outputs against ground truth explicitly established by human-reviewed private fixture expectations or fixture-level manual review.
Task 63 will produce a governance review table listing fixture/page/staff, expected opening-symbol status, observed summary label, false-positive/false-negative classification, and notes.
Task 63 does not authorise recogniser implementation or product semantic promotion.

Goal:
Create a governance PR that adds the corpus review table and documents the false positive rate, false negative rate, and staff-line exclusion performance of the current proportional heuristics.

Non-goals:
- Do not modify the product repo.
- Do not implement code.
- Do not create or modify tests.
- Do not create fixtures.
- Do not add screenshots, rendered images, logs, debug dumps, PDFs, GP files, or local artifacts.
- Do not authorise ScoreIR emission.
- Do not authorise recognised clef objects.
- Do not authorise pitch, rhythm, key signature, time signature, notes, rests, voices, or musical semantics.
- Do not authorise OCR.
- Do not authorise vector/raster fusion.
- Do not authorise product recogniser implementation.
- Do not decide recogniser readiness (Task 63 only provides the evidence table).

Acceptance criteria:
- Governance PR opened from `governance/task-63-raster-diagnostics-corpus-review-v0.1` to `main`.
- `ACTIVE_TASK.md` is updated to Task 63.
- `projects/score2gp/runs/2026-06-10-raster-diagnostics-corpus-review.md` (or similar) is added containing the review table.
- The review table lists fixture/page/staff, expected opening-symbol status, observed summary label, false-positive/false-negative classification, and notes.
- Ground truth is explicitly documented as manual review.

Stop conditions:
- Governance PR #114 is not merged.
- Governance repo is dirty before work starts.
- The task requires product repo modifications.

Reporting format:
- Branch name
- PR link
- Exact files changed
- Commit hash
- Commands run
- Validation results
- Privacy/artifact check results
- Summary of review findings
- Known limitations
- Whether PR is ready for review
