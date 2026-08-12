# Score2GP executable command entrypoints

For any request to continue, advance, run the next command, `go`, `got`, or
`next`, the first task action must be:

```bash
python3 scripts/score2gp_dispatch.py --product ../score2gp --agentops . --json
```

For an explicit PR review request, route the exact repository and number:

```bash
python3 scripts/score2gp_dispatch.py --product ../score2gp --agentops . --json \
  --review-repo <owner/repo> --review-pr <number> [--review-level <level>]
```

Never substitute the active-task PR when the user named another PR.

Run it from the `score2gp-agentops` repository root. The Linux worker identity
selects the role: `tticom-automation` routes to author `go`; `tticom-gov` and
`tticom-codex` route to governance/reviewer `got` under their own isolated
GitHub identities. Never invoke the
other role's helper based only on the user's command word. Its JSON `state` and
`current_review` are authoritative. Do not query GitHub manually, reuse a
previous handback summary, or reconstruct the state in prose.

- `ADDRESS_CURRENT_PR_REVIEW`: immediately execute
  `projects/score2gp/prompts/next/address-current-pr-review.md` using
  `current_review.id`, `current_review.commit_id`, and `current_review.body`.
- `PUBLISH_AGY_HANDBACK`: reconstruct, publish, and read back the author
  handback receipt for the exact live head, then report `AWAITING_GOVERNANCE_REVIEW`.
- `AWAITING_GOVERNANCE_REVIEW` or `READY_FOR_HUMAN_MERGE`: report and stop.
- `MERGED_AWAITING_GOVERNANCE_PROMOTION`: report and stop. Do not rerun,
  re-verify, summarize, or otherwise continue the completed product task.
  Report the returned `next_action` directing governance to run `got`.
- `EXECUTE_PROMPT`, `ADDRESS_CURRENT_PR_REVIEW`, and `PUBLISH_AGY_HANDBACK` are the only states that
  authorize task actions. Every other state is terminal: report it and stop.
- Any helper failure or missing field: fail closed and report the exact error.

Repeated commands with unchanged JSON are idempotent. Do not create another
task, review, or handback.

For governance/review, the routed JSON is authoritative. Never resume or replay
a prior managed task.
- `REVIEW_CURRENT_HEAD`: use the returned `review_worktree`, prove
  `review_local_head == pr.headRefOid`, invoke the returned `review_skill` from
  the exact `review_skill_path`, apply the Score2GP overlay, and publish the
  exact-head formal verdict, useful inline findings, and mandatory marked PR summary comment.
  `proposed-pin-isolated` uses a proposed merged skills pin by
  immutable path without changing installed skill links.
  Publish only through the returned `review_publisher_path`; never substitute
  the installed `$HOME/.agents` publisher.
  Reviewer mode may mutate review metadata only; it must not modify repository
  content, refs, branches, commits, PR bodies, prompts, reports, or task state.
  A status-only or chat-only response is a dispatcher failure.
- `REVIEW_PUBLICATION_INCOMPLETE`: reconcile the missing marked summary for the
  existing exact-head formal review, verify it remotely, and stop. Do not rerun
  the review or create a replacement verdict.
- `READY_FOR_HUMAN_MERGE`: report and stop.
- `AWAITING_AGY_FIXES`: report the current exact-head findings and stop.
- `PROMOTE_MERGED_TASK` / `PROMOTE_RESOLVED_TASK`: verify merged main and prepare the next governance
  promotion. A status-only response is a dispatcher failure; historical
  reviews must not override `MERGED`.

`tticom-automation` and `tticom-gov` never merge. `tticom-codex` may merge only
after a separate current explicit instruction from `tticom` naming the exact
repository, PR number, and reviewed full head SHA.

Read `AGENT-RULES.md` and the selected role skill for all other work.
