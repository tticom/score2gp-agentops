# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: AUT-01 — Consolidate the autonomous development loop

**Status**: IN_PROGRESS

**Repository**: tticom/score2gp-agentops

**PR Branch**: `codex/autonomous-development-loop`

**Pull Request**: 573

**Owner Role**: architect

## Objective

Make ORCHESTRATION_STATE.json the sole machine authority and expose one deterministic, idempotent advance(live_state) decision interface while retaining explicit compatibility adapters.

## Allowed paths

- `projects/score2gp/ACTIVE_TASK.md`
- `projects/score2gp/AGENT_CONTROL.md`
- `projects/score2gp/ORCHESTRATION_STATE.json`
- `scripts/score2gp_governance_audit.py`
- `scripts/score2gp_orca_control.py`
- `scripts/score2gp_orchestrator.py`
- `tests/test_score2gp_orca_control.py`
- `tests/test_score2gp_orchestrator.py`

## Validation commands

- `../score2gp/.venv/bin/python -m pytest -q tests/test_score2gp_orchestrator.py tests/test_score2gp_orca_control.py tests/test_score2gp_dispatch.py`
- `../score2gp/.venv/bin/python -m pytest -q tests`
- `python3 scripts/score2gp_governance_audit.py`
- `git diff --check origin/main...HEAD`
