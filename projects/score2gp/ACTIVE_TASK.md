# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: WIN-01 — OS-Agnostic Governance and Dispatch

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/win-01-windows-native-execution`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Make Score2GP governance, dispatch and validation OS-agnostic: resolve the worker role from the authenticated GitHub login cross-checked against the workspace path, resolve Python and tools portably, and remove WSL, /home and .venv/bin mandates from live governance, without altering product recognition semantics.

## Allowed paths

- `projects/score2gp/AGENT_CONTROL.md`
- `projects/score2gp/ORCA_WORKFLOW.md`
- `projects/score2gp/SKILLS_LOCK.md`
- `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md`
- `projects/score2gp/prompts/next/address-current-pr-review.md`
- `projects/score2gp/prompts/next/got-dispatch.md`
- `CLAUDE.md`
- `.agents/agents/project-director/agent.json`
- `scripts/link_session.py`
- `scripts/score2gp_control_plane.py`
- `scripts/score2gp_dispatch.py`
- `scripts/score2gp_go_bootstrap.py`
- `scripts/score2gp_got_bootstrap.py`
- `scripts/score2gp_orca_control.py`
- `scripts/verify_identity.py`
- `tests/conftest.py`
- `tests/test_dispatch_entrypoint_contract.py`
- `tests/test_governance_audit.py`
- `tests/test_score2gp_control_plane.py`
- `tests/test_score2gp_dispatch.py`
- `tests/test_score2gp_orchestrator.py`
- `tests/test_score2gp_orca_control.py`
- `tests/test_verify_identity.py`

## Validation commands

- `python scripts/score2gp_governance_audit.py`
- `python -m pytest tests/test_score2gp_dispatch.py tests/test_score2gp_orchestrator.py tests/test_score2gp_orca_control.py tests/test_verify_identity.py tests/test_dispatch_entrypoint_contract.py tests/test_governance_audit.py tests/test_score2gp_control_plane.py`
- `python -m pytest`
- `git diff --check`
