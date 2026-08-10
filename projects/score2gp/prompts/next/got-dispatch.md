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

When the maintainer names a PR, invoke the router with `--review-repo` and
`--review-pr`; pass `--review-level devils-advocate` for `real review` or
`devil's advocate review`. The explicit target overrides active-task PR
selection for review metadata only. Never guess that a same-numbered PR belongs
to the other Score2GP repository.

Query the configured repository for the PR whose head is exactly `PR Branch`.
Never choose by recency.

Use the same `scripts/score2gp_pr_review_state.py` resolver as `go`. A verdict
is durable only after a formal review exists on GitHub for the exact head;
local task state, chat, and issue comments do not count.

- No PR: continue only when the task is assigned to Codex; otherwise report
  `AWAITING_AGY_PUBLICATION`.
- No author handback comment pins the current head: report
  `AWAITING_AGY_HANDBACK`; never review a chat summary.
- A marked author handback exists but does not pin the current head: report
  `INVALID_OR_STALE_AGY_HANDBACK` with the expected live head, observed
  handback heads, rejected comment ID/URL, and the instruction for the author
  to publish a corrected exact-head handback. Do not collapse this state into
  `AWAITING_AGY_HANDBACK` or review the stale handback.
- New head with complete finding dispositions, or no current-head trusted
  review: require `review_local_head == pr.headRefOid`, work only in the
  returned detached `review_worktree`, and invoke `review_skill` from the exact
  returned `review_skill_path`. For a lock-changing AgentOps PR, use the
  proposed pin only when it is already contained in `agy-skills/origin/main`;
  materialize it immutably as `proposed-pin-isolated` and never activate or
  relink it before the AgentOps PR merges. The dispatcher selects the minimum
  review level from live
  changed paths, active authority, risk markers, and earlier-head reviews:
  - `code-review` / BASIC only for genuinely low-risk documentation;
  - `hard-review` for code, tests, fixtures, executable scripts, domain data,
    generated artifacts, or empirical claims;
  - `devils-advocate-review` for AgentOps/control-plane changes,
    architecture/research, conversion correctness, or any re-review after a
    trusted review on an earlier head.
  A task declaration or current maintainer request may escalate this level but
  may never weaken it. `real review` means `devils-advocate-review`.
  The dispatcher also returns `review_publisher_path` from the same immutable
  checkout as `review_skill_path`. Never substitute a mutable or installed
  publisher path.
- Read the selected pinned skill completely and then apply Score2GP's project
  overlay. BASIC performs exact-head code sanity and contract checks. HARD also
  classifies every material test as real-source, extracted-real-source,
  synthetic/mocked, or data-free and rejects synthetic/data-free evidence for
  domain acceptance. DEVILS_ADVOCATE assumes every developer and prior-reviewer
  assertion is wrong and attempts to disprove it independently.
- Before approval, execute the selected skill's reviewer-created counterexample probes outside
  the repository. Timing, grouping, aggregation, fallback, capacity,
  fail-closed, parser, conversion, and privacy claims require the stricter
  devil's-advocate quota and production-path evidence.
  green CI and author tests are not substitutes.
- On revised heads, rerun the original counterexample and attack the repair.
  Maintain a cumulative contradiction ledger: every earlier finding and
  approval claim must map to a freshly executed reviewer-owned probe on the
  current exact head. An author test never becomes reviewer-created evidence.
- Apply claim-to-oracle closure: every `verified` claim must cite the exact
  final-artifact assertion for the same required or forbidden value and a
  negative control killed by that oracle. A claim/oracle scope mismatch
  requires changes.
- Reviewer mode may mutate review metadata only. It must leave both the review
  worktree and repository refs unchanged and clean. Never edit code, tests,
  prompts, reports, tasks, PR bodies, commits, or branches while reviewing.
- Current-head review requests changes: report `AWAITING_AGY_FIXES`.
- Current-head review approves: verify checks and threads, report
  `READY_FOR_HUMAN_MERGE`, and stop. Never merge.
- Formal agent review without the exact selected-level marked summary: report
  `REVIEW_PUBLICATION_INCOMPLETE`. Publish or repair only that missing review
  metadata, re-query GitHub, and stop; do not rerun the review, change the
  verdict, or claim completion from a local transcript.
- Merged PR: emit actionable state `PROMOTE_MERGED_TASK` (or `PROMOTE_RESOLVED_TASK` when active task status is RESOLVED), verify the merge on
  remote main, synchronize the Codex clone, reread `ACTIVE_TASK.md`, and
  prepare the smallest governance promotion. A status-only response is a
  dispatcher failure. Never promote a report candidate directly into product
  implementation.
- Merged PR with `ACTIVE_TASK.md` already at `Status: MERGED`: report
  `NO_ACTIVE_TASK` and stop. The completion promotion is already durable;
  never create a duplicate promotion. A new task requires a separate explicit
  governance promotion.
- Closed unmerged PR: report `BLOCKED`.

Every review includes the three equal full head SHAs. HARD and
DEVILS_ADVOCATE reviews also include the required disconfirmation record,
provenance ledger, fixture-coupling result, and external evidence packet.
Publish through the pinned shared guarded publisher:

```bash
python3 "<review_publisher_path>" \
  --repo <Repository> \
  --pr <PR number> \
  --expected-head <reviewed full head SHA> \
  --level <basic|hard|devils-advocate> \
  --verdict <APPROVE|CHANGES_REQUESTED|CANNOT_VERIFY> \
  --review-body-file <external-formal-review.md> \
  --summary-file <external-pr-summary.md> \
  [--inline-comments-file <external-inline-comments.json>] \
  [--packet <external-evidence.json>] \
  [--prior-packet <external-prior-evidence.json>] \
  [--prior-overturns <count>]
```

The publisher pins the formal review and inline comments to the exact head and
always creates or updates one marked PR issue comment containing review level,
head, base, verdict, findings, validation, and residual risk. It re-queries the
head after publication and fails closed on movement or proof mismatch.

Do not substitute a chat verdict, committed report, task-state edit, or PR-body
rewrite for review metadata. A publisher failure is a hard stop. Re-query and
prove the formal review, any inline findings, and mandatory summary comment
exist on the exact head. Finally prove the review worktree is still clean.
`tticom-gov` and `tticom-automation` never merge. `tticom-codex` requires a
separate current exact-PR maintainer instruction before any merge operation.

Repeated `got` with unchanged remote inputs creates no new task or duplicate
review.
