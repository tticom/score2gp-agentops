# Active Task

**Task**: FS-02: Canonical Entry-Point Reconciliation
**Authorised Role**: Developer
**Repository**: `tticom/score2gp` (product) and `tticom/score2gp-agentops` (governance)

## Status

APPROVED

## Task Authorised

Yes. FS-01 was externally merged as product PR #378. The Runtime-Provenance
and Functional-Stabilisation Programme may now proceed to FS-02.

## Permissions and Boundaries

- Start from `origin/main` in both repositories.
- Implement only FS-02 as defined in
  `projects/score2gp/programmes/2026-07-19-runtime-provenance-functional-stabilisation.md`.
- Use FS-01 evidence to answer one question: which committed function path is actually run by the supported command?
- If a local auto-OMR path exists but is not committed, it is an uncontrolled runtime and must be cleanly committed and reviewed or discarded.
- Do not describe an external OMR engine, a deterministic generator, or a diagnostic bridge as the product route without direct function and revision evidence.

## Completion Evidence

1. A clear, evidence-backed answer on which committed function path is actually run.
2. If an uncontrolled runtime was found, it is cleanly committed and reviewed, or discarded.
3. A distinct Reviewer verifies the exact PR head.
4. Agy leaves the accepted PR `READY_FOR_EXTERNAL_MERGE`.

## Unattended Continuation

This task opts into the Unattended Consecutive Loop Protocol for developer and
review rework only. After acceptance, Agy must prepare the external-merge
handoff and may continue only with an independent approved task.
