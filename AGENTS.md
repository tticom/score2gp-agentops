# Score2GP executable command entrypoints

For an exact user message `go` or `next`, execute this before any manual
inspection:

```bash
python3 scripts/score2gp_go_bootstrap.py --product ../score2gp --agentops . --json
```

Treat its JSON as authoritative. Never replace it with direct GitHub queries
or a cached handback. `ADDRESS_CURRENT_PR_REVIEW` means execute
`projects/score2gp/prompts/next/address-current-pr-review.md` with the returned
formal review ID, commit ID, and body. Fail closed if the helper fails.
Only `EXECUTE_PROMPT` and `ADDRESS_CURRENT_PR_REVIEW` authorize task actions.
For `MERGED_AWAITING_GOVERNANCE_PROMOTION`, report the state and stop without
rerunning, re-verifying, or summarizing the completed task. Treat every other
unrecognized or non-action state as terminal.

Read `AGENT-RULES.md` for the remaining repository rules.

For an exact user message `got`, first execute:

```bash
python3 scripts/score2gp_got_bootstrap.py --product ../score2gp --agentops .
```

Treat its JSON as authoritative and never resume a cached managed task.
