# AGY Cycle Roadmap

This roadmap records the remaining work after AGY Cycle v2 merged in PR #666.
Priorities are based on the risk of false readiness, duplicate execution, or
loss of recoverable state.

## P0 — must complete before relying on unattended cycles

### AGY-002 — Durable completion and restart recovery

Status: READY and prepared as the next cycle.

The current runtime records are ignored. Completing a cycle releases locks but
does not durably update the backlog or write a durable completion summary. A
restart can therefore make a previously completed task appear executable again.

Required outcome:

- write an append-only completion record containing task ID, cycle ID, PR,
  exact head, merge commit, validation receipt, and completion time;
- make `complete` idempotent;
- prevent a completed task from being claimed after runtime state is gone;
- preserve successor preparation without executing it;
- add crash/replay tests.

### AGY-003 — Worktree lifecycle and publish verification

The controller can inspect an optional worktree but does not create the
isolated worktree, verify branch ancestry, or push/read back the remote branch
before creating a PR.

Required outcome:

- create one disposable worktree per cycle;
- verify the branch starts at the recorded base SHA;
- validate changed paths and clean state;
- push without force and read back the remote head;
- create or find exactly one PR only after successful publication.

## P1 — required for safe multi-agent operation

### AGY-004 — Exact-head reviewer routing

The local `review` command prevents a matching owner string, but does not yet
dispatch or authenticate an independent reviewer against the live PR head.
Add reviewer assignments, remote identity checks, detached read-only worktrees,
and stale-head rejection at review time.

### AGY-005 — Interactive AGY reliability

`run_interactive` uses POSIX PTY handling but has no regression tests for
non-TTY input, child exit, buffering, timeout, or interrupted sessions. Add a
fake interactive CLI harness and make failure/recovery behavior deterministic.

### AGY-006 — Readiness preflight

Before claim, verify repository, base SHA, required paths, validation tools,
branch name, and dependency authority. A proposed or stale task must remain
blocked instead of becoming claimable because its YAML is syntactically valid.

## P2 — operational improvements

### AGY-007 — Durable cycle history and operator reporting

Promote cycle summaries, validation receipts, and repair actions into a compact
reviewable history without committing raw logs or private artifacts.

### AGY-008 — Compatibility retirement

After two successful real product cycles, retire duplicated `go`/`got`, active
task reducers, and obsolete Docker execution paths from the normal process.

## Exit criteria for the roadmap

The process is ready for unattended product cycles when AGY-002 through AGY-006
are complete, two independent product cycles have passed, and one review-fix
round has been exercised on the same PR.
