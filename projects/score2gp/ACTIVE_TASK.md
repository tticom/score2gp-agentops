## Current Active Task

## Task 64 — Interpret raster diagnostics corpus review and define numeric threshold gates

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-64-decide-recogniser-readiness-v0.1`

PR title:
`docs(score2gp): decide recogniser readiness and semantic promotion boundary`

Context:
Task 64 is a governance-only decision task.
Task 63 completed the read-only evidence collection for raster diagnostics, showing 0 false positives and 11 false negatives across the private corpus, with 3 true negatives.
Task 64 must interpret this evidence and define numeric threshold gates. It must state that the current evidence is not sufficient to authorise semantic promotion, because 3 true negatives is too small to prove robust staff-line/TAB/noise exclusion.

Goal:
Create a governance PR that defines explicit numeric and qualitative threshold gates. The decision must maintain the block on semantic promotion until broader evidence is collected.

Non-goals:
- Do not modify the product repo.
- Do not implement product recogniser code.
- Do not authorise ScoreIR emission.
- Do not authorise recognised clef objects.
- Do not authorise pitch, rhythm, key signature, time signature, notes, rests, voices, or musical semantics.
- Do not authorise OCR.
- Do not authorise vector/raster fusion.
- Do not semantically promote `treble_clef_candidate`.

Acceptance criteria:
- Governance PR opened from `governance/task-64-decide-recogniser-readiness-v0.1` to `main`.
- `ACTIVE_TASK.md` is updated to Task 64.
- `projects/score2gp/reviews/2026-06-10-recogniser-readiness-decision.md` is added.
- The decision note explicitly blocks semantic promotion based on insufficient negative coverage.
- The note defines acceptable false positive and false negative thresholds.

Stop conditions:
- Governance PR #115 is not merged.
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
- Summary of decision
- Known limitations
- Whether PR is ready for review
