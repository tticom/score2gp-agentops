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
4. Relevant task template(s) under `projects/score2gp/templates/`

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

Agents may create a task branch, modify files allowed by `ACTIVE_TASK.md`, run tests, commit, push the task branch to the human remote, and open a PR.

**Human approval is for the task boundary, not role transitions.**
An approved `ACTIVE_TASK.md` authorizes the full lifecycle of that task:
* research
* architecture
* development
* review
* reviewer-requested fixes
* testing
* re-review
* evidence recording
* pushing follow-up commits to the same branch
* updating the same PR

No extra human approval is needed to move from Architect to Developer to Reviewer as long as the work stays inside the approved task boundary.

**One task should normally produce one PR.**
The default model is:
* one approved task
* one task branch
* one PR in the repository that owns the durable output
* many review/fix/re-review cycles on that same branch and PR

Do not create separate PRs for Architect, Developer, and Reviewer phases.

**Governance PRs are only for governance.**
A governance PR is appropriate when changing:
* `ACTIVE_TASK.md`
* task templates
* control policy
* orchestration notes
* review records
* evidence/handoff records

A governance PR is not the right place for durable product design knowledge.
Durable product architecture, parser design, diagnostics design, fixture plans, test plans, implementation notes, scripts, generated public fixtures, and product documentation belong in `score2gp`.

Agents may update task-tracking files only for the approved task, and only to reflect accurate state.

A task must not be marked `DONE` until the human has actually merged the PR and it has been verified on main.

## Status Model

Statuses must strictly distinguish:

- `NO_ACTIVE_TASK_APPROVED`: Agents may inspect and report only.
- `APPROVED`: The task may start.
- `IN_PROGRESS`: Agents are working inside the approved task boundary.
- `PR_OPEN`: A task PR exists. Agents may continue review, fixes, tests, follow-up commits, and re-review on the same branch/PR.
- `CHANGES_REQUESTED`: Reviewer found issues. Developer may fix them on the same branch/PR without new human approval.
- `READY_FOR_HUMAN_MERGE`: Reviewer says acceptance criteria are met. Agents must stop before merge.
- `BLOCKED`: Human decision is required.
- `DONE`: Only after human merge or explicit human closure.

## Task Scope and Exploration

**Tasks should be meaningful, not microscopic.**
Avoid process theatre. A task may include multiple cycles of research, development, and review if that is what is needed to reach a useful outcome.

A task is valid if either:
* the expected outcome is well-defined, with acceptance criteria, or
* it is explicitly a research task, where the output is evidence, constraints, options, risks, and a recommended next step

For research tasks, the result does not have to be predetermined. The point is to discover reality safely and report it clearly.

**Branches make exploration safe, but not uncontrolled.**
It is acceptable to explore, test, refine, or discard work on a task branch. However, the branch does not remove the task boundary. Agents must still stop if:
* the work exceeds approved scope
* private/copyrighted/sensitive material would be exposed
* allowed files or repositories need expansion
* destructive commands are required
* tests fail and the cause is unclear
* the task needs a human architectural/product decision
* merge is required
* force-push or branch deletion would be needed

## Role Boundaries

Agents operate under the following role boundaries during team operation:

- **Orchestrator**: identifies active blocker, sequences approved work, reports state.
- **Architect**: defines requirements, assumptions, acceptance criteria, risks.
- **Developer**: implements smallest useful approved change.
- **Reviewer**: reviews code/docs/process/evidence and comments, but does not merge or self-approve.
- **Researcher**: investigates uncertainty and records evidence without changing product implementation unless approved.

### Forbidden Actions

Agents must not merge PRs, push directly to main, force-push, delete branches, run `gh pr merge`, run commands containing `--delete-branch`, use the `hgh` CLI alias, approve their own PR, bypass failing checks, start unrelated backlog work, expand scope without human approval, or mark unmerged work as merged/done.

### Human-Only Operations

Only the human maintainer may merge PRs, approve scope expansion, approve movement to a different task, close or abandon task PRs, accept a known failing-check risk, or explicitly close a task without merge.

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

## Validation Permission

Within an approved task, agents are authorized to run and re-run relevant non-destructive validation commands inside the task boundary without per-test human approval. This includes targeted pytest tests, the full pytest suite, diff checks, schema checks, and fixture-generation smoke checks when relevant to the task.

Human approval is only needed if validation would:
- exceed the approved task boundary
- require destructive commands
- use private/copyrighted/sensitive data
- create large generated artifacts
- need unexpected network access
- alter dependencies/environment configuration
- modify files outside the allowed scope

## Stop Conditions

Agents must stop and report if:

- `ACTIVE_TASK.md` says `NO_ACTIVE_TASK_APPROVED`
- required preflight checks fail
- the current branch is unexpected
- the working tree contains unrelated changes
- a requested action would merge or delete a branch, or perform an unauthorized push/PR
- a requested action would touch private or generated artifacts
- requirements conflict with repository evidence
- tests fail and the failure is not clearly in scope
- the task would require implementing a deferred capability
- the next step requires human approval
