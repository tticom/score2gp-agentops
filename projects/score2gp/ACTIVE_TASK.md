## Current Active Task

## Task 59 — Define raster diagnostics summary reporting/export boundary

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-59-raster-diagnostics-summary-reporting-boundary-v0.1`

PR title:
`docs(score2gp): define raster diagnostics summary reporting boundary`

Context:
Task 59 is a governance-only task.
Task 59 defines whether and how a CLI, smoke script, JSON report, or governance run record may expose the raster diagnostics summary without committing artifacts, leaking private fixtures, or implying semantic recognition.
Task 59 must be completed before any product implementation of reporting/export occurs.
Task 59 depends on the merge of Governance PR #111.

Goal:
Create a governance PR that defines the reporting/export contract for the read-only raster diagnostics summary helper. The note must explicitly state what reporting actions are authorised and what remain strictly prohibited.

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
- Do not promote `treble_clef_candidate` or the diagnostics summary into semantic recognition.

Acceptance criteria:
- Governance PR opened from `governance/task-59-raster-diagnostics-summary-reporting-boundary-v0.1` to `main`.
- `ACTIVE_TASK.md` is updated to Task 59.
- `projects/score2gp/reviews/2026-06-10-raster-diagnostics-summary-reporting-boundary.md` is added.
- The boundary note specifies what forms of reporting/export are permitted.
- The boundary note prohibits ScoreIR and semantic inferences.
- The boundary note sets up the next implementation task securely.

Stop conditions:
- Governance PR #111 is not merged.
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
- How PR #111 merge was verified
- Boundary summary
- Known limitations
- Whether PR is ready for review
