# Active Task

**Task**: CR-03A: Local tuplet-group evidence and meter resolution - Developer Phase
**Authorised Role**: Developer
**Repository**: `tticom/score2gp` (product) and `tticom/score2gp-agentops` (governance)

## Status

APPROVED

## Task Authorised

Yes, Tier 2 implementation phase authorized.

## Permissions and Boundaries

- Create the product branch from current product `origin/main` only.
- Modify only `src/score2gp/whole_note_recogniser.py` and new or directly related
  public tests for this association model.
- Implement staff-local measure spans, `TupletMarkerEvidence`, and
  `TupletAssociation` before `build_staff_timeline_preview` slices chords.
- Test one genuine above-staff 3:2 tuplet and the TAB, measure-label, metadata,
  and ambiguous-geometry rejection cases using public synthetic data.
- Do not import, cherry-pick, copy, or depend on the recovery prototype or
  product PRs #371/#372. Do not add automatic OMR orchestration or a
  deterministic MusicXML emitter; neither is present on product `origin/main`.
- Product PR creation is permitted after validation. Guarded autonomous merge
  is permitted only after independent Reviewer conformance review and every
  condition in `programmes/2026-07-18-unattended-consecutive-loop-protocol.md`.

## Completion Evidence

1. A public synthetic test proves one unique above-staff 3:2 association and
   rejects TAB, measure-label, metadata, and ambiguous candidates.
2. Association evidence retains marker, candidate, and span identities without
   changing unrelated meter or event-slicing behavior.
3. A focused product PR targets current product `origin/main` and records the
   limitation that end-to-end deterministic MusicXML emission is not in scope.

## Unattended Continuation

This task opts into the Visual Output Correctness Recovery Programme's
Unattended Consecutive Loop Protocol. After review, rework, or guarded merge,
agents must continue to the next required role or eligible task without routine
maintainer confirmation. Before a genuine stop, they must commit the required
human-focused end-of-run report in AgentOps.
