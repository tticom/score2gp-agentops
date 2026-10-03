# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: PDF-GROUP-01 — Group TAB systems whose last bar ends in a thin+thick double barline and whose first bar has no accepted left barline, using scale-relative rules

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/pdf-group-01-final-barline-first-bar-boundary`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Group safely the TAB systems whose last bar ends in a thin+thick double barline (C1) and whose first bar has no accepted left barline although fret digits lie left of the first barline (C2), using staff-space-relative limits only. Never invent a value, never loosen a gate to raise a count; anything ambiguous stays refused with a located reason. Expected gain is an estimate of 3 to 4 files (03 05 15 28), not 9.

## Allowed paths

- `src/score2gp/pdf.py`
- `src/score2gp/pdf_tab_system_partition.py`
- `tests/test_pdf*.py`
- `tests/test_pdf_group_01_*.py`
- `tests/fixtures/pdf/pdf_group_01/**`
- `docs/design/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
