# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: PARTIAL-01 — Write the boxed systems and refuse only the unboxed one instead of refusing the whole file (pdf_partial_grouping_one_system_unboxed)

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/partial-01-per-system-refusal`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

When exactly the readable systems can be written unambiguously, write them and refuse the unboxed system with a located reason instead of refusing the whole file (9 of 17 private PDFs in the 2026-10-02 investigation are refused for one unboxed system). Never invent a value, never loosen a gate to raise a count; anything ambiguous stays refused.

## Allowed paths

- `src/score2gp/build_ir.py`
- `src/score2gp/pdf.py`
- `src/score2gp/pdf_*.py`
- `src/score2gp/cli.py`
- `src/score2gp/report.py`
- `src/score2gp/notation_omr/**`
- `docs/design/**`
- `tests/test_dur_02_oracle.py`
- `tests/test_note_duration*.py`
- `tests/test_pdf*.py`
- `tests/test_partial_01_*.py`
- `tests/fixtures/pdf/partial_01/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
