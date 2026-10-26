# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: LAYOUT-01-FU3 — Remove the tautological assertion at tests/test_layout_01_public.py:55

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/layout-01-fu3-tautological-assertion`

**Pull Request**: 517

**Owner Role**: implementation

## Objective

Remove the tautological assertion at tests/test_layout_01_public.py:55. Source: authority item LAYOUT-01-FU3. Non-blocking follow-up 3 from review 5355475879 of tticom/score2gp#471 at b612713. tests/test_layout_01_public.py:55 asserts source_system_bars is None immediately after the test assigned counts, which is already None. The real assertions on the helper return and warning.provenance carry the check, so replace the line with an assertion that can fail, or delete it.

## Allowed paths

- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
