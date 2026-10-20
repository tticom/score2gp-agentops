# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: MEM-03 — Bound the work-directory footprint of a conversion and add a resource budget test

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/mem-03-bound-workdir-footprint`

**Pull Request**: 505

**Owner Role**: implementation

## Objective

One Lesson 3 conversion wrote 160 MB in 23 files (score.ir.json 51 MB, conversion-report.html 50 MB, tab/tab_raw.json 22 MB, inspect_pdf.json 16 MB written twice). MEM-02 fixes the report. Remove the duplicate inspect output, make heavy diagnostics opt-in, and add budgets for peak memory and bytes written per bar so regressions fail.

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
