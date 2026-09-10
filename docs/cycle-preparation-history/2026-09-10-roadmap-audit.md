# AGY Cycle Roadmap Audit — 2026-09-10

## Scope

Audited the merged AGY Cycle v2 implementation after PR #666 and prepared the
highest-priority next cycle.

## Findings and priority

| Priority | Gap | Why it matters | Planned task |
|---|---|---|---|
| P0 | Completion is runtime-only | Restart can reselect completed work | AGY-002 |
| P0 | Worktrees/pushes are not fully managed | Cycles can share source or create an unverified PR | AGY-003 |
| P1 | Reviewer dispatch is local-only | Self-review and stale-head risks remain at the integration boundary | AGY-004 |
| P1 | PTY behavior is untested | Interactive cycles may hang or lose recovery state | AGY-005 |
| P1 | Readiness preflight is incomplete | Proposed/stale tasks can look executable | AGY-006 |
| P2 | History/reporting needs a durable compact ledger | Future review needs facts without raw logs | AGY-007 |
| P2 | Legacy process paths remain | Operators may accidentally use the old state engines | AGY-008 |

## First next cycle prepared

`AGY-002 — Make cycle completion durable and restart-safe`

- Status: `READY`
- Repository: `score2gp-agentops`
- Branch: `feat/agy-cycle-durable-completion`
- Base SHA: `ebd56d1876dde5947fda16d7102d90a89d615b66`
- Resource group: `agy-control`
- Cardinality: `1`
- Ordinality: `1`
- Dependencies: `AGY-001`, which is complete in PR #666

## Preparation checks

- AgentOps `main` baseline is the PR #666 merge commit.
- AgentOps working tree is clean before preparation.
- Existing AgentOps suite: `266 passed, 2 skipped`.
- Candidate task has explicit paths, acceptance criteria, and validation.
- REC-06 remains blocked and cannot outrank AGY-002.
- No AGY-002 cycle has been claimed or implemented.

## Next operator action

After this preparation change is merged, claim only AGY-002:

```bash
scripts/agy-cycle claim AGY-002
```

Do not claim REC-06 until PR #665 is resolved and its missing product paths and
validation toolchain have been independently confirmed.
