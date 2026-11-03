# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-09 — Read stem flags that are unread or unidentified

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-09-flag-glyphs`

**Pull Request**: 543

**Owner Role**: implementation

## Objective

REFUSE-07 measured flag_glyph_unread (6 bars), flag_glyph_unidentified (3 bars) and grace_note_unsupported_flag_count (1 bar) among the refusals. A flag count on a stem fixes the note type. Measure why the flags are unread or unidentified (overlap with beams, glyph variants, stem geometry) and read the flags only where the count is unambiguous from the drawn glyphs. Leads, not facts: re-measure on the current runtime.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
