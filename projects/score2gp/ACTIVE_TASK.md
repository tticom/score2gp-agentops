# Developer Implementation: Quarter-Rest GP Export Verification v0.1

## Repository
tticom/score2gp

## Goal
Implement missing GP export integration tests for quarter-rest ScoreIR events, proving that the existing `gpif.py` export path handles rests safely without breaking existing multi-note timing, and fix any minor schema mismatches if discovered.

## Progress Baseline
* Product PR #319 merged, providing deterministic sequencing of quarter rest candidates as ScoreIR rest events.
* Architect research (Outcome A) confirmed the existing `gpif.py` structurally supports rests via `event.is_rest` and safely segregates note logic.
* Relevant files: `src/score2gp/gp_package.py`, `src/score2gp/gpif.py`, `tests/test_gp_writer.py`.

## Active Blocker
There are no regression or integration tests verifying that ScoreIR rest events export to valid GP7 XML. GP7 import validity for these exported files has not been functionally verified.

## Explicit Scope & Acceptance
* Write `test_gpif_rests` or equivalent in `tests/test_gp_writer.py` using a synthetic ScoreIR object or the `QuarterRestThenNotes.pdf` public fixture.
* Assert that the `.gp` zip payload encodes the rest `<Beat>` accurately without `<Notes>` tags and with correct rhythm.
* Identify and fix any minor GP XML schema mismatch (e.g. if an explicit `<Rest>` tag is actually mandated inside the Beat) solely within `gpif.py`.
* Ensure existing note export regression tests in `test_gp_writer.py` continue to pass.

## Constraints and Preservation
* Do not rewrite measure timing logic; rely on the existing `onset_ticks` and `duration_ticks` workflow.
* Do not broaden the task to tab-only export or full notation coverage.
* Do not add support for other rest types (whole, half, eighth).
* Do not include private PDFs, GP files, screenshots, generated dumps, logs, or local artifacts in the PR.
