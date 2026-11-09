# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: GROUP-03 — Resolve the sources that are still refused at TAB grouping

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/group-03-remaining-grouping-unsafe-sources`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Four sources remain refused with pdf_only_tab_grouping_unsafe after GROUP-01 and TABRHY-01. They are real teaching material. Leads, not facts: re-measure which check raises the refusal per source (quote the code), the systems and bars found, and which warning blocks it. Raise the grouping resolution where the geometry makes the grouping determinable; never loosen the safety check.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
