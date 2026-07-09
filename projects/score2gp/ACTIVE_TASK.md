# Active Task

**Task**: Req-131 / Task 78: Design rest mapping and rhythm timeline reconstruction schema
**Authorised Role**: Architect
**Repository**: `score2gp-agentops`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Architect must design the schema, voice alignment cursor rules, and duration reconstruction formulas for injecting quarter, half, and whole rests into ScoreIR and GP7 packages under Req-131, checking in the rest/rhythm pitch translation lookup document.

## 1. Baseline
- Req-130 accidental and key signature pitch mapping implementation is complete.
- Basic clefs, rests, and pitch mapping diagnostics are hardened.

## 2. Context
Having completed clef-aware and accidental-aware pitch mapping, we can now design the timeline rules for inserting rests and reconstructing the musical timeline in ScoreIR.

## 3. Goal
Create a rest mapping and rhythm timeline reconstruction schema document.

## 4. Non-goals
- Do not modify product code in score2gp.
- Do not implement the timeline logic in Python.
- Do not write playable GP files containing rests.

## 5. Scope
All changes must be within `score2gp-agentops`.

## 6. Suggested Work Branch
`governance/req-131-rest-timeline-schema-v0.1`

## 7. Required Validation
Check that the document covers voice cursors, polyphonic alignments, and rest insertion rules.

## 8. Acceptance Criteria
- Rest mapping and rhythm timeline schema document completed and approved.
- Details voice cursors, polyphonic alignments, and rest insertion rules.

## 9. Next Steps
- Review Req-131 rest mapping and rhythm timeline schema design.
- Implement the python timeline logic.
