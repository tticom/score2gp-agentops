# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: NPG-06A-FU1 — NPG-06A validation: show the production GPIF layout does not depend on pytest

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/npg-06a-fu1-validate-pytest-independent-gpif-layout`

**Pull Request**: 526

**Owner Role**: implementation

## Objective

Validate, without changing production code, that the earlier removal of the pytest-conditional GPIF layout holds. Rescoped to validation only on the maintainer's word (2026-10-28: 'approved: rescope NPG-06A to validation only'); the explicit legacy layout option and its test migration are NPG-06A-FU2.

## Allowed paths

- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
