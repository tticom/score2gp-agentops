# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: ORC-02 — Agent Isolation & Control-Plane Cutover

**Status**: IN_PROGRESS

**Repository**: tticom/score2gp

**PR Branch**: `chore/orc-02-agent-isolation`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Isolate all agent instructions to the agentops repository, leaving the score2gp repository completely free of agentic governance files. Execute the state cutover to formally retire legacy `go` and `got` commands.

## Allowed paths

- `*`

## Validation commands

- `git diff --check`
- `python3 -m pytest tests/test_score2gp_orca_control.py`
