# Remediation 03 — Chord Recognition and Capacity Hacks Fix

Status: SKELETON

## Context
The `TopologicallyLockedBarTimeline` from CRP-10 currently fails to correctly recognize chords. Instead of enforcing true capacity invariants, it silently truncates overlapping same-voice notes and pads misaligned measures with synthetic `padding_rest` data. This indicates that the system still cannot accurately recognize chords and is applying partition hacks to force the output into a valid state.

## Goal
Fix `TopologicallyLockedBarTimeline` so that it correctly recognizes simultaneous notes (chords) in the same voice without truncating them as overlaps. Remove the silent truncation and synthetic `padding_rest` data injection. The system must natively support and preserve chord structures based on OMR evidence.

## Acceptance
- Overlapping same-voice notes with identical start times are properly parsed as chords.
- `TopologicallyLockedBarTimeline` no longer silently truncates notes or injects `padding_rest`.
- If a measure violates capacity, it fails loudly and actionably rather than silently padding.
