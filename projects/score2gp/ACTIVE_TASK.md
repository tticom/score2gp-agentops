# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: FND-02 — Replace silent ScoreIR clamps with rejecting validators

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/fnd-02-reject-instead-of-clamp`

**Pull Request**: 524

**Owner Role**: implementation

## Objective

Replace silent ScoreIR clamps with rejecting validators. Source: authority item FND-02. Contradicts the L3 'no note clamping' gate; target limits belong in capability checks (ADR-008).

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
