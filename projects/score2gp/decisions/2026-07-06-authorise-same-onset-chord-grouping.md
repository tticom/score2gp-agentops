# Decision Record — Authorise Developer Same-Onset Chord Grouping Task

## Status
APPROVED

## Context
Following the Reviewer architecture re-verification approval of Governance PR #240 (merged at `9c4ec0e7c98ffc923d7ac347f55e9e8a0a6b12cd`), the Architect report concluded that basic OMR candidate extraction for eighth and sixteenth notes is viable on synthetic fixtures, but identified a major blocker in the notation bridge layer (`src/score2gp/notation_bridge.py`): vertically aligned note candidates (chords) are serialized sequentially, violating timing and exceeding measure tick limits. 

The GP writer is verified to support multiple notes in a single event as a chord (iterating over `event.notes` in `gpif.py` lines 1819-1820). Therefore, the next step is to authorise a narrow Developer implementation task to support same-onset chord grouping in the bridge.

## Decision
We authorise a Developer implementation task to implement same-onset chord grouping in `src/score2gp/notation_bridge.py` for eighth and sixteenth notes, with tests in `tests/test_notation_bridge.py`.

## Developer Task Specification
- **Intended Capability**: Group note candidates representing the same onset into a single ScoreIR `Event` containing multiple `Note` objects, preserving timing, duration, and preventing tick overflow.
- **Allowed Files**:
  - `src/score2gp/notation_bridge.py`
  - `tests/test_notation_bridge.py`
- **Explicit Non-goals**:
  - True polyphony
  - Same-staff multi-voice support
  - Voice separation
  - Multiple independent rhythmic voices
  - OMR candidate extraction changes
  - Staff geometry changes
  - New PDF fixtures
  - Committed `.gp` artifacts
  - Real-world score support claims
- **Required Tests**:
  - Mock candidates representing same-onset chords are grouped into one Event.
  - The Event contains multiple Notes.
  - Onset ticks are shared for grouped chord notes.
  - Duration ticks are correct for eighth and sixteenth notes.
  - Valid chord inputs do not raise `cumulative_duration_exceeds_one_4_4_bar`.
  - Non-aligned sequential candidates remain sequential.
  - Existing duration mapping for eighth/sixteenth notes remains intact.
- **Validation Command**:
  - `pytest tests/test_notation_bridge.py`
- **Stop Conditions**:
  - Stop if implementation requires changing OMR candidate extraction or staff geometry.
  - Stop if implementation requires committing generated PDF or GP files.
- **Required Next Review**:
  - Reviewer implementation conformance review.
  - PR readiness review.
