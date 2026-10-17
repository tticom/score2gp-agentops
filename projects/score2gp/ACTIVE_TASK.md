# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: LETRING-01 — Read let ring from the page and write it (Lesson 5 bar 30)

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/letring-01-let-ring`

**Pull Request**: 497

**Owner Role**: implementation

## Objective

Lesson 5 bar 30 carries a let ring in the reference that the PDF-only route does not write. Read the mark from the page (text or symbol evidence) and write it on the notes it covers; where it cannot be read unambiguously, record a located reason.

## Allowed paths

- `src/score2gp/**`
- `tests/**`
- `docs/**`
- `schemas/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
