# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-04 — Settle the alignment and total-mismatch refusals REFUSE-03 left unknown

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-04-settle-remaining-alignment-refusals`

**Pull Request**: 536

**Owner Role**: implementation

## Objective

Continue REFUSE-03. After it, 186 bars of the 43-PDF set are refused (leads, re-measure): note_duration_event_unread 107 (REFUSE-02 scope), bar_without_notation_event 26 (19 in one source whose detected staff has zero height, 5 blank stubs after a closing repeat barline or before the first barline, 2 elsewhere), notation_note_without_tab_digit 29 (11 with no TAB digit placed in the bar, 18 with differing counts), bar_total_mismatch 12, notehead_digit_count_mismatch 10, mixed_percussive_tie_ownership_unread 2. REFUSE-03 left these classified unknown. Settle them: for each class decide, from the printed notation and TAB together, whether the refusal is correct or a reader gap, and fix the largest reader gap. Refusals that are correct (blank stubs, evidence that really disagrees) stay refused with a clearer located reason.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
