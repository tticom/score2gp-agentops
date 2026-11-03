# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-08 — Read rest glyphs that the unread-duration refusals leave behind

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-08-rest-glyphs`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

REFUSE-07 measured the whole-set note_duration_event_unread ranking. Rests are unambiguous musical symbols: rest_glyph_beside_note (6 bars) and rest_glyph_unidentified (4 bars) are refused today. Measure why each rest glyph is not identified or is refused beside a note, and read rests whose glyph shape fixes their value (whole, half, quarter, eighth, sixteenth, with dots). Never read a rest from spacing. Leads, not facts: re-measure on the current runtime.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
