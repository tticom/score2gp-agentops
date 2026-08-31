# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REC-02 — Recognition Contract Schemas

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/rec-02-recognition-contract-schemas`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Create versioned, frozen contracts for DocumentObservations, DocumentTopology, RecognitionGraph, ResolutionResult and MusicalDocument without changing runtime recognition or export behaviour.

## Allowed paths

- `src/score2gp/recognition/schemas.py`
- `tests/recognition/test_schemas.py`

## Validation commands

- `python3 -m pytest tests/recognition/test_schemas.py`
- `python3 -m mypy src/score2gp/recognition/schemas.py tests/recognition/test_schemas.py`
- `python3 scripts/artifact_audit.py`
- `python3 scripts/regenerate_recognition_schemas.py`
