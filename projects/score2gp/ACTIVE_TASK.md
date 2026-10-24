# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: PERC-01 — Castles Made of Sand.pdf and Crossroads.pdf: write the bars as printed, or refuse them with a located reason; write every printed percussive strike

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/perc-01-castles-crossroads-percussive-strikes`

**Pull Request**: 512

**Owner Role**: implementation

## Objective

Castles Made of Sand.pdf and Crossroads.pdf: write the bars as printed, or refuse them with a located reason; write every printed percussive strike. Source: authority item PERC-01. Maintainer 2026-10-22: both PDFs contain percussive strikes (dead-note X heads) and neither has a reference .gp. Survey 2026-10-20: both REFUSED with pdf_only_tab_grouping_unsafe, so the strike cannot be judged until the bars are written; depends on the grouping work and on the G-Am-C-Lick.pdf tasks. Oracle: the PDF's own notation and TAB plus the maintainer's check by ear and eye; no reference may be invented. Follow the storage convention in the percussive-strike decision (UNREAD-02). Needs detail: which grouping cause blocks each file and whether it is one shared fix.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
