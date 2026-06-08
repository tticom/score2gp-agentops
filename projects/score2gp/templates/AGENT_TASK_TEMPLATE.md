# Agent Task Template

## Title

Short task name.

## Status

NOT_APPROVED

Use `APPROVED` only when the human maintainer has explicitly approved execution.

## Permission Tier

Tier 0 inspect only by default.

Allowed values:

- Tier 0 inspect only
- Tier 1 local edits only
- Tier 2 local commit
- Tier 3 push/open PR
- Tier 4 merge/delete branch

Tier 3 and Tier 4 are human-only unless a future policy explicitly changes this.

## Context

What the agent needs to know.

## Current Verified State

Only facts verified from repository state, command output, or explicit human instruction.

## Goal

Concrete expected outcome.

## Non-goals

What must not be attempted.

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

- branch
- files changed
- commands run
- validation results
- commit hash, if human-approved
- PR link, if human-created
- limitations
- next recommended task
