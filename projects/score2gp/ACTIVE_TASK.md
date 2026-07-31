# Active Task

**Task**: AGENTOPS-PROMOTE-RESOLVED: Distinguish RESOLVED Tasks in Dispatcher State
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Governance Developer / Tooling Specialist
**Repository**: tticom/score2gp-agentops
**PR Branch**: `agy/agentops-promote-resolved-task`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0025-agentops-promote-resolved-task.md`

## Context

When a merged active task has `Status: RESOLVED` (e.g. verified as resolved on product main without product code changes), `score2gp_dispatch.py` / `score2gp_got_bootstrap.py` currently emits `PROMOTE_MERGED_TASK`, which falsely implies an ordinary code PR merge.

## Goal

- Emit `PROMOTE_RESOLVED_TASK` when the merged active task has `Status: RESOLVED`.
- Retain `PROMOTE_MERGED_TASK` for ordinary completed tasks.
- Update `AGENTS.md` and related governance docs/skills to recognize `PROMOTE_RESOLVED_TASK`.
- Add regression tests covering both `PROMOTE_RESOLVED_TASK` and `PROMOTE_MERGED_TASK` dispatch paths.

## Allowed Files

- `scripts/score2gp_got_bootstrap.py`
- `scripts/score2gp_go_bootstrap.py`
- `AGENTS.md`
- `.agents/skills/score2gp-project-director/SKILL.md`
- `CLAUDE.md`
- `projects/score2gp/prompts/next/go-dispatch.md`
- `projects/score2gp/prompts/next/got-dispatch.md`
- `tests/test_score2gp_got_bootstrap.py`
- `tests/test_dispatch_entrypoint_contract.py`
- `projects/score2gp/ACTIVE_TASK.md`

## Acceptance

1. When active task status is `RESOLVED` and PR is `MERGED`, `score2gp_dispatch.py` emits state `PROMOTE_RESOLVED_TASK`.
2. When active task status is `APPROVED` or other ordinary status and PR is `MERGED`, `score2gp_dispatch.py` emits `PROMOTE_MERGED_TASK`.
3. Governance tests pass cleanly. `AGENTS.md` documents `PROMOTE_RESOLVED_TASK`.
