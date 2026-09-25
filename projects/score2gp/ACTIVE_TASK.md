# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: PLAN-01 — Single coherent backlog, with research tasks per requirement

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/plan-01-single-coherent-backlog`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Make ORCHESTRATION_STATE.json the single, machine-validated backlog: every planned item from every current planning source absorbed or dispositioned, every requirement traced to items, a dispatchable research task per requirement below ACCEPTED, and the superseded backlog sources removed.

## Allowed paths

- `projects/score2gp/ORCHESTRATION_STATE.json`
- `projects/score2gp/ACTIVE_TASK.md`
- `projects/score2gp/PLANNING_DATA.md`
- `projects/score2gp/tasks/**`
- `projects/score2gp/programmes/**`
- `plan/**`
- `.agy/**`
- `projects/score2gp/TASK_RECORDING_CONVENTION.md`
- `README.md`
- `projects/score2gp/README.md`
- `projects/score2gp/requirements/**`
- `projects/score2gp/prompts/next/res-*.md`
- `scripts/score2gp_orca_control.py`
- `scripts/score2gp_orchestrator.py`
- `tests/test_score2gp_orca_control.py`
- `tests/test_score2gp_orchestrator.py`
- `scripts/agy_cycle.py`
- `scripts/agy_spec_job.py`
- `docs/agy-cycle.md`
- `docs/agy-cycle-roadmap.md`
- `docs/agy-cycle-v2-plan.md`
- `docs/spec-job-orca.md`
- `requirements-agy-cycle.txt`
- `tests/test_agy_cycle.py`
- `tests/test_agy_spec_job.py`
- `projects/score2gp/plans/**`
- `projects/score2gp/AGENT_CONTROL.md`
- `projects/score2gp/ORCA_WORKFLOW.md`
- `projects/score2gp/skills/**`
- `skills/**`
- `projects/prompts/**`
- `.agents/agents/project-director/agent.json`
- `AGENT-RULES.md`
- `.agents/skills/**`
- `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md`
- `projects/score2gp/prompts/*.md`
- `docs/**`
- `tests/test_governance_audit.py`
- `tests/test_single_backlog.py`
- `projects/score2gp/prompts/next/agy-*.md`
- `.github/workflows/governance-control-plane.yml`

## Validation commands

- `python -m pytest`
- `python scripts/score2gp_governance_audit.py`
- `python scripts/score2gp_dispatch.py --product ../score2gp --agentops . --json`
- `git diff --check`
