# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-06 — Reduce the largest remaining unread-symbol class

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-06-next-unread-symbol-class-after-tabrhy`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Measure and reduce the largest remaining class of note_duration_event_unread, which after REFUSE-04 stands at 107 bars (leads from earlier measurement, re-measure): symbol_unclassified, grace_note_in_tuplet, rest_glyph_unidentified, unclassified_same_position_arc, parenthesized_head_unrepresented, rest_glyph_beside_note, accidental beside a notehead (non-natural), flag_glyph_unidentified. Pick by bar count and by whether the symbol is unambiguously musical.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
