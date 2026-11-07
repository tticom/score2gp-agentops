# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-18 — Reduce the largest remaining unread-duration class

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-18-largest-unread-duration-class-after-tsig`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

After TSIG-01 to PERF-02 the whole-set ranking is led by note_duration_event_unread at 88 bars (reader gap), including tab_column_without_rhythm_mark and unclassified_mark_below_strings in the newly routed TAB-only source. Leads, not facts: re-measure on the current runtime and pick by bar count and by whether the symbol is unambiguously musical.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
