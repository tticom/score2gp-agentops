# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: LAYOUT-01-FU1 — pdf_systems_layout_fallback: report the source system total, not the bars consumed so far

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/layout-01-fu1-fallback-source-total`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

The row-layout fallback message reports 'source bars N' as the bars up to the offending system, not the source total, which makes the diagnostic misleading to a user. Report both counts correctly and pin the message with a test.

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
