# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: TABEXT-01 — Read the fret digits that TAB extraction excludes before the route

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/tabext-01-read-fret-digits-excluded-before-the-route`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

REFUSE-13's whole-set measurement (46 PDFs, 863 bars written) found that the largest honest part of notation_note_without_tab_digit / no_tab_column_at_notation_event is not a notation problem: about 8 bars in 4 sources print ordinary fret digits (chords and single notes) that TabRaw excluded before the route, under pdf_fret_page_or_legend_number_excluded, pdf_fret_multidigit_extracted, pdf_fret_digits_not_merged_exceeds_max_fret and pdf_fret_digit_symbol_overlap_ambiguous. One more bar is a tied chord whose TAB digits are bracketed at a system start, and one TAB row of a staffless source loses its digits the same way. Leads, not facts: re-measure. Read a digit as a fret only where its position on a string line and its size make it unambiguous; a number that is a page number, a legend or a tempo mark must stay excluded.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
