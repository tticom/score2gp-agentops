# Decision Record — Authorise Developer Same-Onset Chord Grouping Task

## Status
APPROVED

## Context
Following the Reviewer architecture re-verification approval of Governance PR #240 (merged at `9c4ec0e7c98ffc923d7ac347f55e9e8a0a6b12cd`), the Architect report concluded that basic OMR candidate extraction for eighth and sixteenth notes is viable on synthetic fixtures, but identified a major blocker in the notation bridge layer (`src/score2gp/notation_bridge.py`): vertically aligned note candidates (chords) are serialized sequentially, violating timing and exceeding measure tick limits. 

The GP writer is verified to support multiple notes in a single event as a chord (iterating over `event.notes` in `gpif.py` lines 1819-1820). Therefore, the next step is to authorise a narrow Developer implementation task to support same-onset chord grouping in the bridge.

## Decision
We authorise a Developer implementation task to implement same-onset chord grouping in `src/score2gp/notation_bridge.py` for eighth and sixteenth notes, with tests in `tests/test_notation_bridge.py`.

## Developer Task Specification
- **Intended Capability**: Group note candidates representing the same onset into a single ScoreIR `Event` containing multiple `Note` objects, preserving timing, duration, and preventing tick overflow. Candidates may be grouped into a single chord Event only when they share the same page identity, system identity, staff index identity, and have horizontal onset/x coordinates within a tolerance of 1.0 point. Candidates with the same x/onset coordinate but different page, system, or staff context must remain separate events.
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
  - GP writer changes unless a failing test proves the existing chord export path cannot consume multiple notes per Event
  - New PDF fixtures
  - Committed `.gp` artifacts
  - Real-world score support claims
- **Required Tests**:
  - same-onset candidates in the same page/system/staff context are grouped into one Event;
  - candidates with the same x/onset coordinate but different page identity are not grouped;
  - candidates with the same x/onset coordinate but different system identity are not grouped;
  - candidates with the same x/onset coordinate but different staff index are not grouped;
  - non-aligned sequential candidates remain sequential;
  - existing eighth/sixteenth duration mapping remains intact;
  - valid same-context chord inputs do not raise `cumulative_duration_exceeds_one_4_4_bar`.
- **Validation Command**:
  - `pytest tests/test_notation_bridge.py`
- **Stop Conditions**:
  - Stop if implementation requires changing OMR candidate extraction or staff geometry.
  - Stop if implementation requires committing generated PDF or GP files.
- **Required Next Review**:
  - Reviewer implementation conformance review.
  - PR readiness review.
