# Active Task

Status: PR_OPEN

Current Permission Tier: Tier 2 branch and PR work.

## Title

Governance: End-to-End Task PR Workflow

## Context

We have identified a control-flow problem in the score2gp-agentops governance model. The previous model was too phase-oriented, making agents seek separate approval to move between Architect, Developer, and Reviewer roles, and encouraging multiple PRs per task.
The intended model is: One approved task = one task branch = one task PR = many allowed cycles of research, architecture, development, review, fixes, testing, and re-review inside the same approved task boundary.
Durable product knowledge (fixtures, architecture, tests) belongs in the product repo, whereas the governance repo tracks active tasks and policy. The previous task PRs (#79, #80) mixed these concerns and are abandoned/superseded by this policy correction.

## Current Verified State

* Product PR #197 exists separately in `score2gp` for the fixture expansion plan.
* Governance PR #79 is abandoned.
* Governance PR #80 is superseded.
* We are on the `governance/end-to-end-task-pr-flow-v0.1` branch for this correction.

## Goal

Correct the governance process model in `AGENT_CONTROL.md` and templates to explicitly state that an approved task authorizes the full lifecycle (one task, one branch, one PR), and that human approval is for the task boundary, not role handoffs.

## Non-goals

* Do not modify the product repo.
* Do not modify product PR #197.
* Do not implement fixture scripts or tests.
* Do not preserve PR #80 unchanged.

## Forbidden Actions

* Modifying product code or product repo documentation.
* Pushing directly to `main`.
* Creating product research files in `score2gp-agentops`.
* Merging any PR.
* Approving your own PR.

## Allowed Repositories

Governance repo: `/home/tticom/work/score2gp-workspace/score2gp-agentops`

## Allowed Branches

`governance/end-to-end-task-pr-flow-v0.1`

## Allowed Files

Governance repo:
* `projects/score2gp/AGENT_CONTROL.md`
* `projects/score2gp/ACTIVE_TASK.md`
* `projects/score2gp/templates/AGENT_TASK_TEMPLATE.md`

## Constraints

* The policy updates must clarify the status models, the one-task-one-PR flow, and the distinction between governance tracking and product architecture.

## Required Pre-flight Checks

* Ensure starting from governance `main`.

## Implementation Guidance

* Updated `AGENT_CONTROL.md` with explicit sections on "Human approval is for the task boundary", "One task should normally produce one PR", and updated status definitions.
* Updated `AGENT_TASK_TEMPLATE.md` to reflect the new expected statuses and PR flow.

## Validation

* Run `git diff --check`, `git status --short`, `git diff --stat` to ensure only governance files are touched.

## Acceptance Criteria

* `AGENT_CONTROL.md`, `AGENT_TASK_TEMPLATE.md`, and `ACTIVE_TASK.md` are updated.
* A governance PR is opened defining the end-to-end task PR workflow.

## Stop Conditions

* Blocked on human review.

## Reporting Format

Report branch name, files changed, commands run, new PR link, and next recommended task.
