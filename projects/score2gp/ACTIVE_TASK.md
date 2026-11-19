# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: TECH-01 — Slides the reference files have and the product does not write: design on Melodic Soloing Masterclass, holdout on Can't Find My Way Home, Bebop and Ex 2 Hands Up

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/tech-01-slide-misses-against-references`

**Pull Request**: 578

**Owner Role**: implementation

## Objective

Find why slides the .gp references contain are not written for Melodic Soloing Masterclass (design source), make the existing slide reader write them from printed-page evidence, and apply it once to the pre-named holdouts (Can't Find My Way Home, Bebop Licks in Am, Ex 2 Hands Up), verified against the references with the independent oracle. Other reference differences are findings only. Leads, not facts: re-measure.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
