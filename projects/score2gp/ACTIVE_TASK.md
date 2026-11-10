# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-19 — Reduce the largest remaining refused-bar class

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-19-largest-refused-class-after-mem-04`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

REFUSE-18, TABEXT-03, NOTAB-01, GROUP-03 and DUR-04 have landed since the last whole-set ranking. Re-rank every refused bar over the whole private set on the current runtime, then take the largest class that is a reader or representation gap and that the printed page settles. Leads, not facts: do not trust older counts.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
