# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: UNREAD-01 — Unclassified notation symbols refuse whole bars

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/unread-01-classify-notation-symbols`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

note_duration_event_unread is the largest bar-level refusal in the 2026-10-08 survey (34 bars: Derek Trucks BB King 19 of 20 bars, G-Am-C-Lick 8 of 9, The_EXACT_System 5, Am-blues-lick 1, Just-Practice 1), with the detail symbol_unclassified and, for Derek Trucks, 29 key_clef_unread records. Census the unclassified symbols and key/clef forms, read the standard-notation classes by a staff-space-relative rule, and give every other symbol a located unread event naming its class (never a silent drop). Folds in DUR-01-FU1. Derek Trucks BB King has a reference .gp and is the measurable target.

## Allowed paths

- `src/score2gp/notation_omr/**`
- `src/score2gp/pdf_tab_duration_associator.py`
- `src/score2gp/pdf_tab_duration_types.py`
- `src/score2gp/pdf_tab_bar_assembler.py`
- `src/score2gp/pdf_tab_event_factory.py`
- `tests/test_dur_02_oracle.py`
- `tests/test_dur_02_*.py`
- `tests/test_unread_01_*.py`
- `tests/fixtures/pdf/unread_01/**`
- `docs/design/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
