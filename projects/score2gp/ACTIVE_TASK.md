# Active Task

**Task**: Req-130 / Task 76: Implement accidental and key signature pitch mapping
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Developer must implement the accidental and key signature modifier logic inside `score2gp`, add unit tests verifying mapping correctness, pass verification, push the branch, and open a product PR.

## 1. Baseline
- Req-130 accidental and key signature schema is designed and approved.
- Clef-aware pitch mapping diagnostics are complete.

## 2. Context
Having approved the accidental and key signature rules, we can now implement the mapping modifier calculation and state memory in Python.

## 3. Goal
Implement the accidental modifier engine inside `score2gp` and update read-only note candidate diagnostics.

If visual accidental or key-signature candidate extraction is not already available, do not stop. Implement the pure modifier engine and bounded read-only diagnostic integration against structured inputs/mocks, then document that visual accidental/key-signature detection remains a later task.

## 4. Non-goals
- Do not create ScoreIR events from standard-staff notes.
- Do not change GP writer output.
- Do not implement full visual accidental glyph detection if no existing candidate source exists.
- Do not infer key signatures from arbitrary page text or MusicXML/GP oracle data.

## 5. Scope
Allowed files:
- `src/score2gp/pdf_pitch_mapper.py`
- `src/score2gp/whole_note_recogniser.py`
- `tests/` unit tests for pitch mapper

## 6. Suggested Work Branch
`feature/req-130-accidental-mapping-v0.1`

## 7. Required Validation
Run the full verification suite `make verify`.

## 8. Acceptance Criteria
- Modifier calculation logic is implemented.
- Key signatures and local accidentals are correctly supported.
- Covered by unit tests.
- If visual accidental/key-signature candidates are not available, structured-input tests prove the modifier engine and the implementation report records the deferred visual-detection dependency.
- No ScoreIR, GP writer, MusicXML oracle, rhythm, timeline, or voice behavior changes.
- `make verify` passes.

## 9. Next Steps
- Review Req-130 accidental and key signature implementation.
- Accidental mapping implementation is complete.
