# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: PDFG-01 — Mixing Lead & Rhythm pt1 and PARANOID refused with pdf_only_tab_grouping_unsafe: find the cause, fix it or locate it

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/pdfg-01-refused-new-fixtures`

**Pull Request**: 492

**Owner Role**: implementation

## Objective

Two of the three newest private fixtures are refused wholesale with `pdf_only_tab_grouping_unsafe`, so a user converting either gets nothing. Find which grouping condition fires and why, fix the cause where the PDF evidence is unambiguous, and otherwise narrow the refusal to the bars that are actually unsafe.

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
