# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: L3-01 — Paired-staff barline acceptance for the Lesson 3 first system

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/l3-01-paired-staff-barline-acceptance`

**Pull Request**: 464

**Owner Role**: implementation

## Objective

Stop notation-staff note stems being inherited as system barlines so the Lesson 3 first system yields exactly its 4 adjudicated boundaries and 3 bar boxes, without regressing existing TAB-missed barline recovery.

## Allowed paths

- `src/score2gp/pdf.py`
- `tests/test_paired_staff_barline_acceptance.py`
- `tests/test_lesson3_native_acceptance.py`
- `tests/test_pdf.py`
- `tests/test_npg_05_irregular_layout_real.py`

## Validation commands

- `python -m pytest tests/test_paired_staff_barline_acceptance.py tests/test_barline_recovery.py tests/test_pdf.py`
- `python -m pytest tests/test_native_slice_acceptance.py tests/test_lesson3_native_acceptance.py`
- `python -m pytest`
- `python scripts/artifact_audit.py`
- `git diff --check`
