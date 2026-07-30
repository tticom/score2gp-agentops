# Score2GP executable command entrypoints

For any request to continue, advance, run the next command, `go`, `got`, or
`next`, execute this identity-aware router before any manual inspection:

```bash
python3 scripts/score2gp_dispatch.py --product ../score2gp --agentops . --json
```

The Linux worker identity, not the command word, selects the role:
`tticom-automation` runs author `go`; `tticom-gov` (or the legacy
`tticom-codex` worker) runs governance `got`. Never bypass the router by
calling the other role's helper. Treat its JSON as authoritative. Never replace it with direct GitHub queries
or a cached handback. `ADDRESS_CURRENT_PR_REVIEW` means execute
`projects/score2gp/prompts/next/address-current-pr-review.md` with the returned
formal review ID, commit ID, and body. Fail closed if the helper fails.
Only `EXECUTE_PROMPT` and `ADDRESS_CURRENT_PR_REVIEW` authorize task actions.
For `MERGED_AWAITING_GOVERNANCE_PROMOTION`, report the state and stop without
rerunning, re-verifying, or summarizing the completed task. Also report the
returned `next_action`: governance must run `got`, which dispatches
`PROMOTE_MERGED_TASK`. Treat every other unrecognized or non-action state as
terminal.

Read `AGENT-RULES.md` for the remaining repository rules.

For governance, treat the routed JSON as authoritative and never resume a
cached managed task.
For `got`, `REVIEW_CURRENT_HEAD` authorizes and requires an exact-head formal
review using the pinned `code-review` skill and Score2GP hard-review overlay;
a status-only response is a dispatcher failure. This `got` state is separate
from the action-authorizing states defined above for `go`.
`PROMOTE_MERGED_TASK` authorizes and requires verifying the merge on remote
main, synchronizing product and governance mains, rereading `ACTIVE_TASK.md`,
and preparing the smallest bounded governance promotion. A status-only
response in this state is a dispatcher failure.
