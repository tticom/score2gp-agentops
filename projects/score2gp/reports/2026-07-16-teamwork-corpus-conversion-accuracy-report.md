# Teamwork Recovery Baseline Report: Task 88 Execution

This report documents the baseline established from the recovery branch `recovery/pre-teamwork-score-output-baseline-v0.1` at `e70bddaa`, with the single implemented generic source-layout propagation trace.

## 1. Scope of the Recovery Task

As directed by the Project Director:
- **Baseline Branch**: `recovery/pre-teamwork-score-output-baseline-v0.1` (started from clean commit `e70bddaa` in a separate worktree `score2gp-recovery`).
- **Failed Commit Work**: Completely isolated and frozen; no code from the failed branch was cherry-picked, merged, or copied.
- **Constraints Applied**: Absolutely no accidental/key signature, duration, chord, or embellishment code changes were made in this task.
- **Single Layout Improvement**: Implemented and verified the generic source-layout propagation trace:
  `PDF staff-system identity` $\rightarrow$ `first measure of system` $\rightarrow$ `MusicXML print/rehearsal` $\rightarrow$ `ScoreIR Bar layout_break/marker` $\rightarrow$ `GPIF MasterBar Break/Section` XML serialization.

---

## 2. Before/After Separation: Failed Output vs Recovery Baseline

This table separates the failed Teamwork branch output from the restored recovery baseline output:

| File | Failed Teamwork Branch Status | Restored Recovery Baseline Status |
| :--- | :--- | :--- |
| **Lesson-3.gp** | - Introduced filename key-signature overrides<br>- Created root-level file pollution | **Matches: True** (100% exact semantic match) |
| **Lesson-4.gp** | - Severe accidental & technique regressions<br>- Lacked layout/title propagation | **Matches: False**<br>- **First Remaining Mismatch**: `tempo` (expected: 70, actual: 93)<br>- No accidental or embellishment regressions. |

*Note: The recovery baseline successfully restores the correct accidental and technique parsing behavior, preventing the regressions introduced in the failed branch.*

---

## 3. Generic Source-Layout Trace Implementation

The trace is implemented generically without hardcoding:
1. **OMR Sidecar Generation** ([deterministic_musicxml.py](file:///home/tticom/work/score2gp-workspace/score2gp-recovery/src/score2gp/deterministic_musicxml.py)): System first measures and page boundaries are detected using page and system indices from the timeline preview. Appropriate `<print new-page="yes">` or `<print new-system="yes">` tags are written into the MusicXML.
2. **MusicXML Parser** ([musicxml.py](file:///home/tticom/work/score2gp-workspace/score2gp-recovery/src/score2gp/musicxml.py)): The parser extracts the `<print>` element's attributes (`new-page` / `new-system`) and maps them to `measure.layout_break`.
3. **ScoreIR Builder** ([build_ir.py](file:///home/tticom/work/score2gp-workspace/score2gp-recovery/src/score2gp/build_ir.py)): Passes `measure.layout_break` directly into the `Bar` constructor.
4. **GPIF Serializer** ([gpif.py](file:///home/tticom/work/score2gp-workspace/score2gp-recovery/src/score2gp/gpif.py) & [gp_package.py](file:///home/tticom/work/score2gp-workspace/score2gp-recovery/src/score2gp/gp_package.py)): 
   - Relational and classic parsers extract `<Section><Name>` as `Bar.marker`.
   - Relational and classic writers serialize the marker to `<Section><Name>` in `<MasterBar>`.
   - Roundtrip validation verifies equivalence for `layout_break`, `barline`, and `marker`.

---

## 4. Verification and Integration Tests

A comprehensive integration test has been added to prove the layout and marker propagation trace:
- `test_layout_and_title_propagation` in [test_system_breaks.py](file:///home/tticom/work/score2gp-workspace/score2gp-recovery/tests/test_system_breaks.py):
  - **Positive Case**: Verifies that a measure starting a new staff system gets `<print new-system="yes">`, which parses into `Bar.layout_break = "line"`, and generates `<Break>Line</Break>` in the final GPIF. Also checks rehearsal mark propagation (`Exercise 1` $\rightarrow$ `<Section><Name>Exercise 1</Name>`).
  - **Negative Case**: Verifies that a measure continuing a system does not get print breaks or incorrect section markers.

All **932 unit and integration tests** in the recovery codebase pass cleanly.
Conversions were run locally without reference leakage. Output files are isolated under `work/recovery/run_2/` in the recovery worktree.
