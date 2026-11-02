# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-05 — Read augmentation dots painted in the page but absent from the reader's inputs

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-05-read-painted-augmentation-dots`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Read the augmentation dot that is painted in the page but absent from the drawings, text characters and font outlines the duration reader uses. REFUSE-04 (merged) found this is the largest suspected reader gap behind the short bar totals: in at least two sources a dotted rest or dotted eighth is painted, the reader counts no dot, the bar totals short (bar_total_mismatch, 12 bars, 10 short) and the following tied bar cascades into notation_note_without_tab_digit (29 bars, 10 of them cascades). Leads, not facts: re-measure on the current runtime. Read the dot from the rendered page (raster or font level) only where it is unambiguous; never infer it from the bar total.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
