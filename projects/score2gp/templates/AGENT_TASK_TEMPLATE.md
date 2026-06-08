# Agent Task Template

## Title

Short task name.

## Status

NO_ACTIVE_TASK_APPROVED

Use `APPROVED` only when the human maintainer has explicitly approved execution.
Valid statuses:
- `NO_ACTIVE_TASK_APPROVED`: Agents may inspect and report only.
- `APPROVED`: The task may start.
- `IN_PROGRESS`: Agents are working inside the approved task boundary.
- `PR_OPEN`: A task PR exists. Agents may continue review, fixes, tests, follow-up commits, and re-review on the same branch/PR.
- `CHANGES_REQUESTED`: Reviewer found issues. Developer may fix them on the same branch/PR without new human approval.
- `READY_FOR_HUMAN_MERGE`: Reviewer says acceptance criteria are met. Agents must stop before merge.
- `BLOCKED`: Human decision is required.
- `DONE`: Only after human merge or explicit human closure.

## Permission Tier

Tier 0 inspect only by default.

Allowed values:

- Tier 0: Inspect Only
- Tier 1: Local Research / Documentation Only
- Tier 2: Branch and PR Work

Tier 2 allows creating a branch, committing, pushing, and opening a PR. Merges and branch deletion remain strictly human-only.
    
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

## Context

What the agent needs to know.

## Current Verified State

Only facts verified from repository state, command output, or explicit human instruction.

## Goal

Concrete expected outcome.

## Non-goals

What must not be attempted.

## Forbidden Actions

Explicitly disallowed actions for this task (e.g., merging PRs, modifying certain files).

## Allowed Repositories

List allowed repositories.

## Allowed Branches

List allowed branches.

## Allowed Files

List files or paths the agent may inspect or edit.

## Constraints

Technical, security, privacy, architecture, branch, and style constraints.

## Required Pre-flight Checks

Commands or inspections required before changes.

## Implementation Guidance

Likely files, approach, and design notes.

## Validation

Tests, smoke checks, manual checks, or evidence required.

## Acceptance Criteria

Conditions for completion.

## Stop Conditions

When to stop and report instead of continuing.

## Reporting Format

Report:

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
