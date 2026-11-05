# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-15 — Read hammer-on / pull-off clusters of adjacent heads

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-15-hammer-pull-clusters`

**Pull Request**: 549

**Owner Role**: implementation

## Objective

REFUSE-12's whole-set measurement left this class unread: notehead_digit_count_mismatch (about 11 bars after REFUSE-12), mostly hammer-on/pull-off clusters of adjacent heads. The slur arc between adjacent heads fixes the technique; Lesson-5.gp and other readable references are the check. Re-measure on the current runtime first. Read the class only where the drawn notation settles it (note type, grouping, a glyph whose meaning is fixed); extend the score model and writer only as far as the printed symbol requires, and leave everything else refused with its located reason. If the class cannot be read without counting or spacing inference, stop and report the located evidence. Leads, not facts.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
