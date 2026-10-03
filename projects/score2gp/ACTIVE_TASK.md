# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: TUPLET-TAB-01 — TAB fret numbers are not tuplet numbers

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/tuplet-tab-01-fret-numbers-not-tuplets`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

A digit text lying on or between TAB staff lines (or otherwise belonging to the TAB row) is never a tuplet-number candidate, so Melodic Soloing Masterclass bar 7 (no tuplet drawn) is no longer refused with tuplet_number_unassociated; a genuine printed tuplet number with its bracket or beam group must still be found. Never invent a value, never loosen a gate to raise a count.

## Allowed paths

- `src/score2gp/notation_omr/note_duration.py`
- `tests/test_note_duration*.py`
- `tests/test_tuplet_tab_01_*.py`
- `tests/fixtures/pdf/tuplet_tab_01/**`
- `docs/design/**`
- `tests/test_npg03b_floating.py`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
