# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: ORC-04 — Integrated PR Lifecycle and Concurrent Review Routing

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/orc-04-integrated-pr-lifecycle`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Make each agent cycle open its PR, route exact-head reviews across independent roles, and support isolated concurrent tasks with verified post-merge reconciliation.

## Allowed paths

- `agent-runtime/assignment_adapter.py`
- `agent-runtime/cycle.py`
- `agent-runtime/scripts/start-instance.sh`
- `scripts/score2gp_dispatch.py`
- `scripts/score2gp_go_bootstrap.py`
- `scripts/score2gp_got_bootstrap.py`
- `scripts/score2gp_orchestrator.py`
- `scripts/score2gp_orca_control.py`
- `tests/test_assignment_adapter.py`
- `tests/test_disposable_cycle.py`
- `tests/test_score2gp_orca_control.py`
- `tests/test_score2gp_orchestrator.py`

## Validation commands

- `python3 -m pytest tests/test_assignment_adapter.py tests/test_disposable_cycle.py tests/test_score2gp_orca_control.py tests/test_score2gp_orchestrator.py`
- `python3 -m compileall -q agent-runtime scripts`
