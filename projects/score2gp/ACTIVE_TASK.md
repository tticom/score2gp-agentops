# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: NOTAB-01 — Explain and read notation notes that have no TAB digit

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/notab-01-notes-without-a-tab-digit`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

After PERF-02 the whole-set ranking holds notation_note_without_tab_digit at 23 bars and notehead_digit_count_mismatch at 9 bars (both unknown). Part may be cascades from tied or unread neighbours, part rests or grace notes with no digit, part extraction gaps. Leads, not facts: re-measure, view each bar, and separate cascades from root causes.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
