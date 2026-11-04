# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-12 — Read the next remaining reader-gap refusal class after REFUSE-11

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-12-next-remaining-refusal-class`

**Pull Request**: 546

**Owner Role**: implementation

## Objective

Same method as REFUSE-11, one class further: after REFUSE-11 lands, re-measure the whole-set ranking of remaining refusal codes and take the largest remaining class that is a reader gap with unambiguous musical symbols. If the largest remaining classes are all representation gaps or unknown, stop and report the located ranking instead of guessing. Leads, not facts.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
