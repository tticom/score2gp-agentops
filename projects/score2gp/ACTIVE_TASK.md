# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: TECH-02 — Bends the reference files have: add bends to the independent oracle, design on Melodic Soloing Masterclass, holdout on Ex 2 Hands Up

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/tech-02-bends-against-references`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Add bends to the independent oracle, measure bend differences against the .gp references, make the product write the design source's bends (Melodic Soloing Masterclass) from printed-page evidence, and apply it once to the pre-named holdout (Ex 2 Hands Up). Oracle extension and measurement stand on their own. Other reference differences are findings only. Leads, not facts: re-measure.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
