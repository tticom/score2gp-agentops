# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-17 — Explain and read the bars that have no notation event and no TAB item

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-17-bars-with-no-notation-and-no-tab-item`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

29 bars across the approved sources are refused as bar_without_notation_event / bar_without_notation_or_tab_item, and TABGUESS-01's measurement found 0 TAB columns in all of them (22 + 4 + 2 + 1 by source), so no spacing model can reach them. They are bars of real teaching material. Leads, not facts: re-measure, view the page for every bar, and decide per group what it is: a printed rest bar, a repeat or volta bar, a bar with only chord names or text, a bar whose TAB the extraction missed (see TABEXT-01 and TABEXT-02), a stub, or something else.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
