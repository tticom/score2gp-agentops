# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: ORC-03 — Automated Post-Merge State Reconciliation

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `codex/orc-03-post-merge-state-reconciliation`

**Pull Request**: 639

**Owner Role**: governance

## Objective

Automate verified gate-completion transitions so merged tasks are reconciled into completed_tasks and the generated active view advances without manual state edits.

## Allowed paths

- `scripts/score2gp_orca_control.py`
- `scripts/score2gp_orchestrator.py`
- `scripts/score2gp_governance_audit.py`
- `tests/test_score2gp_orca_control.py`
- `tests/test_score2gp_orchestrator.py`
- `tests/test_governance_audit.py`

## Validation commands

- `python3 -m pytest tests/test_score2gp_orca_control.py tests/test_score2gp_orchestrator.py tests/test_governance_audit.py`
- `python3 scripts/score2gp_governance_audit.py`
- `python3 -m compileall -q scripts`
