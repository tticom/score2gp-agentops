# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: RES-REQ-0003 — Research to take REQ-0003 to ACCEPTED: dependency licence audit and PDF-library options

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/res-req-0003-dependency-licence-compatibility`

**Pull Request**: TBD

**Owner Role**: architect

## Objective

Establish the facts the maintainer needs to accept REQ-0003: a licence inventory of every runtime and build dependency, a measured comparison of pymupdf against permissive PDF libraries on Lesson 3, a proposed mechanical CI audit, and a status proposal. Records only: no product code or dependency change, no legal conclusions.

## Allowed paths

- `projects/score2gp/requirements/REQ-0003-dependency-licence-compatibility.md`
- `projects/score2gp/reports/**`
- `projects/score2gp/prompts/next/res-req-0003-dependency-licence-compatibility.md`

## Validation commands

- `python -m pytest`
- `PYTHONUTF8=1 python scripts/score2gp_governance_audit.py`
- `git diff --check`
