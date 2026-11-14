# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-23 — Reduce the next-largest remaining refused-bar class

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-23-next-refused-class-after-refuse-22`

**Pull Request**: 572

**Owner Role**: implementation

## Objective

After REFUSE-22, re-rank every refused bar over the whole private set on the current runtime and take the largest remaining reader or representation class that the printed page settles and that earlier REFUSE tasks did not address. Leads, not facts: re-measure.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
