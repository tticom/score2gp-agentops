# Active Product Task

## Product Task 163 — Add read-only staff-position indexing for ledger-line candidates

### Scope
- Work in `tticom/score2gp`.
- Add read-only `staff_position_index` to valid `ledger_line_candidate` objects.
- Use existing staff geometry and existing staff-position indexing convention.
- Preserve the established convention:
  - `0` = top staff line
  - `1` = first space below top staff line
  - `2` = second staff line
  - values increase downward
  - `8` = bottom staff line
- Positions above the staff must be negative.
- Positions below the staff must be greater than `8`.
- Use ledger-line candidate geometry only after a candidate has already been safely promoted.
- Fail closed if the ledger-line candidate is missing required geometry or cannot be safely associated with a staff.
- Add tests proving correct staff-position indexes for ledger lines above and below the staff.
- Add tests proving existing note-candidate `staff_position_index` behaviour remains unchanged.
- Add tests proving `assumed_treble_pitch` behaviour remains unchanged.
- Add tests proving no pitch field is added to `ledger_line_candidate`.
- Preserve ledger-line extraction behaviour from Task 162.
- Preserve duplicate beam/ledger suppression behaviour from Task 162.
- Preserve whole-note recognition compatibility.

### Non-Goals
- Do not implement pitch inference.
- Do not implement ledger-line pitch mapping.
- Do not extend `assumed_treble_pitch` to ledger lines.
- Do not alter existing note-candidate staff-position semantics.
- Do not alter ledger-line extraction heuristics unless a blocker is reported.
- Do not implement clef recognition.
- Do not implement accidentals.
- Do not implement key signatures.
- Do not implement rhythm inference.
- Do not emit ScoreIR, MusicXML, Guitar Pro, GP output, OCR, or rests.
- Do not commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.
