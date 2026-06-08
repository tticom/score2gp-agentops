# Process-Flow Correction Record

**Date**: 2026-06-08
**Task**: Governance: End-to-End Task PR Workflow

## Overview
This record captures the governance correction applied to resolve the phase-oriented PR generation issue observed during task execution.

## Motivation
Agents were generating separate PRs for role transitions (Architect, Developer, Reviewer) and were putting durable product research (e.g. fixture planning) into governance PRs instead of the product repository.

## Actions Taken
1. **AGENT_CONTROL.md**:
   - Clarified that human approval applies to the task boundary, not role handoffs.
   - Enforced the "One approved task = one task branch = one PR" rule.
   - Explicitly restricted durable product architecture to the `score2gp` product repository.
   - Clarified the status enum and rules around exploring within a branch.

2. **AGENT_TASK_TEMPLATE.md**:
   - Added precise definitions for all valid task statuses.
   - Removed ambiguity around the `APPROVED` status versus role handoffs.

3. **ACTIVE_TASK.md**:
   - Updated the task tracker to reflect this governance process-flow correction as the single active effort, replacing the previous fragmented fixture research tasks on the governance side.

## Impact
This correction ensures that all future task executions operate under a unified lifecycle branch, eliminating "process theatre" and keeping product knowledge properly located in the product repository.

After this PR is merged, ACTIVE_TASK.md must be reset or advanced by a human-approved follow-up so main does not indefinitely show this governance correction as PR_OPEN.
