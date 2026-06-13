# Post-Task 114: Agent PR Readiness Workflow

Date: 2026-06-13
Authorised by: Governance Task 114

## Context
Repeated delays in the `score2gp` agentic workflow were caused by agents reporting PRs as “ready” before Codex comments or review threads appeared and were explicitly dispositioned. This led to process failures where minor product fixes were slowed down by disconnected review loops.

## Decision
We have introduced a strict Agent PR Readiness workflow to ensure agents verify the PR review surface properly and only report “ready” after CI and Codex/comment checks have settled.

The durable instructions have been recorded in:
- `projects/score2gp/AGENT_PR_READINESS.md`
- Referenced in `projects/score2gp/AGENT_CONTROL.md`

## Rule Summary
1. **Readiness Statuses**: Agents must explicitly classify readiness as `READY`, `NOT READY`, `NEEDS SUPERVISOR DECISION`, or `NEEDS CHANGES`.
2. **Codex Disposition**: Every Codex comment must be dispositioned (accepted as blocker, accepted as non-blocking, already fixed, rejected with reason).
3. **Regression Tests**: Plausible correctness bugs identified by Codex require regression tests.
4. **Evidence Block**: All reports must include a standard PR readiness evidence block.
5. **Open vs. Complete**: Opening a PR is not completion. Agents must wait for checks and address blockers before reporting ready.
6. **Fast-Lane Rule**: Fast-lane reviews are reserved for tiny corrective PRs.
7. **Role Responsibilities**: Clear delineation between product agents, governance agents, and reviewers regarding PR inspection and validation.

## Authorised Next Task
Product Task 113 (Shared whole-note candidate evidence shaping for diagnostics and recognition) may now proceed, following this updated readiness workflow.
