# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REC-03 — Canonical Vector and Text Observations

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/rec-03-vector-text-observations`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Implement the vector/text evidence adapter and reconstruct canonical strokes, glyphs and text spans without assigning musical meaning.

## Allowed paths

- `src/score2gp/recognition/observations.py`
- `tests/recognition/test_observations.py`
- `src/score2gp/pdf.py`

## Validation commands

- `python3 -m pytest tests/recognition/test_observations.py`
- `python3 -m mypy src/score2gp/recognition/observations.py tests/recognition/test_observations.py`
- `python3 scripts/artifact_audit.py`
