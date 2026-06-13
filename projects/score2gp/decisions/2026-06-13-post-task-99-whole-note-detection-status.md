# Decision: Post Task 99 Whole-Note Detection Status

**Date:** 2026-06-13
**Context:** Product Task 99 implementation completed and merged.

## Task 99 Record
Product PR #256 successfully added a machine-checkable `whole_note_detection_status` / readiness status to the raster diagnostics gate report, derived from the existing whole-note fixture outcome summary.

* **Product PR URL:** `https://github.com/tticom/score2gp/pull/256`
* **Head SHA:** `b0f35d280e7bbc2ec569c926f4f92694dce94218`
* **Merge Commit SHA:** `b52054c95c5877f7253f9dbbbd1f7ec9989ee02a`

**Files changed in Product PR #256:**
* `scripts/raster_diagnostics_gate_report.py`
* `tests/test_raster_diagnostics_gate_report.py`

**Task 99 Additions Summary:**
* Added a stable machine-checkable JSON field `whole_note_detection_status` (`pass`, `review`, or `fail`).
* Added `whole_note_detection_status_reasons`.
* Ensured JSON output remains backwards compatible.

**Backward Compatibility and Constraints Verified:**
* Existing fields remain unchanged (`whole_note_candidate`, `whole_note_candidate_pages`, `whole_note_candidate_locations`, `whole_note_candidate_summary`, `whole_note_fixture_outcome_summary`).
* Output remains strictly diagnostic-only.
* No ScoreIR, GP output, pitch inference, duration/rhythm inference, OCR, or full notation recognition was authorised or introduced.
* No generated artifacts or private fixtures were committed.

## Authorisation for Product Task 101

Product Task 101 is authorised as the next smallest visible product improvement.

**Goal:**
Make existing `whole_note_detection_status` actionable in the raster diagnostics gate decision/check mode.

**Requirements:**
* Derive the new gate/check contribution from existing `whole_note_detection_status`.
* Preserve current passing behaviour when `whole_note_detection_status == "pass"`.
* Make `review` and `fail` statuses visible in machine-checkable gate/check output.
* Ensure check mode exits non-zero when whole-note detection is not `pass`, if that matches the existing check-mode semantics for non-passing gate status.
* Keep existing JSON fields backwards compatible.
* Add tests for:
  * current `pass` behaviour;
  * mocked or fixture-controlled `review` status;
  * mocked or fixture-controlled `fail` status;
  * check-mode exit behaviour for non-pass whole-note detection status, if check mode already exits non-zero for gate failures.
* Do not change extraction logic.

**Explicit Non-Goals (Constraints):**
* Do not change whole-note candidate extraction.
* Do not change hollow oval detection.
* Do not change stem exclusion logic.
* Do not add pitch inference.
* Do not add rhythm or duration inference beyond diagnostic gate/status labels.
* Do not add ScoreIR.
* Do not add GP output.
* Do not add OCR.
* Do not add full notation recognition.
* Do not update governance files.
* Do not add or commit generated reports, screenshots, PDFs, GP files, logs, local scratch files, raw JSON dumps, private diagnostics, or PR body files.

## Standing Rules for Future Reviews

**Codex Comment Disposition:**
Future reviews must include a “Codex comment disposition” section. Every Codex comment or review thread must be inspected and explicitly dispositioned as one of:
* accepted as blocker;
* accepted as non-blocking;
* already fixed;
* rejected with reason.

If a Codex comment identifies a plausible correctness bug, require or verify a regression test unless there is a clear reason not to.
