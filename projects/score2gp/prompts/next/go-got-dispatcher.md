# GOV-GO-GOT-01 — State-Aware Agent Handoff Dispatch

## Objective

Replace the static task pointer with permanent role-specific dispatchers so
the maintainer can use `go` for Agy and `got` for Codex throughout the full
author, review, fix, re-review, and merge cycle.

## Publication

Review governance PR `https://github.com/tticom/score2gp-agentops/pull/383`.

## Scope

Governance documentation and tests only. Preserve identity separation,
one-task/one-PR discipline, human-only merging, evidence contracts, and the
rule that candidates are not authority.

## Acceptance

- `NEXT.md` permanently routes `go` and `got`.
- Dispatch uses the exact configured repository and branch, never recency.
- Agy cannot replay a merged original prompt.
- Codex cannot review without a handback pinned to the live head.
- Review fixes remain on the existing PR.
- Approval stops at the human merge gate.
- Merge routes Codex to governance promotion, not product implementation.
- Governance tests cover these invariants.

## Validation

Run the governance pytest suite, governance audit, and `git diff --check`.
Publish one AgentOps PR from `codex/go-got-dispatcher` and stop for independent
review. Do not merge it.
