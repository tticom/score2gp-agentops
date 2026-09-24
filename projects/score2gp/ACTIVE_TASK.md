# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: WIN-04 — Post-migration governance hygiene and test decoupling

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/win-04-post-migration-governance-hygiene`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Remove stale agy-cycle and agy-skills references, and decouple governance tests from live authority and untracked files. Agent merge authority is out of scope and belongs to a separate governance task.

## Allowed paths

- `docs/agy-cycle.md`
- `projects/score2gp/prompts/next/go-dispatch.md`
- `tests/test_governance_audit.py`
- `tests/test_score2gp_dispatch.py`

## Validation commands

- `python scripts/score2gp_governance_audit.py`
- `python -m pytest tests/test_governance_audit.py tests/test_score2gp_dispatch.py`
- `python -m pytest`
- `git diff --check`
