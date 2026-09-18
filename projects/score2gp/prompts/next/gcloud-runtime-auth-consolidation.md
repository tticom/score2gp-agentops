# GCloud runtime authentication: author completion prompt

## Author and authority

- Author identity: `tticom-codex`
- Repository: `tticom/score2gp-agentops`
- Branch: `fix/gcloud-only-startup-auth`
- Starting head: `0f2fbb1c4f92b2070e23ee39aafcc88c7bef40a4`

## Goal

Consolidate the GCloud/Secret Manager and interactive-auth fixes into the
current AgentOps runtime direction, then deliver one bounded PR. This branch
must not be merged independently while the container-task-checkpoints branch
contains overlapping runtime changes.

## Required work

1. Compare this branch with current `main` and
   `codex/container-task-checkpoints`; identify which authentication,
   diagnostics, token-normalization, timeout, and validation-failure changes
   are still missing from the chosen final implementation.
2. Rebase the chosen implementation onto current `main`, preserving only
   non-duplicated, tested behavior.
3. Add focused regression tests for dispatch stderr/reason propagation,
   whitespace-normalized secrets, interactive versus unattended stdin, and
   validation failure preventing completion/checkpoint publication.
4. Run the full AgentOps runtime test suite plus `git diff --check`.
5. If live GCloud or GitHub credentials are unavailable, record that as an
   explicit unproven gate rather than replacing it with a mock claim.

## Scope boundary

Limit changes to `agent-runtime/`, focused tests, and directly related runtime
documentation. Do not alter product code, private fixtures, or active-task
authority. Do not maintain two competing runtime-auth PRs.

## Delivery

Push the consolidated non-protected branch, open one PR against `main`, attach
an exact-head handoff with validation evidence, and stop for independent
review. Do not self-review, self-approve, merge, or delete the source branch
until the replacement PR is accepted.
