# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-01B — Reduce refused bars by reading the largest honestly readable unread class, measured on the current runtime

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-01b-reduce-refused-bars-current-runtime`

**Pull Request**: 530

**Owner Role**: implementation

## Objective

Reduce refused bars on the approved private PDFs by reading the largest honestly readable class of unread symbol or bar, measured on the current runtime. Replaces REFUSE-01, whose premise (thin bands) was stale: those bands are beams already owned. Baseline from the REFUSE-01 author run (leads, re-measure): 43 PDFs, 672 bars written, 134 refused: note_duration_event_unread 63, notation_note_without_tab_digit 25, bar_total_mismatch 18, bar_without_notation_event 15, notehead_digit_count_mismatch 11; residual unclassified symbols are arpeggio fragments, bend curves and vibrato marks. The older REFUSE-02 counts (accidental beside notehead 93, rests 37, over or under notehead 35, tuplet numbers 31) came from the same stale survey and must be re-measured too.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
