# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-04 — Arpeggio marks: detect rolled-chord marks and write them

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-04-arpeggio-marks`

**Pull Request**: 475

**Owner Role**: implementation

## Objective

Detect the vertical wavy arpeggio (rolled-chord) mark beside a chord and write GPIF `Arpeggio` on that beat. The reference Lesson-3.gp has 2; the output has none.

## Allowed paths

- `src/score2gp/pdf.py`
- `src/score2gp/pdf_*.py`
- `src/score2gp/notation_omr/**`
- `src/score2gp/recognition/**`
- `src/score2gp/ir.py`
- `src/score2gp/tabraw.py`
- `src/score2gp/build_ir.py`
- `src/score2gp/gpif.py`
- `src/score2gp/gp_package.py`
- `src/score2gp/version_adapter.py`
- `src/score2gp/cli.py`
- `schemas/**`
- `tests/test_dur_02_oracle.py`
- `docs/design/**`
- `docs/architecture.md`
- `tests/test_omit_04_*.py`
- `tests/fixtures/pdf/omit_04/**`
- `tests/test_gp_writer.py`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
