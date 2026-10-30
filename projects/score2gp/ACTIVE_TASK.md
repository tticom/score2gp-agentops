# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: CP-16 — Governance audit binds an open task PR against the task record on main, not the copy on the PR's own branch

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/cp-16-audit-binds-task-record-on-main`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

This task is gate-adjacent. It may only make the gate read the evidence it already reads more correctly; no review, merge or audit check may be removed, loosened or reordered, and anything that was denied for a real reason stays denied. Seen 2026-09-27 on #713 (CP-13): governance recorded pull_request 713 on main (#714), but the audit reads the authority in the checkout, so at the PR head it still saw TBD and failed until the author merged origin/main into the branch. Every AgentOps task PR hits this, because the PR number exists only after the branch is cut.

## Allowed paths

- `scripts/score2gp_governance_audit.py`
- `tests/test_cp_16_*.py`
- `tests/test_governance_audit.py`

## Validation commands

- `python -m pytest`
- `PYTHONUTF8=1 python scripts/score2gp_governance_audit.py`
- `git diff --check`
