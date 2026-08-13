# Remediation 02 — Unowned Notes Bug Fix & Hand Position Research

Status: SKELETON

## Context
The `ScoreIRCompiler` currently fails on "unowned notes", and CRP-12 papered over this by silently injecting a fake `(string=1, fret=0)` note, producing musically corrupt output. A system that simply fails on unowned notes is useless; we must understand and fix what is *causing* notes to be unowned in the first place.

Additionally, the `BiomechanicalPositionOptimizer` assumes sequential hand jumps, but musicians play chords as single hand shapes, and some musicians move around the fretboard more than others. We need to determine if recording explicit hand positions is actually necessary or if we should rely solely on the explicit TAB fret/string evidence.

## Goal
1. **Fix Unowned Notes Bug**: Trace the lifecycle of a note from OMR evidence through the compiler to identify why notes are arriving at the compiler without valid TAB string/fret ownership. Fix the bug at its source (likely in the fusion or extraction layer) so that the compiler does not receive unowned notes, and remove the synthetic `(string=1, fret=0)` injection fallback.
2. **Research Hand Positions**: Conduct research and document a design decision on whether it is strictly necessary to infer and record physical hand positions, or if we can rely entirely on the provided explicit TAB data.

## Acceptance
- The root cause of unowned notes is identified and fixed upstream.
- The `ScoreIRCompiler` strictly refuses synthetic generation and throws a clear, actionable error if it ever receives an unowned note.
- An architectural decision record (ADR) or research note answering whether recording hand positions is necessary, taking into account varying musician styles and chord shapes.
