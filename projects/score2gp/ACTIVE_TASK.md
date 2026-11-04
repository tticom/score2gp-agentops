# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-13 — Read bend-target heads that carry no TAB digit

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-13-bend-target-heads`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

REFUSE-12's whole-set measurement left this class unread: notation_note_without_tab_digit / no_tab_column_at_notation_event, about 15 bars across 4 sources, mostly bend-target heads. Check the bend acceptance recorded in TABRHY-01 and reuse its representation. Re-measure on the current runtime first. Read the class only where the drawn notation settles it (note type, grouping, a glyph whose meaning is fixed); extend the score model and writer only as far as the printed symbol requires, and leave everything else refused with its located reason. If the class cannot be read without counting or spacing inference, stop and report the located evidence. Leads, not facts.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
