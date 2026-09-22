# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: WIN-01 — Windows-Native Primary Execution Migration

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/win-01-windows-native-execution`

**Pull Request**: TBD

**Owner Role**: governance

## Objective

Remove mandatory WSL dependency, establish Windows-native primary execution with PowerShell/Python/Git/gh compatibility, and preserve WSL as an optional secondary environment without altering product recognition semantics.

## Allowed paths

- `projects/score2gp/AGENT_CONTROL.md`
- `projects/score2gp/CLAUDE.md`
- `CLAUDE.md`
- `scripts/score2gp_dispatch.py`
- `scripts/score2gp_go_bootstrap.py`
- `scripts/score2gp_got_bootstrap.py`
- `scripts/verify_identity.sh`
- `scripts/verify_identity.py`
- `tests/test_score2gp_dispatch.py`
- `tests/test_score2gp_orchestrator.py`

## Validation commands

- `python3 scripts/score2gp_governance_audit.py`
- `python3 -m pytest tests/test_score2gp_orchestrator.py tests/test_score2gp_orca_control.py`
- `git diff --check`
