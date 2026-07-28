# Score2GP executable command entrypoints

For an exact user message `go` or `next`, the first task action must be:

```bash
python3 scripts/score2gp_go_bootstrap.py --product ../score2gp --agentops . --json
```

Run it from the `score2gp-agentops` repository root. Its JSON `state` and
`current_review` are authoritative. Do not query GitHub manually, reuse a
previous handback summary, or reconstruct the state in prose.

- `ADDRESS_CURRENT_PR_REVIEW`: immediately execute
  `projects/score2gp/prompts/next/address-current-pr-review.md` using
  `current_review.id`, `current_review.commit_id`, and `current_review.body`.
- `AWAITING_CODEX_REVIEW` or `READY_FOR_HUMAN_MERGE`: report and stop.
- Any helper failure or missing field: fail closed and report the exact error.

Repeated commands with unchanged JSON are idempotent. Do not create another
task, review, or handback.

For an exact user message `got`, the first task action must be:

```bash
python3 scripts/score2gp_got_bootstrap.py --product ../score2gp --agentops .
```

Its JSON is authoritative. Never resume or replay a prior managed task.
`MERGED_AWAITING_GOVERNANCE_PROMOTION` means verify merged main and prepare
the next governance promotion; historical reviews must not override `MERGED`.

Read `AGENT-RULES.md` and the selected role skill for all other work.
