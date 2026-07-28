# Codex `got` Dispatcher

Turn `got` into the next authorised reviewer/governor action from Agy's
durable PR handback and exact live GitHub state.

## Gate

Prove `tticom-codex` identity and canonical WSL workspace. Read
`AGENT_CONTROL.md`, `ACTIVE_TASK.md`, the Reviewer skill, `REVIEW_RULES.md`,
`PR_REVIEW_TEMPLATE.md`, and `PR_EVIDENCE_CONTRACT.md`. Require stable `Task`,
`Status`, `Assigned Identity`, `Repository`, `PR Branch`, and
`Original Prompt` fields.

Run `scripts/score2gp_control_plane.py` before dispatch. It must:

- fetch AgentOps and product remotes;
- switch clean canonical clones to `main` and fast-forward with `--ff-only`;
- reread authority only after AgentOps local `main == origin/main`;
- fetch `agy-skills` without switching it to latest main and verify the
  immutable checkout exactly equals the full commit in `SKILLS_LOCK.md`,
  materializing and atomically activating that exact pin when the merged lock
  changes;
- when a live PR exists, fetch its full `headRefOid` and materialize that exact
  commit detached or in a dedicated review worktree.

Before diffing, require local review `HEAD == live headRefOid`. Diff the base
object ID against that exact object ID, not against an unrelated local
`HEAD`. Re-query GitHub immediately before publishing and require:

`initial live head == reviewed local HEAD == final live head`.

Any mismatch discards the verdict and restarts review at the new head.
Arbitrary task-branch pulls, merges, resets, and silent adoption of newer
skills are prohibited.

## Dispatch

Query the configured repository for the PR whose head is exactly `PR Branch`.
Never choose by recency.

Use the same `scripts/score2gp_pr_review_state.py` resolver as `go`. A verdict
is durable only after a formal review exists on GitHub for the exact head;
local task state, chat, and issue comments do not count.

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

Every approval includes the disconfirmation record and the three equal full
head SHAs. After review, publish the
verdict on the exact head and one machine-actionable state:
`AWAITING_AGY_FIXES`, `READY_FOR_HUMAN_MERGE`,
`AWAITING_AGY_HANDBACK`, or `BLOCKED`.
Re-query formal reviews after publication and prove the expected review ID,
reviewer, commit ID, state, and timestamp exist before reporting the state.
Repeated `got` with unchanged remote inputs creates no new task or duplicate
review.
