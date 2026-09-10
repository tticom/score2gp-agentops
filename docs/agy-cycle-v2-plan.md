# AGY Cycle v2: Combined Process Plan

This document records the comparison between the earlier ORC-04 integrated
PR-lifecycle plan and the simpler AGY Cycle design, and defines the process
implemented by this repository.

## Findings from PR #665 / ORC-04

The earlier design provides the correctness guarantees that the simpler
runner must retain:

- exact remote branch and PR head verification;
- one PR per task branch;
- stable task IDs and leases;
- isolated worktrees and runtime directories;
- exact-head, read-only reviewer routing;
- no self-review;
- idempotent post-merge reconciliation;
- falsification checks for stale heads, branch reuse, failed PR creation, and
  concurrent cycles.

PR #665 itself promotes REC-06 and changes the orchestration pointer. The
ORC-04 task behind it defines the integrated lifecycle and concurrent-review
requirements. Those requirements are retained here without retaining the
multiple-file governance handoff process.

## AGY Cycle simplifications

The operator-facing process is intentionally smaller:

- `.agy/flow.yaml` is the only lifecycle-transition definition;
- `plan/backlog.yaml` owns backlog, sprint, ordering, dependencies, and scope;
- cycle records and leases are runtime data, ignored by Git;
- AGY is an interactive worker, not a state manager;
- Orca calls deterministic commands and consumes JSON results;
- one task, one branch, one worktree, and one PR per cycle;
- resetting a stuck cycle is one command;
- Docker is optional and not required for normal execution.

## Lifecycle

```text
READY -> CLAIMED -> IMPLEMENTING -> VALIDATING -> PR_OPEN
  -> REVIEW_REQUIRED -> APPROVED -> MERGE_READY -> MERGED
  -> RECONCILED -> COMPLETE
```

Exceptional states are `BLOCKED`, `FAILED`, and `CANCELLED`.

Rules:

1. `cardinality: 1` is required for an executable task.
2. A cycle can attach exactly one PR.
3. The PR head SHA is recorded and re-read before every review or merge
   decision.
4. Review fixes stay on the same branch and PR.
5. A successor may be prepared but never automatically executed.
6. Reconciliation is idempotent.

## Files

```text
.agy/
  flow.yaml                 # transition rules and hard limits
  prompts/                  # bounded AGY prompts
  cycles/<cycle-id>.json    # ignored runtime record
plan/backlog.yaml           # planning authority
```

`ACTIVE_TASK.md` and `ORCHESTRATION_STATE.json` may be generated as temporary
compatibility views, but they are not independently authored state in this
process.

## Concurrent execution

The task claim is atomic. Every claimed task receives a unique cycle ID,
lease, branch, worktree, runtime directory, and PR. Tasks may run in parallel
when their task IDs and declared `resource_group` values do not conflict.
Writable controller state is never shared between cycles.

## Roles

- **AGY/implementation** edits the assigned worktree and runs validation.
- **Orca** claims work, invokes commands, and collects machine-readable facts.
- **Reviewer** receives a detached read-only worktree and an exact PR head.
- **Human/integration authority** decides merge; workers never merge.

The controller commands are deliberately explicit:

```bash
scripts/agy-cycle transition CYCLE-ID VALIDATING
scripts/agy-cycle validate CYCLE-ID
scripts/agy-cycle open-pr CYCLE-ID --repository ORG/REPO
scripts/agy-cycle verify-pr CYCLE-ID
```

The first command creates no external side effect; `validate` writes a receipt;
`open-pr` creates or finds the sole PR and verifies its head; `verify-pr` reads
the live PR again before review or merge decisions.

## Repair

```bash
scripts/agy-cycle status CYCLE-ID
scripts/agy-cycle reset CYCLE-ID FAILED
scripts/agy-cycle reset CYCLE-ID READY
```

If the transition logic itself is wrong, the human changes only
`.agy/flow.yaml`. No model reconstructs state from prose or old handoffs.

## Required falsification tests

- claim the same task concurrently and prove only one claim succeeds;
- attempt to claim a task with unmet dependencies and prove it fails;
- attach a second PR and prove it fails;
- move a remote PR head and prove review is invalidated;
- attempt self-review and prove it is rejected;
- run two independent tasks concurrently and prove their worktrees and
  receipts are separate;
- replay reconciliation and prove no duplicate completion or successor
  execution occurs.
