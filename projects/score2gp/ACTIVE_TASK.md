# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: GOV-01 — Delegated merge execution through the merge gate (audited)

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/gov-01-delegated-merge-execution`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Let tticom-codex and tticomgov-code merge through a sanctioned executor that runs verify_merge_gate on fresh live state and merges the exact reviewed head, detect any delegated merge without a matching executor receipt, and restate every live human-only merge rule; the maintainer accepted on 2026-09-24 that exclusivity is audited, not enforced.

## Allowed paths

- `scripts/score2gp_orca_control.py`
- `scripts/score2gp_control_plane.py`
- `tests/test_score2gp_orca_control.py`
- `tests/test_score2gp_control_plane.py`
- `tests/test_dispatch_entrypoint_contract.py`
- `.agents/rules/pr_standards.md`
- `.agents/skills/score2gp-project-director/SKILL.md`
- `AGENTS.md`
- `CLAUDE.md`
- `projects/score2gp/AGENT_CONTROL.md`
- `projects/score2gp/ORCA_WORKFLOW.md`
- `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md`
- `projects/score2gp/prompts/next/got-dispatch.md`
- `projects/score2gp/prompts/next/go-dispatch.md`
- `projects/score2gp/prompts/next/go-got-dispatcher.md`
- `projects/score2gp/skills/orca-supervisor/SKILL.md`
- `projects/score2gp/skills/project-director/SKILL.md`
- `projects/score2gp/templates/AGENT_TASK_TEMPLATE.md`
- `skills/score2gp-pr-hard-review.md`
- `skills/score2gp-task-orchestration.md`
- `skills/score2gp-project-director.md`
- `README.md`
- `docs/agy-cycle-v2-plan.md`
- `projects/score2gp/SIMPLE_AGENT_PROCESS.md`
- `scripts/score2gp_orchestrator.py`
- `scripts/score2gp_publish_review.py`
- `scripts/score2gp_governance_audit.py`
- `tests/test_score2gp_orchestrator.py`
- `tests/test_governance_audit.py`
- `tests/test_score2gp_publish_review.py`
- `.github/workflows/governance-control-plane.yml`

## Validation commands

- `python scripts/score2gp_governance_audit.py`
- `python -m pytest tests/test_score2gp_orca_control.py tests/test_score2gp_control_plane.py tests/test_dispatch_entrypoint_contract.py tests/test_score2gp_orchestrator.py tests/test_governance_audit.py tests/test_score2gp_publish_review.py`
- `python -m pytest`
- `git diff --check`
