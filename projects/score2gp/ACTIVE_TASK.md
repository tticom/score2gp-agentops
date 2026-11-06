# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: NOROUTE-01 — Diagnose the PDFs that end without a route record

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/noroute-01-diagnose-pdfs-with-no-route-record`

**Pull Request**: 553

**Owner Role**: implementation

## Objective

REFUSE-15's measurement found 6 of 46 PDFs end without a route record because the CLI refuses before any bar is produced (4 with exit 4, 1 with exit 1, 1 with exit 2). REFUSE-02 and GROUP-01 turned two of the earlier grouping refusals into routes; these six remain. They are real teaching material (maintainer, 2026-11-04). Leads, not facts: re-measure.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
