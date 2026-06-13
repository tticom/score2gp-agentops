# Decision: Post Task 95 Whole-Note Fixture Outcomes

**Date:** 2026-06-13
**Context:** Product Task 95 implementation completed and merged.

## Task 95 Record
Product PR #254 successfully added a machine-checkable `whole_note_fixture_outcome_summary` to the raster diagnostics gate report, using only existing diagnostic report data.

* **Product PR URL:** `https://github.com/tticom/score2gp/pull/254`
* **Head SHA:** `fdd195f35484dbdcfe8eb3c8b2d60c29fcdf160c`
* **Merge Commit SHA:** `a7a84a90ddf425d71fc9fc04cb0f05141ef94930`

**Files changed in Product PR #254:**
* `scripts/raster_diagnostics_gate_report.py`
* `tests/test_raster_diagnostics_gate_report.py`

**Task 95 Additions Summary:**
* Introduced `whole_note_fixture_outcome_summary` to JSON report output.
* Added aggregate counts for positive whole-note fixtures.
* Added aggregate counts for half-note fixtures.
* Added aggregate counts for negative/noise fixtures.
* Added case-level whole-note outcome labels.
* Default/no-`--test-manifest` gate coverage now includes positive whole-note fixture, half-note fixture, and negative/noise fixture coverage.

**Backward Compatibility and Constraints Verified:**
* Existing fields remain unchanged (`whole_note_candidate`, `whole_note_candidate_pages`, `whole_note_candidate_locations`, `whole_note_candidate_summary`).
* Output remains strictly diagnostic-only.
* No ScoreIR, GP output, pitch inference, duration/rhythm inference, OCR, or full notation recognition was authorised or introduced.
* No generated artifacts or private fixtures were committed.

## Authorisation for Product Task 97

Product Task 97 is authorised as the next smallest visible product improvement.

**Goal:**
Add a human-readable whole-note fixture outcome section to the normal text-mode raster diagnostics gate report.

**Requirements:**
* Use the same already-computed `whole_note_fixture_outcome_summary` data.
* Print aggregate counts for:
  * positive whole-note fixtures evaluated;
  * positive fixtures with candidates;
  * positive fixtures without candidates;
  * half-note fixtures evaluated;
  * half-note fixtures with false-positive whole-note candidates;
  * negative/noise fixtures evaluated;
  * negative/noise fixtures with false-positive whole-note candidates.
* Optionally print concise per-case outcome lines if the output remains readable.
* Keep JSON output backwards compatible.
* Keep existing machine-checkable JSON fields unchanged.
* Add regression tests for text-mode output.
* Remain strictly diagnostic-only.

**Explicit Non-Goals (Constraints):**
* Do not change extraction logic.
* Do not infer pitch.
* Do not infer duration or rhythm beyond existing diagnostic labels and fixture outcome labels.
* Do not emit ScoreIR.
* Do not emit GP output.
* Do not add OCR.
* Do not attempt full notation recognition.
* Do not add private fixtures or commit generated artifacts.

## Standing Rules for Future Reviews

**Codex Comment Disposition:**
Future reviews must include a “Codex comment disposition” section. Every Codex comment or review thread must be inspected and explicitly dispositioned as one of:
* accepted as blocker;
* accepted as non-blocking;
* already fixed;
* rejected with reason.

If a Codex comment identifies a plausible correctness bug, require or verify a regression test unless there is a clear reason not to.
