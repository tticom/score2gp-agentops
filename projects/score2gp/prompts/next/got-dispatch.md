# Codex `got` Dispatcher

Turn `got` into the next authorised reviewer/governor action from Agy's
durable PR handback and exact live GitHub state.

## Gate

Prove one complete, non-mixed reviewer profile:

- Linux `tticom-gov`, GitHub/Git `tticomgov-code`, workspace
  `/home/tticom-gov/work/score2gp-workspace`; or
- Linux `tticom-codex`, GitHub/Git `tticom-codex`, workspace
  `/home/tticom-codex/work/score2gp-workspace`.

Cross-profile credentials or paths fail closed. Read
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
  Before approval, execute a reviewer-created counterexample absent from the
  PR tests. Timing, grouping, aggregation, fallback, capacity, and fail-closed
  changes require disagreement plus order/partition/boundary challenges.
  On revised heads, rerun the original probe and add a second-order probe.
  Maintain a cumulative counterexample registry: every earlier finding must
  map to a freshly executed reviewer-owned probe on the current exact head.
  A test changed by the author in the PR scores zero as reviewer-created
  evidence, even if the reviewer executes it. For each remediation, record a
  delta threat model covering changed symbols, the fix assumption, new
  branches or thresholds, and adjacent false-positive/false-negative risks.
  Challenge zero/one/many cardinality, both sides of every new threshold, the
  closest value that must remain distinct, and the nearest representation that
  must remain rejected. If the remediation changes a test oracle, require a
  product contract or domain-authority citation; author intent is insufficient.
  Apply claim-to-oracle closure: every `verified` claim must cite the exact
  final-artifact assertion for the same required or forbidden value and a
  negative control killed by that oracle. Exercising a related path or checking
  adjacent symptoms is not verification. A claim/oracle scope mismatch requires
  changes.
- Current-head review requests changes: report `AWAITING_AGY_FIXES`.
- Current-head review approves: verify checks and threads, report
  `READY_FOR_HUMAN_MERGE`, and stop. Never merge.
- Merged PR: emit actionable state `PROMOTE_MERGED_TASK` (or `PROMOTE_RESOLVED_TASK` when active task status is RESOLVED), verify the merge on
  remote main, synchronize the Codex clone, reread `ACTIVE_TASK.md`, and
  prepare the smallest governance promotion. A status-only response is a
  dispatcher failure. Never promote a report candidate directly into product
  implementation.
- Closed unmerged PR: report `BLOCKED`.

Every approval includes the disconfirmation record and the three equal full
head SHAs. After review, publish the
verdict on the exact head with the guarded publisher:

```bash
python3 scripts/score2gp_publish_review.py \
  --repo <Repository> \
  --pr <PR number> \
  --head <reviewed full head SHA> \
  --verdict "<needs changes|APPROVED>" \
  --body-file <formal review markdown> \
  --evidence-file <review-evidence.json> \
  [--high-risk]
```

The publisher normalizes `needs changes` to GitHub `CHANGES_REQUESTED`, pins
the review to the exact head, and re-queries the formal review before
returning one machine-actionable state:
`AWAITING_AGY_FIXES`, `READY_FOR_HUMAN_MERGE`,
`AWAITING_AGY_HANDBACK`, or `BLOCKED`.
Do not return a chat-only verdict. A publisher failure is a hard stop.
The publisher rejects approvals whose review body lacks populated executable
adversarial-evidence fields; green CI and author tests are not substitutes.
For approval, it also reads `projects/score2gp/REVIEWER_SCORECARD.json` and
requires a machine-validated evidence packet. Active reviewer strikes increase
the probe quota. Omit `--evidence-file` for a changes-requested verdict.
Repeated `got` with unchanged remote inputs creates no new task or duplicate
review.
