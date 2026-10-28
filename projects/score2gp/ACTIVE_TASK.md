# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: FND-03A — FND-03 slice A: extend the independent stdlib GP reader oracle to repeats and endings, sections and chord diagrams

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/fnd-03a-independent-oracle-repeats-sections-chords`

**Pull Request**: 527

**Owner Role**: implementation

## Objective

FND-03 slice A: extend the independent stdlib GP reader oracle to repeats and endings, sections and chord diagrams. Source: authority item FND-03A. Ex 2 Hands Up GP6 vs GP7 encode repeat counts differently (2 vs 4): raw attributes are not version-neutral.

## Allowed paths

- `tests/**`
- `scripts/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
