# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: WIN-01 — Windows-Native Primary Execution Migration

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/win-01-windows-native-execution`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Remove mandatory WSL dependency, establish Windows-native primary execution with PowerShell/Python/Git/gh compatibility, and preserve WSL as an optional secondary environment without altering product recognition semantics.

## Allowed paths

- `projects/score2gp/AGENT_CONTROL.md`
- `projects/score2gp/ORCA_WORKFLOW.md`
- `projects/score2gp/prompts/next/address-current-pr-review.md`
- `CLAUDE.md`
- `agent-runtime/README.md`
- `agent-runtime/policies/README.md`
- `scripts/score2gp_dispatch.py`
- `scripts/score2gp_go_bootstrap.py`
- `scripts/score2gp_got_bootstrap.py`
- `scripts/score2gp_orca_control.py`
- `scripts/verify_identity.py`
- `scripts/verify_identity.ps1`
- `tests/conftest.py`
- `tests/test_agent_runtime.py`
- `tests/test_agy_cycle.py`
- `tests/test_codex_runtime.py`
- `tests/test_score2gp_dispatch.py`
- `tests/test_score2gp_orchestrator.py`
- `tests/test_score2gp_orca_control.py`
- `tests/test_verify_identity.py`

## Validation commands

- `python scripts/score2gp_governance_audit.py`
- `python -m pytest tests/test_score2gp_dispatch.py tests/test_score2gp_orchestrator.py tests/test_score2gp_orca_control.py`
- `python -m pytest`
- `git diff --check`
