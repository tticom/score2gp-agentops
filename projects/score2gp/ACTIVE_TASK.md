# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-03 — Measure and reduce alignment and total-mismatch bar refusals

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-03-alignment-and-total-mismatch-refusals`

**Pull Request**: 535

**Owner Role**: implementation

## Objective

Measure and reduce the refused bars that REFUSE-02 does not cover. On the 43-PDF baseline the refusals by code were (leads, re-measure): notation_note_without_tab_digit 25, bar_total_mismatch 18, bar_without_notation_event 15, notehead_digit_count_mismatch 11, mixed_percussive_tie_ownership_unread 2. REFUSE-02 handles note_duration_event_unread (unread symbols); this task handles the alignment and total-mismatch classes, where notation and TAB disagree or a bar has no notation event. Some refusals may be correct (the source is wrong, ambiguous or not music); those stay refused with a clearer reason.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
