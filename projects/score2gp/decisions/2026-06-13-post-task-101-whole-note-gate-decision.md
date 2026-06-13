# Decision: Post Task 101 Whole-Note Gate Decision

**Date:** 2026-06-13
**Context:** Product Task 101 implementation completed and merged.

## Task 101 Record
Product PR #257 successfully made the existing `whole_note_detection_status` actionable in the raster diagnostics gate/check mode, introducing a machine-checkable `whole_note_detection_gate_status` and appropriately reflecting non-pass conditions into the aggregate `gate_status`.

* **Product PR URL:** `https://github.com/tticom/score2gp/pull/257`
* **Head SHA:** `395149baec60427900c9360ede6f4f16968be2e9`
* **Merge Commit SHA:** `fb6f026f896247b4572e9cbd285d5719891c6673`

**Files changed in Product PR #257:**
* `scripts/raster_diagnostics_gate_report.py`
* `tests/test_raster_diagnostics_gate_report.py`

**Task 101 Additions Summary:**
* Made `review` and `fail` statuses visible in the machine-checkable gate/check output by surfacing them in the aggregate gate decision.
* Introduced `whole_note_detection_gate_status` to track whole note explicit gate contributions.
* Added specific review and fail testing for the whole-note component, assuring the exit status operates correctly in check mode.

**Backward Compatibility and Constraints Verified:**
* Existing fields and definitions remain unchanged.
* Output remains strictly diagnostic-only.
* No ScoreIR, GP output, pitch inference, duration/rhythm inference, OCR, or full notation recognition was authorised or introduced.
* No generated artifacts or private fixtures were committed.

## Authorisation for Product Task 103

Product Task 103 is authorised as the next useful product improvement, to compare actual whole-note candidate counts against explicit expected counts for safe public fixtures.

**Goal:**
Add expected whole-note candidate count checks to the raster diagnostics gate report.

**Requirements:**
* Use existing `whole_note_candidate_summary.total_count`.
* Add explicit expected whole-note candidate counts for safe public fixtures in the gate report manifest/data path.
* For the current public fixtures, expected counts should be diagnostic-only, for example:
  * blank/negative fixtures: expected count `0`;
  * half-note fixture: expected count `0`;
  * whole-note fixture: expected count `1`, if live fixture evidence confirms that is the intended current fixture.
* Add machine-checkable JSON output for expected count comparison, such as:
  * `expected_whole_note_candidate_count`;
  * `whole_note_candidate_count_matches_expected`;
  * per-case actual/expected count fields;
  * aggregate count gate/status/reasons.
* Make count mismatch affect aggregate gate/check status.
* Preserve existing JSON fields.
* Add tests for:
  * pass when actual count matches expected count;
  * review/fail when a positive whole-note fixture has too few candidates;
  * review/fail when a positive whole-note fixture has too many candidates;
  * review/fail when a half-note or negative fixture has candidates despite expected count `0`;
  * check-mode non-zero behaviour for count mismatch, if consistent with existing gate semantics.
* Keep output diagnostic-only.
* Do not change extraction logic.

**Explicit Non-Goals (Constraints):**
* Do not change whole-note candidate extraction.
* Do not change hollow oval detection.
* Do not change stem exclusion logic.
* Do not add pitch inference.
* Do not add rhythm or duration inference beyond diagnostic labels, fixture outcome labels, readiness/status labels, and gate/check labels.
* Do not add ScoreIR.
* Do not add GP output.
* Do not add OCR.
* Do not add full notation recognition.
* Do not add or commit generated reports, screenshots, PDFs, GP files, logs, local scratch files, raw JSON dumps, private diagnostics, or PR body files.

## Standing Rules for Future Reviews

**Codex Comment Disposition:**
Future reviews must include a “Codex comment disposition” section. Every Codex comment or review thread must be inspected and explicitly dispositioned as one of:
* accepted as blocker;
* accepted as non-blocking;
* already fixed;
* rejected with reason.

If a Codex comment identifies a plausible correctness bug, require or verify a regression test unless there is a clear reason not to.
