# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REC-05 — Raster Observation Adapter

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/rec-05-raster-observation-adapter`

**Pull Request**: 460

**Owner Role**: implementation

## Objective

Add deterministic page rendering and a typed raster evidence adapter that is a peer of vector/text evidence, not a fallback source of final semantics.

## Allowed paths

- `src/score2gp/recognition/raster.py`
- `tests/recognition/test_raster.py`

## Validation commands

- `python3 -m pytest tests/recognition/test_raster.py`
- `python3 -m mypy src/score2gp/recognition/raster.py tests/recognition/test_raster.py`
