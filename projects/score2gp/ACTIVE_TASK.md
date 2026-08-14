# Active Task

**Task**: Task 105 — Remediation 03: Chord Recognition Architecture and Capacity Hacks Fix
**Status**: PR_OPEN
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: feat/remediation-03-chord-recognition
**Pull Request**: 440
**Original Prompt**: `projects/score2gp/prompts/next/remediation-03-chord-recognition-fix.md`

## Context
The `TopologicallyLockedBarTimeline` from CRP-10 currently fails to correctly recognize chords. Instead of enforcing true capacity invariants, it silently truncates overlapping same-voice notes and pads misaligned measures with synthetic `padding_rest` data. This indicates that the system still cannot accurately recognize chords and is applying partition hacks to force the output into a valid state. 

Because we do not want to rely on an inferred implementation that might introduce new destructive hacks, we must first design the proper deterministic chord grouping algorithm.

## Goal
Conduct architectural research on how to implement proper chord recognition in `TopologicallyLockedBarTimeline` without relying on silent truncation or synthetic `padding_rest` injection.

1. Investigate how `TopologicallyLockedBarTimeline` currently processes overlapping notes.
2. Determine how true OMR evidence represents simultaneous notes.
3. Design a deterministic algorithm for grouping simultaneous notes into chords without relying on `padding_rest` or truncation.
4. Document the design in an Architectural Decision Record (ADR).
5. Outline the concrete implementation steps in a downstream prompt for the Developer.

## Acceptance
- An ADR is published detailing the deterministic chord grouping algorithm based on real OMR evidence.
- A concrete, non-skeleton implementation prompt is prepared for the Developer role.
- No product code is modified during this architectural phase.
