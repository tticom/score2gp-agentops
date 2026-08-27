# REC-12 — Constrained Semantic Resolver

Status: SKELETON — depends on REC-11
Role: Developer
Repository: `score2gp`

## Objective

Resolve graph hypotheses into boundaries, measures, strings, onsets, chords,
durations and voices using explicit hard constraints and ranked soft evidence.

## Required work

1. Version and document every hard and soft constraint.
2. Return Resolved, Ambiguous, Unsupported or Contradictory at relevant scopes.
3. Enforce exclusivity, topology locality, voice timing and measure capacity.
4. Preserve all supporting and rejected hypothesis IDs.
5. Never scale durations, invent measures, drop events or synthesize unlabeled
   fingering to obtain consistency.

## Acceptance and falsification

- Local confidence cannot override a violated hard constraint.
- Cross-modal disagreement is visible in the resolution result.
- Known destructive capacity hacks fail closed.

## Validation

Promoted prompt must define held-out coverage/risk targets and use REC-01 event,
rhythm and complete-measure layers on multiple score families.

