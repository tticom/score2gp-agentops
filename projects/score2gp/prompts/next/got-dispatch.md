# Codex `got` Dispatcher

Turn `got` into the next authorised reviewer/governor action from Agy's
durable PR handback and exact live GitHub state.

## Gate

Prove `tticom-codex` identity and canonical WSL workspace. Read
`AGENT_CONTROL.md`, `ACTIVE_TASK.md`, the Reviewer skill, `REVIEW_RULES.md`,
`PR_REVIEW_TEMPLATE.md`, and `PR_EVIDENCE_CONTRACT.md`. Require stable `Task`,
`Status`, `Assigned Identity`, `Repository`, `PR Branch`, and
`Original Prompt` fields. Fetch without destructive worktree operations.

## Dispatch

Query the configured repository for the PR whose head is exactly `PR Branch`.
Never choose by recency.

- No PR: continue only when the task is assigned to Codex; otherwise report
  `AWAITING_AGY_PUBLICATION`.
- No author handback comment pins the current head: report
  `AWAITING_AGY_HANDBACK`; never review a chat summary.
- New head with complete finding dispositions, or no current-head Codex
  review: run the pinned two-axis review and Score2GP hard-review overlay.
- Current-head review requests changes: report `AWAITING_AGY_FIXES`.
- Current-head review approves: verify checks and threads, report
  `READY_FOR_HUMAN_MERGE`, and stop. Never merge.
- Merged PR: verify the merge on remote main, synchronize the Codex clone,
  reread `ACTIVE_TASK.md`, and prepare the smallest governance promotion.
  Never promote a report candidate directly into product implementation.
- Closed unmerged PR: report `BLOCKED`.

Every approval includes the disconfirmation record. After review, publish the
verdict on the exact head and one machine-actionable state:
`AWAITING_AGY_FIXES`, `READY_FOR_HUMAN_MERGE`,
`AWAITING_AGY_HANDBACK`, or `BLOCKED`.
