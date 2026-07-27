# Agy `go` Dispatcher

Turn `go` into the next authorised author-side action without copied chat
prose or a static pointer to a completed prompt.

## Gate

Prove `tticom-automation` identity and canonical WSL workspace. Read
`AGENT_CONTROL.md`, `ACTIVE_TASK.md`, and the Developer skill. Require stable
`Task`, `Status`, `Assigned Identity`, `Repository`, `PR Branch`, and
`Original Prompt` fields. Stop when the assigned identity differs. Fetch
without destructive worktree operations.

## Dispatch

Query the configured repository for PRs whose head is exactly `PR Branch`.
Never select by recency.

- No PR: if status is `APPROVED` or `IN_PROGRESS`, execute `Original Prompt`;
  otherwise stop. A remote branch without one exact PR is unexplained state.
- Open PR with current-head `CHANGES_REQUESTED`: execute
  `address-current-pr-review.md` using the live review head and findings.
- Open PR with a newer author head: require a handback comment pinning that
  head and dispositioning every finding, then report
  `AWAITING_CODEX_REVIEW`.
- Open PR without a current-head review: verify the evidence contract and
  pinned handback, then report `AWAITING_CODEX_REVIEW`.
- Open PR with current-head `APPROVED`: report `READY_FOR_HUMAN_MERGE` and
  stop. Never merge.
- Conflicting checks, comments, reviews, or threads: report the exact conflict.
- Merged PR: verify the merge on remote main. Do not rerun `Original Prompt`,
  delete the branch, or start a candidate follow-up. Report
  `MERGED_AWAITING_GOVERNANCE_PROMOTION` for Codex `got`.
- Closed unmerged PR: report `BLOCKED`.

After author mutations, publish one PR comment with exact head, finding
dispositions, validation, remaining risks, and `AWAITING_CODEX_REVIEW`.
