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

Read `AGENT-RULES.md` for the remaining repository rules.
