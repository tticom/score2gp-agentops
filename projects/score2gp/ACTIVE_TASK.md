# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: CP-06 — Stop tests writing into the private corpus

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/cp-06-tests-must-not-write-private-corpus`

**Pull Request**: 509

**Owner Role**: implementation

## Objective

Stop tests writing into the private corpus. Source: authority item CP-06. Observed repeatedly 2026-09-25; the stray files reappear in score2gp-private-fixtures after test runs.

## Allowed paths

- `tests/**`
- `src/score2gp/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
