# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: TABEXT-02 — Read the remaining bars that still lack a TAB column

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/tabext-02-read-the-remaining-no-tab-column-bars`

**Pull Request**: 558

**Owner Role**: implementation

## Objective

TABEXT-01 (merged) left 9 no_tab_column bars unfinished: adjacent-fret glyph runs, a tied chord with an empty bracket, a grace-note bend target, and 4 unsettled. REFUSE-13 split the class the same way: the extraction excludes digits before the route (pdf_fret_digits_not_merged_exceeds_max_fret, pdf_fret_digit_symbol_overlap_ambiguous, pdf_fret_multidigit_extracted). Leads, not facts: re-measure. TABEXT-01 also added about 120 s over 73 pages for its extra pass; keep any further pass off sources that do not need it.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
