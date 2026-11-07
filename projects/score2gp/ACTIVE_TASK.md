# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: PERF-02 — Reduce retained inspection data so a long source fits the existing resource budget

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/perf-02-reduce-retained-inspection-data`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

NOROUTE-01 found that a 34-page notation-and-TAB source stops with pdf_resource_inspection_page_nodes_exceeded (2,060,433 nodes against the 2,000,000 PERF-01 budget, at page index 10). PERF-01 is a protected resource limit and is not touched: the fix is to retain less inspection data, not to raise or bypass the budget. Leads, not facts: re-measure which structures hold the nodes (per-page drawing, glyph and text objects kept after they are no longer needed) and how much each contributes. This is also a first measured step toward the Rust bottleneck list.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
