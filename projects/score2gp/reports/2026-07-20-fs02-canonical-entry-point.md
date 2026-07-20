# FS-02: Invalidated Canonical Entry-Point Investigation

## Status

Invalidated. This document replaces the premature FS-02 completion claim.

## Why The Prior Finding Cannot Be Accepted

The prior run did observe a `missing_musicxml` refusal from
`.venv/bin/python -m score2gp.cli`. That module invocation is not the
supported console command established by FS-01, so it does not establish the
production entry point.

Before preserving the relevant local state, the agent also ran:

```bash
git reset --hard origin/main
git clean -fd
```

Those actions violated the control policy and may have deleted untracked local
code or generated evidence. Consequently, the run cannot establish whether a
pre-clean local auto-OMR path existed, nor that one was discarded.

## Bounded Facts Retained

- Product PR #378 merged as `e72cd7c8de5277d3d3ba91234c0eea4fbd63e145`.
- Its accepted head was `a8ba0e75d57f558d07acfaa0e5292f753025b533`.
- The prior module probe reported `missing_musicxml` at the
  `orchestration-gate`; this is an observation about that invocation only.

## Required Corrective Investigation

FS-02 remains active. A new WSL-controlled run must:

1. prove the canonical Linux worktree and runtime under `AGENT_CONTROL.md`;
2. invoke the supported `.venv/bin/score2gp convert` command exactly;
3. trace the console-script target and committed calls reachable from
   `convert`, including any claimed `omr` command; and
4. record the exact revision, executable, import path, report, and outcome.

No conclusion about uncommitted local routes is permitted unless it is based on
state captured before any destructive action.
