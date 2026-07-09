# Active Task

**Task**: Req-127 / Task 68: Define clef-aware pitch mapping schema
**Authorised Role**: Architect
**Repository**: `score2gp-agentops`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Architect must design the lookup tables and metadata schema for mapping staff positions to MIDI pitches based on the detected clef candidate (treble, bass, alto) as requested by Req-127, checking in the pitch translation lookup document.

## 1. Baseline
- Req-125 multi-clef candidate classification is complete, providing treble, bass, and alto candidates.
- Req-128 whole and half rest candidate extraction is complete.

## 2. Context
This is a post-completion continuation task. Having completed rest and clef classification candidate extraction, we can now design the pitch translation schema that maps staff lines/spaces to pitch.

## 3. Goal
Create a pitch translation lookup document mapping staff positions to MIDI pitches for treble, bass, and alto clefs.

## 4. Non-goals
- Do not modify product code in score2gp.
- Do not implement the mapping logic in Python.
- Do not create ScoreIR events.

## 5. Scope
All changes must be within `score2gp-agentops`.

## 6. Suggested Work Branch
`governance/req-127-pitch-mapping-schema-v0.1`

## 7. Required Validation
Check that the pitch lookup tables cover all 5 lines, 4 spaces, ledger lines (at least 3 above/below), and correct transpositions.

## 8. Acceptance Criteria
- Pitch translation lookup document completed and approved.
- Details the mapping formulas and lookup tables for Treble, Bass, and Alto clefs.

## 9. Next Steps
- Review Req-127 pitch mapping schema.
- Implement the python mapping logic.
