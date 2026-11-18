# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: CASCADE-01 — Refused bars that follow a refused bar: fix the root refusal in Black Dog (design), prove it on Crossroads (holdout)

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/cascade-01-tie-stop-cascade-black-dog-crossroads`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Measure which refused bars are refused only because an earlier bar was refused (tie_stop_without_written_predecessor), fix the root refusal in the Black Dog chain using page evidence, and apply the finished reader once to Crossroads as the pre-named positive holdout. A bar the evidence cannot settle stays refused. Leads, not facts: re-measure.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
