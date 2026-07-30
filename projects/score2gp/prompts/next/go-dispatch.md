# Agy `go` Dispatcher

Turn `go` into the next authorised author-side action without copied chat
prose or a static pointer to a completed prompt.

## Gate & Bootstrap Protocol

Every `go` invocation MUST execute the executable dispatcher bootstrap helper:

```bash
python3 scripts/score2gp_go_bootstrap.py --product ../score2gp --agentops .
```

Before task dispatch, it must also run the shared control-plane gate against
the skills source repository. This gate fetches and fast-forwards only clean
canonical `main` branches, materializes the exact immutable skills pin, and
atomically activates the required skill links. It must never silently update
to `agy-skills/main`.

The helper enforces the required state transitions:
1. **Identity & Cleanliness**: Proves `tticom-automation` identity and verifies both repositories are clean before switching. Fails closed on dirty or unexpected state.
2. **Fetch Authoritative State**: Fetches `origin/main` in `score2gp-agentops` and reads `ACTIVE_TASK.md` from `origin/main` (`git show origin/main:projects/score2gp/ACTIVE_TASK.md`), ignoring stale working-tree task files.
3. **Synchronize AgentOps Canonical Branch**: Fast-forwards local AgentOps `main` (`git switch main && git merge --ff-only origin/main`) and verifies synchronized metadata matches `origin/main`.
4. **Synchronize Authorised Output Repository**: Reads `Repository` from the newly fetched task, switches to `main` in the declared repository, and fast-forwards to `origin/main`.
5. **Select Authorised Task Branch**: Reads `PR Branch` and creates or selects the exact authorised task branch from `origin/main`.
6. **Dispatch**: Emits machine-actionable state.

Report `AgentOps SHA`, `Product Main SHA`, and `Skills SHA` on every run.

## Dispatch

Query the configured repository for PRs whose head is exactly `PR Branch`.
Never select by recency.

Use `scripts/score2gp_pr_review_state.py` to query formal pull-request reviews.
Issue comments are author handbacks, not verdicts. On the exact live head, the
latest non-dismissed `tticom-codex` formal review by server timestamp then
review ID governs. A later `CHANGES_REQUESTED` supersedes an earlier
`APPROVED` on the same head.

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
  `MERGED_AWAITING_GOVERNANCE_PROMOTION` and direct the maintainer to Codex
  `got`, whose actionable state is `PROMOTE_MERGED_TASK`.
- Closed unmerged PR: report `BLOCKED`.

After author mutations, publish one PR comment with exact head, finding
dispositions, validation, remaining risks, and `AWAITING_CODEX_REVIEW`.
Repeated `go` with unchanged remote inputs returns the same state without
creating a new task or duplicate handback.
