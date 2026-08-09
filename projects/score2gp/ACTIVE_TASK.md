# Active Task

**Task**: Task 88 — In-Situ Real-Fixture Testing Integration & Fallback Cleanup
**Status**: ACTIVE
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `feature/agy/m6-in-situ-testing`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0043-m6-in-situ-real-fixture-testing.md`

## Context

The master failure diagnosis report has been finalized. We now promote Task 88 (Milestone 6, Task 1) to establish the in-situ test suite running against real fixtures, delete the `synthesize_missing_tab` fallback from `build_ir.py`, and reset `outer_tolerance` back to `24.0` points.

## Goal

Remove fallback synthesis logic, restore snapping tolerance to 24.0, and add the real-fixture in-situ test suite that skips gracefully in public CI.

## Allowed Files

- `src/score2gp/build_ir.py`
- `src/score2gp/pdf.py`
- `tests/test_real_fixtures_alignment.py`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- Do not implement page offsets, digit merging bounds, or barline changes.

## Acceptance

- `synthesize_missing_tab` is completely deleted.
- `outer_tolerance` is 24.0.
- Integration tests assert exactly 38 measures for Lesson-5 and 72 for Lesson-6, checking that no unassigned playable candidates remain.
- Tests skip gracefully in public CI when private fixtures are missing.
- Isolated unit tests are written if they add value.
