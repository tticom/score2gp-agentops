# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: L3-00 — Lesson 3 native source contract and red acceptance

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/l3-00-native-acceptance`

**Pull Request**: 462

**Owner Role**: implementation

## Objective

Produce a trustworthy private source manifest and repeatable red end-to-end native acceptance result, with the earliest source-located divergence and one bounded next implementation seam.

## Allowed paths

- `scripts/native_slice_acceptance.py`
- `scripts/native_slice_reference.py`
- `tests/test_native_slice_acceptance.py`
- `tests/test_lesson3_native_acceptance.py`

## Validation commands

- `python3 -m pytest tests/test_native_slice_acceptance.py tests/test_lesson3_native_acceptance.py`
- `python3 scripts/native_slice_acceptance.py --help`
- `python3 scripts/artifact_audit.py`
- `git diff --check`
