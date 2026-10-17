# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: MEM-02 — Conversion report: replace the 49 MB barline-candidate dump with a bounded summary

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/mem-02-bounded-conversion-report`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

`conversion-report.html` for Lesson 3 is about 50 MB, almost all one `<pre>` block pretty-printing every rejected barline candidate's geometry. A user cannot open that. Summarise by reason with counts and located examples; write the full dump only behind an explicit debug flag.

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
