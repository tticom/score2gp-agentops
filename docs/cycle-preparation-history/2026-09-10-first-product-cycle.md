# First Product Cycle Preparation — 2026-09-10

## Purpose

Record how the repositories were prepared after AGY Cycle v2 merged, so a
future operator can review the preparation process and distinguish a genuinely
ready cycle from a merely proposed one.

## Preparation branch

```text
chore/prepare-first-agy-cycle
```

Preparation began from AgentOps `main` after PR #666.

## Recorded baselines

| Repository | Branch | SHA | Working tree |
|---|---|---|---|
| `score2gp-agentops` | `main` | `ebd56d1876dde5947fda16d7102d90a89d615b66` | clean |
| `score2gp` | `main` | `eae1afb5d875f6d3f3603c3601865485ca9a3dee` | clean |

The AgentOps baseline includes the merged deterministic AGY Cycle v2 process.

## Completed preparation checks

- AgentOps working tree is clean.
- Product working tree is clean.
- AgentOps full test suite passes: `266 passed, 2 skipped`.
- AGY Cycle tests pass: `11 passed`.
- Product repository is on `main` at the recorded baseline.
- No implementation worktree or product branch has been created for REC-06.
- No product PR has been opened for REC-06.

## Candidate cycle

The first candidate is REC-06 — Staff and System Topology, derived from the
current project authority and its proposed prompt.

Its intended contract is recorded in `plan/backlog.yaml`:

- one cycle;
- branch `feat/rec-06-staff-system-topology`;
- resource group `recognition-topology`;
- explicit source/test paths;
- topology-only acceptance criteria;
- no pitch, duration, measure, voice, or event semantics.

## Blockers discovered during preparation

The cycle must not start yet:

1. PR #665, which proposed REC-06 authority, was closed as superseded by
   `tticom` at `2026-09-10T08:53:09Z`; REC-06 authority is not promoted.
2. `src/score2gp/recognition/topology.py` is absent from product `main`.
3. `tests/recognition/test_topology.py` is absent from product `main`.
4. `mypy` is not installed in the product environment.

The proposed task is therefore recorded as `BLOCKED`, not `READY`. This is an
intentional fail-closed preparation result.

## Unblock and resume procedure

After PR #665 is replaced by a new authority promotion:

1. Fetch both repositories again.
2. Record new exact `main` SHAs.
3. Re-read the live authority and REC-06 prompt.
4. Confirm the assigned source and test paths exist.
5. Install or otherwise provide the declared product validation tools,
   including `mypy`.
6. Update REC-06 to `READY` only after those checks pass.
7. Claim the task with `scripts/agy-cycle claim REC-06`.
8. Create the isolated product worktree and begin the single implementation
   cycle.

No AI should infer that REC-06 is ready from the presence of a proposal or an
old task prompt.
