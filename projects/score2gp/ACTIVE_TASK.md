# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: CP-13 — Let Codex author assigned tasks, with crossed review

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/cp-13-codex-author-lane`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

The dispatcher lets a task's assigned author_login author it from its own slot, so tticom-codex can author research, architecture and product tasks (for example when Claude's usage allowance is exhausted), with crossed review and the non-author merge gate unchanged.

## Allowed paths

- `scripts/score2gp_dispatch.py`
- `scripts/score2gp_orca_control.py`
- `scripts/score2gp_orchestrator.py`
- `scripts/verify_identity.py`
- `scripts/score2gp_go_bootstrap.py`
- `scripts/score2gp_got_bootstrap.py`
- `tests/test_score2gp_dispatch.py`
- `tests/test_score2gp_orca_control.py`
- `tests/test_score2gp_orchestrator.py`
- `tests/test_cp_13_*.py`
- `CLAUDE.md`
- `projects/score2gp/AGENT_CONTROL.md`
- `projects/score2gp/TASK_RECORDING_CONVENTION.md`
- `projects/score2gp/ORCA_WORKFLOW.md`

## Validation commands

- `python -m pytest`
- `python scripts/score2gp_governance_audit.py`
- `git diff --check`
