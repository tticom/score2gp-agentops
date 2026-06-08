# Active Task

Status: APPROVED

Current Permission Tier: Tier 2 branch and PR work.

## Title

Relax Agent Control Gate to Allow Branch and PR Workflow

## Context

The current control gate is too restrictive. It correctly prevents uncontrolled merges, but it also blocks useful agent work such as creating branches, committing, pushing task branches, opening PRs, running reviewer/developer loops, and updating task status.

The intended operating model is:

- agents may produce reviewable PRs
- agents may run architect/developer/reviewer loops for an approved task
- agents may update task records for the approved task
- human maintainer controls all merges to `main`

## Goal

Update the governance model so agents can perform approved branch-and-PR work while preserving human control over merges to `main`.

## Non-goals

Do not modify product implementation code.
Do not merge any PRs.
Do not delete branches.
Do not push directly to `main`.
Do not use `hgh`.
Do not start a product backlog task.
Do not mark unmerged work as merged.

## Allowed Repositories

- `/home/tticom/work/score2gp-workspace/score2gp-agentops`
- `/home/tticom/work/score2gp-workspace/score2gp`

## Allowed Files

Governance repo:

- `projects/score2gp/AGENT_CONTROL.md`
- `projects/score2gp/ACTIVE_TASK.md`
- `projects/score2gp/TASKS.md`
- `projects/score2gp/templates/AGENT_TASK_TEMPLATE.md`
- any new review note under `projects/score2gp/reviews/` if needed

Product repo:

- `AGENTS.md`

## Required Pre-flight Checks

Run from the governance repo first:

```bash
~/agent-control/bin/ag-control-check
git status --short
git branch --show-current
git fetch --all --prune
git log --oneline --decorate --max-count=20