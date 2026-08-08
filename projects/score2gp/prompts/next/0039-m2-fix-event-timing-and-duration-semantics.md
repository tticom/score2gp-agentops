# 0039 - M2: Fix Event Timing and Duration Semantics

## Objective

Correct the smallest generic causes of event timing and duration mismatches in the `score2gp` pipeline. Use the bar-level comparator (M1) to observe, trace, and verify exact bar-level timing correctness on Lesson-3 and Lesson-4, and prove that the corrections generalize safely.

## Authorized Product Files

### Source Files
- `src/score2gp/notation_omr/duration.py`
- `src/score2gp/notation_omr/timeline.py`
- `src/score2gp/notation_bridge.py`
- `src/score2gp/pdf_tab_duration_associator.py`
- `src/score2gp/build_ir.py`
- `src/score2gp/pdf_only_chord_event_grouper.py`
- `src/score2gp/pdf_tab_bar_assembler.py`
- `src/score2gp/pdf_tab_event_factory.py`
- `src/score2gp/pdf_tab_measure_timing.py`
- `src/score2gp/pdf_tab_duration_types.py`

### Test Files
- `tests/test_notation_bridge.py`
- `tests/test_pdf_tab_duration_associator.py`
- `tests/test_build_ir.py`
- `tests/test_timeline_refinements.py`
- `tests/test_pdf_only_chord_event_grouper_event_grouping.py`
- `tests/test_pdf_tab_bar_assembler.py`
- `tests/test_pdf_tab_event_factory.py`
- `tests/test_pdf_tab_measure_timing.py`
- `projects/score2gp/ACTIVE_TASK.md`

No other product files in `src/` or `tests/` may be edited in this task.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/programmes/2026-07-16-teamwork-corpus-conversion-accuracy.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/m2-fix-event-timing-and-duration-semantics` in `tticom/score2gp`.
6. Run `python scripts/agent_verify.py` in `score2gp` before making code modifications.

## Implementation Scope & Seam Contract

Using M1's `compare-bars` tool to report precise discrepancies, trace and correct timing/duration semantics. Specifically:

1. **Resolve Ghost Rests**: Eliminate unevidenced or redundant padding/ghost rests in timeline assembly.
2. **Correct Duration Semantic Classifications**: Fix incorrect classifications for whole, half, quarter, eighth, sixteenth, and thirty-second note/rest durations based on source geometry and flags.
3. **Dots on Notes and Rests**: Improve detection and application of dots, ensuring correct beat-value scaling.
4. **Order Notes and Rests correctly**: Prevent incorrect interleaving of note and rest events within measures.
5. **Ties and Carried Duration**: Ensure ties correctly bind durations across events without inflating note values or creating ghost notes.
6. **Chords vs. Sequential Events**: Standardize grouping to distinguish chords (simultaneous notes) from sequential events correctly.

All changes must be generic, geometry/rule-based, and checked against both target Lesson files and a distinct corpus file.

## Validation Commands

1. `.venv/bin/python -m pytest`
2. Run conversion on `Lesson-3.pdf` and `Lesson-4.pdf` using a fresh `--work-dir` under `work/teamwork/<run-id>/` (never unignored `tmp/` or repository root).
3. Use `compare-bars` to evaluate the actual output against the expected/reference baseline, verifying exact improvements in Lesson-3 (bars 47, 63, 66) and Lesson-4 (bars 20, 39, 43).
4. Run conversion and comparator verification against a distinct non-Lesson corpus file (e.g. `Derek Trucks BB King.pdf` or `Melodic Soloing Masterclass.pdf`) to prove timing/duration changes generalize safely without regressions.

## Non-goals

- Do not implement any key signature, meter, layout, double/final barlines, page breaks, or legato/pull-off/slides/vibrato (embellishment) changes.
