# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REC-00 — Recognition Domain Contract and Supersession Ledger

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `codex/rec-00-recognition-domain-contract`

**Pull Request**: TBD

**Owner Role**: architect

## Objective

Define the canonical recognition vocabulary, stage invariants, failure taxonomy, and auditable mapping from superseded geometry-first tasks into the topology-first recognition programme without changing product behaviour.

## Allowed paths

- `projects/score2gp/CONTEXT.md`
- `projects/score2gp/decisions/recognition-architecture-v1.md`
- `projects/score2gp/tasks/2026-08-27-recognition-architecture-backlog.md`

## Validation commands

- `git diff --check`
- `python3 scripts/score2gp_governance_audit.py`
- `python3 -m pytest -q tests/test_score2gp_orchestrator.py tests/test_governance_audit.py`
