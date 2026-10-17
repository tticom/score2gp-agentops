# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-02-FU1 — Write double bars in the reference GPIF shape only

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-02-fu1-double-bar-reference-shape`

**Pull Request**: 496

**Owner Role**: implementation

## Objective

The writer emits `<Barline>Double</Barline>` beside `<DoubleBar/>` on every recognised double bar while the five reference GPs contain no `<Barline>` element and encode the same bars with `<DoubleBar/>` only. Emit only the reference shape (DoubleBar, Repeat, start flag), and make the independent comparator fail on non-reference MasterBar children.

## Allowed paths

- `src/score2gp/**`
- `tests/**`
- `docs/**`
- `schemas/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
