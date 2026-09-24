# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: GOV-02 — Isolate governance-audit tests from the live receipt audit

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/gov-02-receipt-audit-test-isolation`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Make the main()-level governance-audit tests independent of whether live authority enables the GOV-01 receipt audit, without changing audit behaviour, so governance can set merge_policy.executor_audit_since.

## Allowed paths

- `tests/test_governance_audit.py`
- `scripts/score2gp_governance_audit.py`

## Validation commands

- `python scripts/score2gp_governance_audit.py`
- `python -m pytest tests/test_governance_audit.py`
- `python -m pytest`
- `git diff --check`
