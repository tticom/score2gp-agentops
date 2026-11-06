# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: TSIG-01 — Read the cut-time meter glyph that stops a TAB-only source before any bar

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/tsig-01-read-cut-time-glyph`

**Pull Request**: 555

**Owner Role**: implementation

## Objective

NOROUTE-01 found that one three-page TAB-only source with printed rhythm stops with pdf_only_tab_time_signature_unread (38 bars, first bar 0): the meter printed after the TAB clef is a 'C' with a vertical stroke, one contour about 1.9 by 3.5 staff spaces. The TAB rhythm reader reads stacked numerals only, and the notation reader's classify_common_cut rejects the contour (common_time_not_an_open_c). In standard engraving that glyph is cut time (2/2); the maintainer's expectation of that source is 4/4. Both have the same bar capacity, so the bar totals cannot tell them apart. Leads, not facts: re-measure.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
