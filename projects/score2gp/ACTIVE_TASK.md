# Active Task

**Task**: Task 106 — Remediation 03: Chord Recognition Implementation
**Status**: PR_OPEN
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: feat/remediation-03-chord-recognition
**Pull Request**: 440
**Original Prompt**: `projects/score2gp/prompts/next/remediation-03-chord-recognition-fix.md`

## Context
The architecture for proper chord recognition and capacity validation has been defined in an ADR. The `TopologicallyLockedBarTimeline` currently uses destructive partition hacks that mask OMR alignment errors.

## Goal
Implement the deterministic chord grouping algorithm and strict capacity validation as defined in the ADR and prompt.

## Acceptance
- The `TopologicallyLockedBarTimeline` preserves OMR evidence natively and groups identical chords.
- Unequal durations at the same start tick are rejected.
- Rest/note collisions at the same start tick are rejected.
- No synthetic `padding_rest` events are injected; short measures trigger `invalid = True`.
- `musicxml_generator.py` refuses to generate XML for invalid measures.
- Existing tests are updated and pass.
