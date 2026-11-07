# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: RASTER-00 — Scope the scanned and hand-drawn sources that need raster reading

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/raster-00-scope-the-scanned-and-hand-drawn-sources`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

NOROUTE-01 found three approved sources that are images, not vector pages: two scanned books (177 and 105 pages, notation and TAB staves, 0 vector drawings and 1 image per page) and a one-page hand-drawn source. They are real teaching material and the largest unread share of the corpus. Reading them needs raster recognition, which is the territory of the REC recognition items and DEC-01 (still undecided), so this task scopes and measures; it does not build the recogniser. Leads, not facts: re-measure.

## Allowed paths

- `src/score2gp/**`
- `tests/**`
- `docs/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
