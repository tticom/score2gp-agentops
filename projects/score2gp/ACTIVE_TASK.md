# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: GROUP-01 — Raise the TAB grouping resolution for sources refused at grouping

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/group-01-raise-grouping-resolution-refused-sources`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Nine private sources produce no route because they are refused at grouping (pdf_only_tab_grouping_unsafe, ambiguous_bar_assignment), including two that carry a score. REFUSE-02 found these are a grouping problem, not an unread symbol, and TABRHY-01 raised the grouping resolution for staffless TAB only. This task measures the rest. Raise the grouping resolution only where the evidence (staff and TAB line geometry, barlines, digit positions) makes the grouping safely determinable; do not loosen or bypass the safety check. The maintainer's standing view: the grouping safety or resolution needs to be increased until the TAB is safely determinable.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
