# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REC-00A — Agent Workspace Cleanup Skill

**Status**: MERGED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `codex/prepare-rec02-and-workspace-cleanup`

**Pull Request**: 609

**Owner Role**: architect

## Objective

Define and add a reusable cleanup skill for agent environments that safely identifies stale worktrees, prunable metadata, generated artifacts, and untracked files across the three agent identities without deleting active or uncommitted work.

## Allowed paths

- `projects/score2gp/prompts/next/rec-00a-agent-workspace-cleanup.md`
- `projects/score2gp/tasks/2026-08-30-agent-workspace-cleanup-skill.md`

## Validation commands

- `python3 scripts/score2gp_governance_audit.py`
- `git diff --check`
- `dry-run inventory against all three agent environments`
