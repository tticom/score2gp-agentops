## Current Active Task

## Task 56 — Define diagnostic consumer boundary for raster treble-clef candidates

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-56-raster-treble-clef-diagnostic-consumer-boundary-v0.1`

PR title:
`docs(score2gp): define raster treble-clef diagnostic consumer boundary`

Context:
Task 56 is governance-only.
Task 56 defines the consumer boundary for `raster_opening_symbol_classification`.
Task 56 does not authorise product implementation.
Task 56 depends on merged governance PR #109 and merged product PR #236.
No downstream product task may consume the diagnostic classifier until this consumer boundary is merged.
The next likely task may be a read-only diagnostics summary, but only if this note defines the consumer contract clearly.

Goal:
Create a governance PR that defines how downstream diagnostic or research tasks may consume `raster_opening_symbol_classification` without crossing into ScoreIR creation, recognised clef objects, or full semantic music recognition.

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
- Do not promote `treble_clef_candidate` to semantic recognition.

Acceptance criteria:
- Governance PR opened from `governance/task-56-raster-treble-clef-diagnostic-consumer-boundary-v0.1` to `main`.
- `ACTIVE_TASK.md` is updated to Task 56.
- `projects/score2gp/reviews/2026-06-10-raster-treble-clef-diagnostic-consumer-boundary.md` is added.
- The note verifies PR #236 and PR #109 are merged.
- The note defines the diagnostic consumer boundary.
- The note preserves diagnostic-only meaning.
- The note blocks ScoreIR and semantic recognition.
- The note defines allowed and disallowed uses.
- The note preserves `unknown` as a required consumer-visible result.
- The note defines acceptance criteria for any later read-only diagnostics summary implementation.

Stop conditions:
- Product PR #236 is not merged.
- Governance PR #109 is not merged.
- Governance repo is dirty before work starts.
- The task requires product repo modifications.
- The task would authorise ScoreIR, recognised clefs, pitch, rhythm, key/time inference, OCR, or vector/raster fusion.
- The task requires new fixtures or private artifacts.

Reporting format:
- Branch name
- PR link
- Exact files changed
- Commit hash
- Commands run
- Validation results
- Privacy/artifact check results
- How PR #236 merge was verified
- How PR #109 merge was verified
- Boundary summary
- Known limitations
- Whether PR is ready for review
- Recommended next smallest task after this PR is merged
