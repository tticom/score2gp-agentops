# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: CP-19 — Align reconciliation PRs with TASK_RECORDING_CONVENTION.md: dated reconciliation record

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/cp-19-reconciliation-dated-record`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Non-blocking process note from tticom-codex's approving review of tticom/score2gp-agentops#730 (thread at ORCHESTRATION_STATE.json:1749): the convention calls for a dated reconciliation record alongside a completed task, while #726 and #730 record completion only in the authority and the exact-head handback. Either add the dated record to reconcile_promote (and backfill OMIT-01 and OMIT-02) or amend the convention to recognise the authority record plus the handback.

## Allowed paths

- `scripts/*.py`
- `projects/score2gp/TASK_RECORDING_CONVENTION.md`
- `projects/score2gp/handoffs/*.md`
- `tests/test_cp_19_*.py`

## Validation commands

- `python -m pytest`
- `PYTHONUTF8=1 python scripts/score2gp_governance_audit.py`
- `git diff --check`
