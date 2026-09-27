# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: RES-REQ-0005 — Research to take REQ-0005 to ACCEPTED: map every silent gap, reason-code taxonomy, best-effort delivery options, shortfall record and report design

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/res-req-0005-explained-shortfalls`

**Pull Request**: 706

**Owner Role**: implementation

## Objective

Answer REQ-0005's open questions with evidence from the product code and real corpus runs, and turn its draft acceptance criteria into testable ones, so the maintainer can accept the requirement and implementation can be planned.

## Allowed paths

- `projects/score2gp/research/2026-09-26-res-req-0005-explained-shortfalls/**`
- `projects/score2gp/requirements/REQ-0005-explained-shortfall-reporting.md`
- `projects/score2gp/requirements/README.md`

## Validation commands

- `python -m pytest`
- `python scripts/score2gp_governance_audit.py`
- `git diff --check`
