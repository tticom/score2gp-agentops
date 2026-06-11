## Current Active Task

## Task 65 — Expand diagnostic evidence corpus with negative fixtures and failure taxonomy

Status: ACTIVE

Owning repo: score2gp

Branch:
`product/task-65-expand-diagnostic-corpus`

PR title:
`test(diagnostics): add negative fixtures and failure taxonomy for treble clef candidates`

Context:
Task 64 established that the current raster diagnostics corpus has insufficient negative coverage (only 3 true negatives). Semantic promotion is blocked.
Before any semantic recognition can be considered, we must provide robust proof of staff-line, TAB, and noise exclusion. We also need a structured failure taxonomy for the existing false negatives (11 found in Task 63). 

Goal:
Expand the product repository's diagnostic fixtures to include explicit negative cases (TAB staves, blank staves, noise). Create a failure taxonomy documenting why false negatives occur. Establish a repeatable validation command or fixture manifest. This task remains purely diagnostic.

Non-goals:
- Do not implement ScoreIR emission.
- Do not authorise recognised clef objects.
- Do not authorise pitch, rhythm, key signature, time signature, notes, rests, voices, or musical semantics.
- Do not authorise OCR.
- Do not authorise vector/raster fusion.
- Do not semantically promote `treble_clef_candidate`.
- Do not modify governance decisions; implement the required evidence base.

Acceptance criteria:
- New negative fixtures (TAB, blank staves, text/noise) added to the `score2gp` test corpus.
- Documentation or taxonomy created for false negatives.
- A repeatable command or script to validate the diagnostic coverage against these fixtures.
- The `treble_clef_candidate` implementation remains diagnostic-only (returning coordinates/boxes without musical semantics).
- PR opened from `product/task-65-expand-diagnostic-corpus` to `main` in the `score2gp` repo.

Stop conditions:
- Product repo is dirty before work starts.
- The task attempts to emit ScoreIR or semantically recognised objects.

Reporting format:
- Branch name
- PR link
- Exact files changed
- Commit hash
- Commands run
- Validation results (pass/fail for new fixtures)
- Summary of taxonomy added
- Known limitations
- Whether PR is ready for review
