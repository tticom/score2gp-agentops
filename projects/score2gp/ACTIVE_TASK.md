# Active Task

**Task**: Req-130 / Task 74: Design accidental and key signature pitch mapping schema
**Authorised Role**: Architect
**Repository**: `score2gp-agentops`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Architect must design the lookup tables, metadata schema, and modifier rules for modifying base MIDI pitches based on accidental candidates (sharps, flats, naturals) and key signatures under Req-130, checking in the accidental/key signature pitch translation lookup document.

## 1. Baseline
- Req-129 pitch mapping diagnostic integration is complete.
- Treble, Bass, and Alto clefs, and ledger lines are covered.

## 2. Context
Having verified read-only pitch mapping for natural notes, we can now design the accidental and key signature schema to support sharps, flats, and key-specific pitch offsets.

## 3. Goal
Create a pitch translation lookup document mapping accidental candidates and key signatures to base pitch modifiers.

## 4. Non-goals
- Do not modify product code in score2gp.
- Do not implement the modifier logic in Python.
- Do not create ScoreIR events.

## 5. Scope
All changes must be within `score2gp-agentops`.

## 6. Suggested Work Branch
`governance/req-130-accidental-schema-v0.1`

## 7. Required Validation
Check that the lookup tables cover sharps, flats, naturals, and major/minor key signatures.

## 8. Acceptance Criteria
- Accidental and key signature schema document completed and approved.
- Details the modifiers for natural notes, accidental lookup tables, and key signatures.

## 9. Next Steps
- Review Req-130 accidental and key signature schema.
- Implement the python modifier logic.
