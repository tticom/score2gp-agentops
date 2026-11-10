# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: MEM-04 — Bring the longest source's report and conversion time inside the existing allowances

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/mem-04-report-size-and-time-for-the-longest-source`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

PERF-02 let the 34-page source convert but it takes about 780 s and 1.8 GB, and its report is about 40.8 MB, 1.7 MB over the existing size allowance (tests/test_mem_02_report.py is a strict xfail for it). The allowance and the PERF-01 budget are protected and are not touched: the fix is to write less report and spend less time. Leads, not facts: re-measure by stage.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
