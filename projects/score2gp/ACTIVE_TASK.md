# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: CRP-01 — Port and Harmonize Barline Detection & Geometry Cleanup

**Status**: IN_PROGRESS

**Repository**: tticom/score2gp

**PR Branch**: `feat/crp-01-barline-detection`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Port valid barline detection thresholds from PR 418 into src/score2gp/pdf.py, revert the outer_tolerance = 300.0 geometry snapping hack, and enforce staff-relative barline height bounds without mutating higher-level layout models.

## Allowed paths

- `src/score2gp/pdf.py`
- `tests/test_pdf.py`
- `tests/test_pdf_geometry_candidate_extractor.py`

## Validation commands

- `python3 -m pytest tests/test_pdf_geometry_candidate_extractor.py tests/test_pdf.py`
