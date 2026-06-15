# Post-Task 156: Record Staff-Position Inference and Authorise Pitch-Boundary Discovery

## Context
Product Task 156 is complete.

Product PR #279 completed Product Task 156 in `tticom/score2gp`:
- Final head SHA: `b7c1ed54494c976384d420844cc70396c8d30a48`
- Merge commit: `bc453e33be4e9af9d6e5a25951e8d0faef9da667`

## Decisions Recorded
* Read-only `staff_position_index` now exists for note candidates.
* The staff-position index definition is a deterministic integer explicitly defined relative to the top staff line (index 0). It increments downward through lines and spaces (e.g., 0 = top line, 1 = first space below, 2 = second line).
* The implementation is explicitly non-pitch and contains no pitch derivations.
* Malformed candidate inputs (e.g., missing bboxes, reversed coordinates, non-sequence types) safely fail closed.
* Pitch inference is still not authorised.
* Clef recognition, octave naming, ledger lines, accidentals, rhythm, ScoreIR, MusicXML, and Guitar Pro output remain entirely out of scope.

## Next Step
Product Task 158 is authorised as a discovery-only task.

Product Task 158 must **not** implement pitch inference. Its purpose is to discover what explicit evidence, assumptions, and fixtures are required before read-only pitch inference can be safely implemented.
