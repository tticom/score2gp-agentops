# Active Task

**Task**: M2: Fix Event Timing and Duration Semantics
**Status**: PR_OPEN
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/m2-fix-event-timing-and-duration-semantics`
**Pull Request**: `https://github.com/tticom/score2gp/pull/415`
**Original Prompt**: `projects/score2gp/prompts/next/0039-m2-fix-event-timing-and-duration-semantics.md`

## Context

Task `M1: Bar-Level Comparator and Mismatch Ledger` completed and merged via product PR #414. The project now promotes task `0039` to correct the timing and duration failures under the `Teamwork Programme: Corpus Conversion Accuracy`.

## Goal

Correct the smallest generic causes of timing, duration, dot, rest, tie, and chord/sequential event grouping mismatches across Lesson-3, Lesson-4, and the general corpus.

## Allowed Files

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
- `tests/test_notation_bridge.py`
- `tests/test_pdf_tab_duration_associator.py`
- `tests/test_build_ir.py`
- `tests/test_timeline_refinements.py`
- `tests/test_pdf_only_chord_event_grouper_event_grouping.py`
- `tests/test_pdf_tab_bar_assembler.py`
- `tests/test_pdf_tab_event_factory.py`
- `tests/test_pdf_tab_measure_timing.py`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- Do not implement any key signature, meter, layout, double/final barlines, page breaks, or legato/pull-off/slides/vibrato (embellishment) changes.

## Acceptance

Successfully implement timing and duration fixes, verify all tests pass locally and on CI, update `ACTIVE_TASK.md`, and publish one product pull request on branch `agy/m2-fix-event-timing-and-duration-semantics` in `tticom/score2gp` for independent Codex review.
