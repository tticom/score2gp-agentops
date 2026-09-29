# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-02 — Double barlines: detect section-ending double barlines and write them

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-02-double-barlines`

**Pull Request**: 469

**Owner Role**: implementation

## Objective

Detect double barlines in the notation or TAB staves and write GPIF `DoubleBar` on the master bar they close. The reference Lesson-3.gp has 11, at bars 3, 7, 13, 18, 25, 28, 34, 40, 49, 53 and 59; the output has none.

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
- `tests/test_omit_02_*.py`
- `tests/fixtures/pdf/omit_02/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
