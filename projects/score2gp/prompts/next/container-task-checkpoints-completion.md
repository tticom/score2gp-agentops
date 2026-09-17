# Container task checkpoints: author completion prompt

## Author and authority

- Author identity: `tticom-codex`
- Repository: `tticom/score2gp-agentops`
- Branch: `codex/container-task-checkpoints`
- Starting head: `8ffeee55e9309aaf4a5070fee8d901c891dcd7db`
- Product task authority remains unchanged. Do not alter the active product task.

## Goal

Complete the container task-checkpoint runtime work already implemented on this
branch and publish one independently reviewable PR. The completion claim must
be based on real host/runtime evidence, not only substituted command tests.

## Required work

1. Rebase or otherwise reconcile this branch with current `main`, preserving
   the existing checkpoint implementation and its documented scope.
2. Run the focused runtime and Docker tests from a clean environment.
3. Exercise a real author cycle with the role-scoped GCP/GitHub credentials:
   successful checkpoint publication, rejected publication, validation failure,
   interruption/recovery, and reviewer no-write behavior.
4. Verify bootstrap behavior with dirty and ahead-of-main repositories, and
   verify that retained failed clones and checkpoint receipts are inspectable.
5. Record exact commands, SHAs, image IDs, statuses, and any unrun live gates
   in a durable handoff. Do not claim rollout completion if a live gate is
   unavailable.

## Scope boundary

Changes are limited to `agent-runtime/`, its focused tests, and the existing
AgentOps control/checkpoint documentation. Do not modify product source,
private fixtures, shared skills, or the active task authority.

## Delivery

Run `git diff --check` and the focused/full validation commands, commit the
result, push this non-protected branch, open or update one PR, and stop for an
independent review. Do not self-review, self-approve, merge, or promote a
follow-on task.
