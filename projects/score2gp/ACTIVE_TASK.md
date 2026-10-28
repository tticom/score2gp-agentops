# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: FND-06 — Quarantine by exact ID, or fix, the known Windows host test failures

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/fnd-06-windows-host-test-failures`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Quarantine by exact ID, or fix, the known Windows host test failures. Source: authority item FND-06. Blocks zero-exit local suites; devils-advocate reviewers withhold verdicts (#465 re-review, 2026-09-25).

## Allowed paths

- `src/score2gp/**`
- `tests/**`
- `pyproject.toml`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
