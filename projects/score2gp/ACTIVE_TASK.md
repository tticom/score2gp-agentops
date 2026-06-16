# Active Product Task

## Product Task 168 — Apply clef-resolved staff pitch mapping from deterministic clef evidence

### Scope
- Work in `tticom/score2gp`.
- Use deterministic `treble_clef_candidate` evidence to apply read-only `clef_resolved_staff_pitch` mapping to note candidates through `map_clef_resolved_staff_pitch(...)`.
- Candidate note types in scope: `whole_note_candidate`, `half_note_candidate`, `quarter_note_candidate`, `eighth_note_candidate`.
- Verify that deterministic `treble_clef_candidate` outcomes exist only where evidence is explicit and staff-associated.
- Build or reuse a deterministic staff-level clef policy from `treble_clef_candidate` outcomes.
- Apply `map_clef_resolved_staff_pitch(...)` only to notes on staves with exactly one deterministic treble clef candidate.
- Do not apply clef-resolved pitch mapping to a staff with zero clef candidates or multiple clef candidates.
- Do not apply mapping when clef evidence is malformed, ambiguous, unsupported, or missing.
- In-staff notes may receive `clef_resolved_staff_pitch` only when staff-level clef evidence is explicit and unambiguous.
- Out-of-staff notes may receive `clef_resolved_staff_pitch` only when staff-level clef evidence is explicit and unambiguous, and required ledger-line support is present.
- Use `staff_position_index` as the vertical pitch coordinate.
- Use `attached_ledger_line_candidate_ids` only as supporting evidence for out-of-staff notes, not as an independent pitch source.
- Preserve existing `assumed_treble_pitch` behaviour. Keep `clef_resolved_staff_pitch` semantically distinct.

### Non-Goals
- Do not implement new visual clef recognition.
- Do not guess treble clef globally.
- Do not use `assume_treble_clef` as visual clef evidence.
- Do not infer clef from pitch outcomes, note positions, or ledger-line placement.
- Do not implement accidentals, key signatures, rhythm inference, rests, or OCR.
- Do not emit ScoreIR, MusicXML, or Guitar Pro output.
- Do not alter existing note-candidate extraction, ledger-line extraction, ledger-line grouping, or raster clef heuristics unless a blocker is reported.
- Do not commit private fixtures or sensitive data.
- Do not introduce a score model.
