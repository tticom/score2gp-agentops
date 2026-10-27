# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: CP-12 — Remove the stale promotion rule from the CR-04D refactor-sequence plan and close the oracle gap

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/cp-12-remove-stale-promotion-rule`

**Pull Request**: 879

**Owner Role**: implementation

## Objective

Remove the stale promotion rule from the CR-04D refactor-sequence plan and close the oracle gap. Source: authority item CP-12. Found 2026-09-26 after PLAN-01 merged (the 'Promotion Rule' section, line 42). tests/test_single_backlog.py did not flag it because the line uses no planning-container word; the fix should also close that oracle gap or record why it is out of scope.

## Allowed paths

- `projects/score2gp/plans/2026-07-26-cr04d-pdf-tab-measure-assembly-refactor-sequence.md`
- `tests/test_single_backlog.py`
- `tests/test_cp_12_*.py`

## Validation commands

- `python -m pytest`
- `PYTHONUTF8=1 python scripts/score2gp_governance_audit.py`
- `git diff --check`
