# Active Task

**Task**: FS-02: Canonical Entry-Point Reconciliation
**Authorised Role**: Developer
**Repository**: `tticom/score2gp` (product) and `tticom/score2gp-agentops` (governance)

## Status

READY_FOR_EXTERNAL_MERGE

## Task Authorised

FS-02 remains active. A previous completion record was invalidated because it
used a noncanonical probe and erased the local preflight state before it could
be assessed. Do not begin the corrective investigation until the WSL Execution
Environment Gate is externally merged.

## Permissions and Boundaries

- Start from `origin/main` in both repositories, using the Linux workspace
  required by `AGENT_CONTROL.md`.
- Implement only FS-02 as defined in
  `projects/score2gp/programmes/2026-07-19-runtime-provenance-functional-stabilisation.md`.
- Use FS-01 evidence to answer one question: which committed function path is
  actually run by the supported command.
- Probe the supported `.venv/bin/score2gp convert` command, not an inferred
  module invocation.
- If a local auto-OMR path exists but is not committed, classify it as an
  uncontrolled runtime. Do not claim it was discarded unless its state was
  recorded before any destructive action.
- Do not describe an external OMR engine, a deterministic generator, or a
  diagnostic bridge as the product route without direct function and revision
  evidence.

## Completion Evidence

1. A clear, evidence-backed answer on which committed function path is actually run.
2. A native WSL probe of the supported command, with exact executable, import
   path, product SHA, report, stage, and refusal/output outcome.
3. Any uncontrolled runtime is accurately classified without deleting or
   recreating evidence.
4. A distinct Reviewer verifies the exact PR head.
5. Agy leaves the accepted PR `READY_FOR_EXTERNAL_MERGE`.

## Unattended Continuation

This task opts into the Unattended Consecutive Loop Protocol for developer and
review rework only. After acceptance, Agy must prepare the external-merge
handoff and may continue only with an independent approved task.
