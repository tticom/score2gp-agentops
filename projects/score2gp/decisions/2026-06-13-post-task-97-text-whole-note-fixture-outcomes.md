# Decision: Post Task 97 Text Whole-Note Fixture Outcomes

**Date:** 2026-06-13
**Context:** Product Task 97 implementation completed and merged.

## Task 97 Record
Product PR #255 successfully added a human-readable `Whole-note fixture outcome summary` in text mode to the raster diagnostics gate report, using only the existing data from `whole_note_fixture_outcome_summary`.

* **Product PR URL:** `https://github.com/tticom/score2gp/pull/255`
* **Head SHA:** `d3649f4944ae9e931a1e4f71bbb6f4504e9486e6`
* **Merge Commit SHA:** `3d87c794a2a3f54108679f7613ef79e1502ab2bf`

**Files changed in Product PR #255:**
* `scripts/raster_diagnostics_gate_report.py`
* `tests/test_raster_diagnostics_gate_report.py`

**Task 97 Additions Summary:**
* Added human-readable `Whole-note fixture outcome summary` block in text mode.
* Printed aggregate counts for positive whole-note fixtures.
* Printed aggregate counts for half-note fixtures.
* Printed aggregate counts for negative/noise fixtures.
* Ensured JSON output remains backwards compatible.

**Backward Compatibility and Constraints Verified:**
* Existing fields remain unchanged (`whole_note_candidate`, `whole_note_candidate_pages`, `whole_note_candidate_locations`, `whole_note_candidate_summary`, `whole_note_fixture_outcome_summary`).
* Output remains strictly diagnostic-only.
* No ScoreIR, GP output, pitch inference, duration/rhythm inference, OCR, or full notation recognition was authorised or introduced.
* No generated artifacts or private fixtures were committed.

## Authorisation for Product Task 99

Product Task 99 is authorised as the next smallest visible product improvement.

**Goal:**
Add a machine-checkable `whole_note_detection_status` / readiness status to the raster diagnostics gate report, derived from the existing whole-note fixture outcome summary.

**Requirements:**
* Derive status from the existing `whole_note_fixture_outcome_summary`.
* Add a stable machine-checkable JSON field: `whole_note_detection_status`.
* Use a small fixed status vocabulary: `pass`, `review`, `fail`.
* Include a short machine-checkable reason list or reason code list if useful: `whole_note_detection_status_reasons`.
* Optionally print the same status in text mode if it improves human readability.
* Keep existing JSON fields backwards compatible.
* Add regression tests for pass/review/fail or, at minimum, current pass plus one mocked review/fail scenario.
* Remain strictly diagnostic-only.

**Explicit Non-Goals (Constraints):**
* Do not change extraction logic.
* Do not infer pitch.
* Do not infer duration or rhythm beyond existing diagnostic labels and fixture outcome/status labels.
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
