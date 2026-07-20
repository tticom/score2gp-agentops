# Active Task

**Task**: FS-03: Stabilise The Real Path
**Authorised Role**: Developer
**Repository**: `tticom/score2gp` (product) and `tticom/score2gp-agentops` (governance)

## Status

APPROVED

## Task Authorised

Yes. FS-02 is complete, confirming that MusicXML sidecars are explicitly required by the committed workflow. The Runtime-Provenance and Functional-Stabilisation Programme may now proceed to FS-03.

## Permissions and Boundaries

- Start from `origin/main` in both repositories.
- Implement only FS-03 as defined in
  `projects/score2gp/programmes/2026-07-19-runtime-provenance-functional-stabilisation.md`.
- Run the selected corpus, identify the first shared source/output divergence, and repair one behaviour class per PR.
- Required evidence follows the event through source evidence, MusicXML, ScoreIR, GPIF, and rendered output where applicable.
- A reviewer must be able to trace a ghost rest by stable event or source identifier before accepting a rest-related claim.

## Completion Evidence

1. A clear PR that repairs one behaviour class.
2. A reviewer verifies the trace of the repaired behaviour.
3. Agy leaves the accepted PR `READY_FOR_EXTERNAL_MERGE`.

## Unattended Continuation

This task opts into the Unattended Consecutive Loop Protocol for developer and
review rework only. After acceptance, Agy must prepare the external-merge
handoff and may continue only with an independent approved task.
