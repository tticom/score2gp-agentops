# Score2GP Agent Control

This file is the governance control policy for agentic work on `score2gp`.

Agents must not treat task lists, backlog files, research notes, handoffs, or unchecked checklist items as permission to execute.

The only executable task source is:

`projects/score2gp/ACTIVE_TASK.md`

If `ACTIVE_TASK.md` says `NO_ACTIVE_TASK_APPROVED`, the agent must stop after preflight and report.

## Mandatory Startup Protocol

Agents must start from the governance repository:

`/home/tticom/work/score2gp-workspace/score2gp-agentops`

Before any work, run and report:

- `git status --short`
- `git branch --show-current`
- `git fetch --all --prune`
- `git log --oneline --decorate --max-count=5`

Agents must then read, in this order:

1. `projects/score2gp/AGENT_CONTROL.md`
2. `projects/score2gp/ACTIVE_TASK.md`
3. `projects/score2gp/TASKS.md`

If product work is involved, agents must also inspect the product repository:

`/home/tticom/work/score2gp-workspace/score2gp`

and read:

`AGENTS.md`

## Permission Tiers

### Tier 0: Inspect Only

Agents may inspect repositories, read files, run safe status/log commands, and report.  
Agents must not modify files, create branches, commit, push, create PRs, merge PRs, or update task status.

### Tier 1: Local Research / Documentation Only

Agents may create local documentation or research notes within the files allowed by `ACTIVE_TASK.md`.  
Agents may commit locally only if explicitly allowed by `ACTIVE_TASK.md`.  
Agents must not push, create PRs, merge PRs, or modify product code.

### Tier 2: Branch and PR Work

Agents may create a task branch, modify files allowed by `ACTIVE_TASK.md`, run tests, commit, push the task branch, and open a PR.

Agents may run an internal architect/developer/reviewer loop for the approved task. The reviewer may inspect the PR and request fixes. The developer may push follow-up commits to the same PR branch.

Agents may update task-tracking files only for the approved task, and only to reflect accurate state such as `IN_PROGRESS`, `PR_OPEN`, `NEEDS_HUMAN_REVIEW`, or `BLOCKED`.

Agents must not merge PRs, push directly to `main`, delete branches, force-push, bypass failing checks, start unrelated backlog tasks, or mark a task as merged before human merge.

### Human-Only Operations

Only the human maintainer may:

- merge PRs
- push directly to protected branches
- delete remote branches
- force-push
- run `gh pr merge`
- run commands containing `--delete-branch`
- use the `hgh` GitHub CLI alias
- approve movement from one backlog task to a different task unless that task is already explicitly listed in `ACTIVE_TASK.md`

## Deferred Product Boundaries

Unless explicitly approved by the human maintainer, agents must not implement or integrate:

- pitch inference
- clef handling
- notehead scanning or classification
- rhythm or duration extraction
- voice assignment
- bar-local timing grids
- ScoreIR event creation from geometry diagnostics
- scanned or OCR PDF support
- direct integration of geometry clusters into playback mapping

Geometry diagnostics remain diagnostic-only until separately approved.

## Stop Conditions

Agents must stop and report if:

- `ACTIVE_TASK.md` says `NO_ACTIVE_TASK_APPROVED`
- required preflight checks fail
- the current branch is unexpected
- the working tree contains unrelated changes
- a requested action would push, open a PR, merge, or delete a branch
- a requested action would touch private or generated artifacts
- requirements conflict with repository evidence
- tests fail and the failure is not clearly in scope
- the task would require implementing a deferred capability
- the next step requires human approval
