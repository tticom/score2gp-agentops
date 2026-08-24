# Run Record: Dynamic System-to-Measure Window Alignment Implementation

- **Date:** 2026-05-31
- **Branch:** `research/domain-knowledge-stage-tests-v1`
- **Remediation Status:** Complete
- **Target Deliverables:**
  - `tests/test_system_skipped_measure_alignment.py` (Synthetic skipped-measure alignment regression test)
  - `src/score2gp/build_ir.py` (Refactored sequence-alignment algorithm)

## Execution Logs

### 1. Verification of Clean Baseline
- Python tests: `405 passed` successfully.
- Private git invariant: pristine (`fixtures/private/.gitkeep` only).

### 2. Implementation Steps
- [x] Create synthetic regression test `tests/test_system_skipped_measure_alignment.py`
  - Validates omitted measure 22 alignment gap.
  - Asserts that omitted measures are logged as `pdf_system_alignment_gap` warnings.
- [x] Implement system-to-measure-window DP algorithm in `src/score2gp/build_ir.py`
  - Replaces greedy contiguous continuity logic.
  - Implements multi-factor match scoring (MIDI pitch sounding, pitch class, event counts, unmatched note penalties).
  - Uses tunable default gap penalty parameter (`gap_penalty = 3.0`).
  - Correctly backtracks to assign visual system measure offsets.
  - Gracefully falls back to contiguous greedy logic if no valid alignment sequence is found.
- [x] Run python tests: all 406 passed perfectly.
- [x] Run private end-to-end smoke pipeline.

### 3. Conversion Quality Improvements (Lesson 3)
The dynamic sequence alignment DP algorithm resulted in a massive quality increase for the Lesson 3 conversion:
- **Matched Playable Candidates:** `451` (up from `423`)
- **Unmatched Playable Candidates:** `3` (down from `31`)
- **Unmatched MusicXML Notes:** `22` (down from `50`)
- **Per Bar Quality Counts:**
  - `good`: **55** (up from `46`)
  - `poor`: **3** (down from `15`)
- **Skipped measures warnings:** Intentionally logged `pdf_system_alignment_gap` warnings for Measure 22 and Measure 25, preventing misalignment propagation downstream.

## Private-Safety Audit
- `git ls-files fixtures/private work` outputs exactly `fixtures/private/.gitkeep` (100% clean).
