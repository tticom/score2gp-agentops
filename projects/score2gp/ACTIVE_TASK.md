# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REC-04 — Local Scale Model

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/rec-04-local-scale-model`

**Pull Request**: 459

**Owner Role**: implementation

## Objective

Estimate local notation, TAB, stroke and glyph scales and express new detector policies in dimensionless units.

## Allowed paths

- `src/score2gp/recognition/scale.py`
- `tests/recognition/test_scale.py`

## Validation commands

- `python3 -m pytest tests/recognition/test_scale.py`
- `python3 -m mypy src/score2gp/recognition/scale.py tests/recognition/test_scale.py`
