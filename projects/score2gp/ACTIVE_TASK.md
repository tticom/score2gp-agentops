# Active Task

Status: PR_OPEN
# Active Task

Status: NO_ACTIVE_TASK_APPROVED

No active task is currently approved.

The previous Tier 2 governance relaxation task was completed by human merge of PR #74.
Agents must stop after preflight and report proposed next action until a new task is explicitly approved here.

Current Permission Tier: Tier 2 branch and PR work.

## Permission Tier

Tier 2

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

## Current Verified State

The `ag-control-check` and wrapper scripts have already been verified to allow push to `human` remote.
The task queue and agent control documentation currently do not reflect full Tier 2 permission policies.

## Non-goals

Do not modify product implementation code.
Do not merge any PRs.
Do not delete branches.
Do not push directly to `main`.
Do not use `hgh`.
Do not start a product backlog task.
Do not mark unmerged work as merged.

## Forbidden Actions

- Do not modify product implementation code.
- Do not modify product `AGENTS.md`.
- Do not merge PRs.
- Do not approve PRs.
- Do not delete branches.
- Do not force-push.
- Do not use `hgh`.
- Do not start product backlog work.

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
```

## Implementation Guidance

Update `AGENT_CONTROL.md`, `AGENT_TASK_TEMPLATE.md`, and potentially `ACTIVE_TASK.md` to ensure they include all required role descriptions, Tier 2 definitions, permission models, and required task shape headers.

## Validation

- git diff --check
- git status --short
- confirm no product files changed
- inspect changed governance text and confirm it is self-sufficient

## Acceptance Criteria

All required governance components (roles, Tier 2 permissions, task shapes, status models) are explicitly defined. PR is open against main.

## Stop Conditions

Stop if any wrapper scripts strictly prohibit pushing to `human` without being able to be overridden, or if product code is required to be touched.

## Reporting Format

- commands run
- files changed
- tests/checks run
- validation results
- commit hash
- branch name
- PR link if opened
- known limitations
- what was not tested
- next recommended task
