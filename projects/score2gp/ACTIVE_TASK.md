# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-02 — Read the remaining unread-symbol classes: accidental beside notehead, rests, marks over and under noteheads, tuplets, parenthesised heads

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-02-read-next-unread-symbol-class`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Read the next largest honestly readable unread-symbol class, measured on the current runtime. REFUSE-01B (natural signs, merged as #530) moved the 43-PDF baseline from 672 written and 134 refused to 682 and 124, and its report lists what still occurs (leads, re-measure): accidental beside notehead (38 unread, many as rest_sized_curve), over or under notehead (17 unread, 87 ignored), rests (9 unread), tuplet numbers (2 unread). Also diagnose Hey Joe and Pride and Joy (pdf_only_tab_grouping_unsafe with a score) and Black Dog (every bar refused). Real approved sources carry acceptance.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
