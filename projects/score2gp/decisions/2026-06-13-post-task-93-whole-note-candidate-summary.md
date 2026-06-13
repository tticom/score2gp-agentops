# Decision Record: Post-Task 93 Whole-Note Candidate Summary

## Status
Completed: Product Task 93

## Context
Product Task 93 was authorised to add a machine-checkable `whole_note_candidate_summary` block to normal diagnostic report output.

## Record of Completion
- **Product PR**: [#253](https://github.com/tticom/score2gp/pull/253)
- **Head SHA**: `acbc48a9214da89e5643c808111180510fc59728`
- **Merge Commit**: `0cfd8b9d510c3e9ccf0f3a55e6f069e1becf91ba`

### Changes Made
Files changed in Product PR #253:
- `scripts/raster_diagnostics_gate_report.py`
- `tests/test_whole_note_integration.py`

Summary of additions:
- Added `whole_note_candidate_summary` block.
- Fields added to the summary: `total_count`, `pages_with_candidates`, `candidate_ids`, `candidate_count_by_page`.
- Existing fields remained backwards compatible (`whole_note_candidate`, `whole_note_candidate_pages`, `whole_note_candidate_locations`).
- Output remains strictly diagnostic-only.
- No ScoreIR, GP output, pitch inference, duration/rhythm inference, OCR, or full notation recognition was introduced.
- The whole-note / half-note boundary remains strictly active:
  - whole-note candidate = hollow oval without attached or closely adjacent vertical stem;
  - half note = hollow oval with attached or closely adjacent vertical stem;
  - stemmed hollow ovals must be excluded from whole-note candidate diagnostics.

## Codex Comment Disposition Rule
Future reviews must include a “Codex comment disposition” section. Every Codex comment or review thread must be inspected and explicitly dispositioned as one of:
- accepted as blocker;
- accepted as non-blocking;
- already fixed;
- rejected with reason.

If a Codex comment identifies a plausible correctness bug, require or verify a regression test unless there is a clear reason not to.

## Authorisation: Product Task 95
Product Task 95 is authorised as the next sequential product task.
**Goal**: Add a machine-checkable whole-note fixture outcome summary to the raster diagnostics gate report, using existing diagnostic data only.

The summary must include at least:
- total whole-note positive fixtures evaluated;
- total positive fixtures with candidates;
- total positive fixtures without candidates;
- total half-note fixtures evaluated;
- total half-note fixtures with false-positive whole-note candidates;
- total negative/noise fixtures evaluated;
- total negative/noise fixtures with false-positive whole-note candidates;
- case-level whole-note outcome entries containing: `case_id`, `category`, `whole_note_candidate`, `whole_note_candidate_summary.total_count`, and an outcome label (e.g., `whole_note_true_positive`, `whole_note_false_negative`, `whole_note_true_negative`, `whole_note_false_positive`).

Product Task 95 must use existing diagnostic report data only. It must not change extraction logic unless a defect is discovered and explicitly reported as a blocker.

### Required Tests for Task 95
Implementation of Product Task 95 must include explicit regression tests proving:
- positive whole-note fixture outcome summary counts;
- half-note fixture false-positive count;
- negative/noise fixture false-positive count;
- case-level outcome labels;
- consistency between case-level `whole_note_candidate_summary.total_count` and aggregate counts;
- proof that output remains strictly diagnostic-only;
- proof that no ScoreIR, GP output, pitch inference, duration/rhythm inference, OCR, or full notation recognition is introduced.
