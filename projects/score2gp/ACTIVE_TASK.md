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
- Do not modify classifier semantics or thresholds unless the task explicitly narrows that change and tests prove it remains diagnostic-only.

Constraints & Privacy Boundaries:
- Use only authorised tracked fixtures or newly generated minimal public fixtures.
- Do not commit private PDFs, commercial PDFs, screenshots, rendered images, GP files, raw diagnostic JSON dumps, logs, scratch files, or local generated artifacts.
- If new fixture files are required, they must be minimal, intentionally created for tests, legally safe to commit, and documented.
- False-negative taxonomy must be anonymised and must not expose private fixture names, page images, screenshots, or copyrighted/private content.

Acceptance criteria:
- New negative fixtures (TAB, blank staves, text/noise) added to the `score2gp` test corpus, strictly adhering to the privacy boundaries.
- Anonymised documentation or taxonomy created for false negatives.
- A repeatable command or script to validate the diagnostic coverage against these fixtures.
- The `treble_clef_candidate` implementation remains diagnostic-only (returning coordinates/boxes without musical semantics).
- PR opened from `product/task-65-expand-diagnostic-corpus` to `main` in the `score2gp` repo.

Stop conditions:
- Product repo is dirty before work starts.
- The task attempts to emit ScoreIR or semantically recognised objects.
- The task attempts to commit unauthorised private material or artifacts.

Required validation:
- `git status --short`
- `git diff --check`
- Targeted pytest command for the new diagnostic fixture coverage
- Broader relevant diagnostics pytest subset if practical
- `git ls-files` privacy/artifact pattern check
- `find` large files check

Reporting format:
- exact files changed
- commands run
- targeted and broader test results
- privacy/artifact check results
- whether any fixtures were added, and why they are safe to commit
- known limitations
