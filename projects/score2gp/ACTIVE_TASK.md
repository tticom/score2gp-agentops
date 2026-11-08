# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: TABEXT-03 — Group the TAB digits that are printed but never reach a bar

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/tabext-03-digits-printed-but-not-grouped`

**Pull Request**: 562

**Owner Role**: implementation

## Objective

REFUSE-17 found 7 bars (6 in one TAB-only source, 1 in another) that print digits TabRaw holds only as ungrouped text (tab_digits_printed_but_not_grouped), and 23 bars refused as bar_without_notation_or_tab_item where digits are printed that TabRaw never saw. Both are TAB extraction gaps in real teaching material. Leads, not facts: re-measure, view each bar.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
