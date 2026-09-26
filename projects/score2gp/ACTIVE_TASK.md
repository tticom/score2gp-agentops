# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: GOV-03 — Active-task PR discovery and fail-closed binding

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/gov-03-active-task-pr-discovery`

**Pull Request**: 703

**Owner Role**: implementation

## Objective

The dispatcher must never report no PR while one exists for the active task's repository, branch and base; route a discovered PR as bound for author and reviewer actions, fail closed on ambiguity, and keep the merge gate requiring the authority PR number.

## Allowed paths

- `scripts/score2gp_go_bootstrap.py`
- `scripts/score2gp_got_bootstrap.py`
- `scripts/score2gp_orca_control.py`
- `scripts/score2gp_governance_audit.py`
- `tests/test_score2gp_orca_control.py`
- `tests/test_score2gp_dispatch.py`
- `tests/test_governance_audit.py`

## Validation commands

- `python -m pytest`
- `python scripts/score2gp_governance_audit.py`
- `git diff --check`
