# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: NPG-06A — One production GPIF serializer: remove the pytest-conditional writer branch

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/npg-06a-one-production-gpif-serializer`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

One production GPIF serializer: remove the pytest-conditional writer branch. Source: authority item NPG-06A. Detail: plans/2026-08-19-native-pdf-to-gp-and-audiveris-retirement.md §16 (NPG-06A). Also the architect's FND-01.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
