# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-14 — Read ghost (parenthesized) heads and slurs over heads

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-14-ghost-and-parenthesized-heads`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

REFUSE-12's whole-set measurement left this class unread: parenthesized_head_unrepresented (6 bars), unsupported_overlapping_form (9) and symbol_unclassified (6). Ghost notes are drawn as a parenthesized head; decide per sub-class which are reader gaps. Re-measure on the current runtime first. Read the class only where the drawn notation settles it (note type, grouping, a glyph whose meaning is fixed); extend the score model and writer only as far as the printed symbol requires, and leave everything else refused with its located reason. If the class cannot be read without counting or spacing inference, stop and report the located evidence. Leads, not facts.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
