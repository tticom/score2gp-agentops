# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-10 — Stop duration-free marks (arcs, overlapping forms, marks below strings) refusing whole bars

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-10-duration-free-marks`

**Pull Request**: 544

**Owner Role**: implementation

## Objective

REFUSE-07 measured unsupported_overlapping_form (5 bars), unclassified_same_position_arc (4), unclassified_mark_below_strings (4) and remaining symbol_unclassified (6) among the refusals. Measure which of these are ties/slurs, bend or technique marks, or other unambiguous symbols that carry no duration and are wrongly refusing the whole bar, and record them as located non-events only where the shape settles it. Leads, not facts: re-measure on the current runtime.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
