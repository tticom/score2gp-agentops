# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-01 — Key signature: read it from the notation and write it on every bar

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-01-key-signature`

**Pull Request**: 468

**Owner Role**: implementation

## Objective

Read the key signature from the notation staff and write it as GPIF `Key` (accidental count from the source; mode only where independently evidenced) on every master bar, including key changes. In the reference Lesson-3.gp every one of the 66 master bars has 1 sharp, G major. The DUR-02 output has no `Key`, so Guitar Pro shows C major and every F sharp carries an accidental.

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
- `tests/test_omit_01_*.py`
- `tests/fixtures/pdf/omit_01/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
