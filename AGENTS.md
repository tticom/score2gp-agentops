# Score2GP executable command entrypoints

For any request to continue, advance, run the next command, `go`, `got`, or
`next`, execute this identity-aware router before any manual inspection:

```bash
python3 scripts/score2gp_dispatch.py --product ../score2gp --agentops . --json
```

For an explicit PR review request, including `review #N`, `hard review`, or
`real review`, route the named repository and PR instead of silently falling
back to the active task:

```bash
python3 scripts/score2gp_dispatch.py --product ../score2gp --agentops . --json \
  --review-repo <owner/repo> --review-pr <number> [--review-level <level>]
```

The Linux worker identity, not the command word, selects the role.
`tticom-automation` runs author `go`; `tticom-gov` and `tticom-codex` run
governance/reviewer `got` under their own isolated GitHub identities. Never
bypass the router by calling the other role's helper. Treat its JSON as
authoritative. Never replace it with direct GitHub queries
or a cached handback. `ADDRESS_CURRENT_PR_REVIEW` means execute
`projects/score2gp/prompts/next/address-current-pr-review.md` with the returned
formal review ID, commit ID, and body. Fail closed if the helper fails.
Only `EXECUTE_PROMPT` and `ADDRESS_CURRENT_PR_REVIEW` authorize task actions.
For `MERGED_AWAITING_GOVERNANCE_PROMOTION`, report the state and stop without
rerunning, re-verifying, or summarizing the completed task. Also report the
returned `next_action`: governance must run `got`, which dispatches
`PROMOTE_MERGED_TASK` or `PROMOTE_RESOLVED_TASK`. Treat every other unrecognized or non-action state as
terminal.

Read `AGENT-RULES.md` for the remaining repository rules.

For governance/review, treat the routed JSON as authoritative and never resume
a cached managed task. `REVIEW_CURRENT_HEAD` authorizes and requires a formal
review in the returned `review_worktree`. Require
`review_local_head == pr.headRefOid`, invoke the returned `review_skill` from
the exact returned `review_skill_path`, and apply the Score2GP project overlay.
A stricter review may be chosen; a weaker review may not. For an AgentOps lock
upgrade, `review_skills_mode=proposed-pin-isolated` means the proposed merged
skills pin is used by immutable path for this review only; never relink the
active installation before the AgentOps PR merges.

`REVIEW_PUBLICATION_INCOMPLETE` means a formal agent review exists but its
required exact-level, exact-head marked summary does not. Reconcile that review
metadata and prove it by GitHub read-back; do not rerun tests or invent a new
verdict.

Reviewer mode is metadata-only: formal review, inline review comments, and one
mandatory marked PR summary comment. Do not edit any repository file, branch,
commit, PR body, task status, prompt, report, or evidence artifact. Publish
through the exact immutable `review_publisher_path` returned alongside
`review_skill_path`; never substitute the installed `$HOME/.agents` copy. A
chat-only or status-only response is a dispatcher failure.

`tticom-automation` and `tticom-gov` never merge. `tticom-codex` may merge only
in a separate operation after a current explicit instruction from `tticom`
naming the exact repository, PR number, and reviewed full head SHA.
This `got` state is separate from the action-authorizing states for `go`.
`PROMOTE_MERGED_TASK` authorizes and requires verifying the merge on remote
main, synchronizing product and governance mains, rereading `ACTIVE_TASK.md`,
and preparing the smallest bounded governance promotion. A status-only
response in this state is a dispatcher failure.
`PROMOTE_RESOLVED_TASK` authorizes and requires verifying the governance resolution on remote main, synchronizing product and governance mains, rereading `ACTIVE_TASK.md`, and preparing the smallest bounded governance promotion for resolved tasks without product code changes. A status-only response in this state is a dispatcher failure.
