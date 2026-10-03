# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: PDF-GROUP-02 — Bridge TAB string-line gaps at full-chord digit columns

**Status**: COMPLETED

**Repository**: tticom/score2gp

**PR Branch**: `feat/pdf-group-02-bridge-string-line-gaps`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

A TAB staff whose six strings are all broken at the same x by fret digits is detected as ONE staff, so its barlines and the joint left stroke are owned by the system, using a scale-relative rule (about 0.8 of the string spacing, aligned across strings or flanked by a digit). Targets A7-Blues-Lick (4 bars, 46 of 46 digits placed) and the grouping of E_Chord_Lick_Chord. Never invent a value, never loosen a gate to raise a count; anything ambiguous stays refused with a located reason.

## Allowed paths

- `src/score2gp/pdf_geometry.py`
- `tests/test_pdf*.py`
- `tests/test_pdf_group_02_*.py`
- `tests/fixtures/pdf/pdf_group_02/**`
- `docs/design/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
