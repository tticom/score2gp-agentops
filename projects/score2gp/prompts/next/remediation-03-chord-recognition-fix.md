# Remediation 03 — Chord Recognition Implementation

Status: ACTIVE

## Context
The architecture for proper chord recognition and capacity validation has been defined in `docs/design/2026-08-14-chord-recognition-architecture-v2.md`. The `TopologicallyLockedBarTimeline` currently uses destructive partition hacks (silent duration truncation and `padding_rest` injection) that mask OMR alignment errors.

## Goal
Implement the deterministic chord grouping algorithm and strict capacity validation as defined in the ADR.

1. **Remove Hacks**: Remove the nested loops in `TopologicallyLockedBarTimeline` that dynamically shrink `duration_ticks` when overlapping with `start_tick`. Also remove the logic that injects `padding_rest` when the cursor falls short of the measure duration.
2. **Strict Chord Equivalence**: Group candidates into a chord if and only if they share the exact same `voice`, `start_tick`, and `duration_ticks`. 
3. **Invalidate on Polyphony/Conflict**: If notes share a `start_tick` and `voice` but have unequal `duration_ticks`, the timeline must explicitly refuse to process them as a single-voice chord. Set `invalid = True` on the timeline object and leave the `events` ledger unaltered.
4. **Invalidate on Capacity Mismatch**: If the final cursor position does not exactly equal `D_measure`, or if there is an explicit overlap between distinct time slices, set `invalid = True`.
5. **Consumer Refusal**: Update downstream consumers (such as `musicxml_generator.py`) to explicitly refuse to compile invalid measures by throwing a capacity mismatch error rather than silently repairing them.

## Acceptance
- The `TopologicallyLockedBarTimeline` preserves OMR evidence natively and groups identical chords.
- Unequal durations at the same start tick are rejected and trigger `invalid = True`.
- No synthetic `padding_rest` events are injected; short measures trigger `invalid = True`.
- `musicxml_generator.py` refuses to generate XML for invalid measures.
- Existing tests (e.g. `test_musical_timeline_replacement.py`) are updated to expect `invalid = True` instead of padding/truncation, and new tests prove strict chord behavior.
