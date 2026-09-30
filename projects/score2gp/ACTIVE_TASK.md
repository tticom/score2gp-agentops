# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: DUR-03 — Detect the TAB staves whose lines are drawn in broken segments so their fret digits are read (Lesson 6: 52 of 72 bars empty)

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/dur-03-tab-staff-detection`

**Pull Request**: 474

**Owner Role**: implementation

## Objective

Recover TAB staves drawn with broken or partly missing lines, so their fret digits reach the assembler with the right string, system and bar, read from the source. Lesson 6 writes 52 of 72 bars empty (226 notes against 844 in the reference) because only 10 of 34 TAB staves are detected; Lessons 4 and 5 lose 2 and 8 bars the same way. Whatever cannot be read unambiguously stays refused with a located reason.

## Allowed paths

- `src/score2gp/pdf.py`
- `src/score2gp/pdf_*.py`
- `src/score2gp/tabraw.py`
- `tests/test_dur_02_oracle.py`
- `tests/test_pdf_*.py`
- `tests/test_dur_03_*.py`
- `tests/fixtures/pdf/dur_03/**`
- `docs/design/**`
- `tests/test_omit_03_private.py`
- `tests/test_pdf.py`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
