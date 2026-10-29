# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: FND-03B — Repair the GP writer's dangling chord diagram links

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/fnd-03b-repair-writer-chord-diagram-links`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Repair the GP writer so every chord diagram link points at a staff-local target that exists. Found by FND-03A's independent reader on 2026-10-29 (author-reported, zero-based locations to re-measure): output 04 has 4 dangling chord targets, output 09 has 12 (for example (0,0,0,0), (2,0,0,0)). Maintainer 2026-10-29: 'Create and prioritise the task.'

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
