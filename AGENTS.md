# Score2GP executable command entrypoints

For any request to continue, advance, run the next command, `go`, `got`, or
`next`, execute this identity-aware router before any manual inspection:

```bash
python3 scripts/score2gp_dispatch.py --product ../score2gp --agentops . --json
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
`review_local_head == pr.headRefOid`, invoke exactly the returned
`review_skill`, and apply the Score2GP project overlay. A stricter review may
be chosen; a weaker review may not.

Reviewer mode is metadata-only: formal review, inline review comments, and one
mandatory marked PR summary comment. Do not edit any repository file, branch,
commit, PR body, task status, prompt, report, or evidence artifact. Publish
through the pinned `code-review/scripts/publish_review.py`; a chat-only or
status-only response is a dispatcher failure.

`tticom-automation` and `tticom-gov` never merge. `tticom-codex` may merge only
in a separate operation after a current explicit instruction from `tticom`
naming the exact repository, PR number, and reviewed full head SHA.
This `got` state is separate from the action-authorizing states for `go`.
`PROMOTE_MERGED_TASK` authorizes and requires verifying the merge on remote
main, synchronizing product and governance mains, rereading `ACTIVE_TASK.md`,
and preparing the smallest bounded governance promotion. A status-only
response in this state is a dispatcher failure.
`PROMOTE_RESOLVED_TASK` authorizes and requires verifying the governance resolution on remote main, synchronizing product and governance mains, rereading `ACTIVE_TASK.md`, and preparing the smallest bounded governance promotion for resolved tasks without product code changes. A status-only response in this state is a dispatcher failure.
