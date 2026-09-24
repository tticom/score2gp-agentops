# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: WIN-04 — Post-migration governance hygiene and merge-rule alignment

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/win-04-post-migration-governance-hygiene`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Remove stale agy-cycle and agy-skills references, restate live merge rules to the maintainer's 2026-09-24 decision, and decouple governance tests from live authority and untracked files.

## Allowed paths

- `docs/agy-cycle.md`
- `projects/score2gp/prompts/next/go-dispatch.md`
- `AGENTS.md`
- `CLAUDE.md`
- `projects/score2gp/AGENT_CONTROL.md`
- `tests/test_governance_audit.py`
- `tests/test_score2gp_dispatch.py`
- `tests/test_score2gp_control_plane.py`
- `.agents/skills/score2gp-project-director/SKILL.md`
- `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md`
- `projects/score2gp/prompts/next/got-dispatch.md`
- `skills/score2gp-pr-hard-review.md`
- `skills/score2gp-task-orchestration.md`
- `tests/test_dispatch_entrypoint_contract.py`
- `projects/score2gp/prompts/next/win-04-post-migration-governance-hygiene.md`

## Validation commands

- `python scripts/score2gp_governance_audit.py`
- `python -m pytest tests/test_governance_audit.py tests/test_score2gp_dispatch.py tests/test_score2gp_control_plane.py tests/test_dispatch_entrypoint_contract.py`
- `python -m pytest`
- `git diff --check`
