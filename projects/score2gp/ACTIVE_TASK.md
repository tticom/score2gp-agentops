# Active Task

**Task**: Req-127 / Task 70: Implement clef-aware pitch mapping
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Developer must implement the pitch mapping translation inside `score2gp`, add unit tests verifying treble, bass, and alto mapping correctness, pass verification, push the branch, and open a product PR.

## 1. Baseline
- Req-127 pitch mapping schema is designed and approved.
- Treble, Bass, and Alto clefs, and ledger lines are covered.

## 2. Context
Having approved the mapping tables, we can now implement the translation functions in Python and bind them to the candidate diagnostics output.

## 3. Goal
Implement a helper or function in `score2gp` to map a notehead's `staff_step_index` to MIDI pitch using the active clef candidate.

## 4. Non-goals
- Do not create ScoreIR pitch-mapped note events.
- Do not infer rhythm timelines.

## 5. Scope
Allowed files:
- `src/score2gp/pdf_pitch_mapper.py` or new mapping modules
- `src/score2gp/whole_note_recogniser.py`
- `tests/` unit tests for pitch mapper

## 6. Suggested Work Branch
`feature/req-127-pitch-mapping-v0.1`

## 7. Required Validation
Run the full verification suite `make verify`.

## 8. Acceptance Criteria
- Pitch mapping translation logic is implemented.
- Covered by unit tests for all 3 clefs and ledger lines.
- `make verify` passes.

## 9. Next Steps
- Review Req-127 pitch mapping implementation.
- Clef-aware pitch mapping schema is complete.
