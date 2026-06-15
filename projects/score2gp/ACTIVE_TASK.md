# Active Product Task

## Product Task 165 — Map logical staff pitches using clef and ledger-line grouping

### Scope
- Work in `tticom/score2gp`.
- Add deterministic, read-only logical pitch mapping for `whole_note_candidate`, `half_note_candidate`, `quarter_note_candidate`, and `eighth_note_candidate`.
- Use existing `staff_position_index` and `attached_ledger_line_candidate_ids` to support mapping.
- Only map logical staff pitches for candidates where clef context is explicit, deterministic, and available.
- If no explicit clef context exists, stop and report the blocker. Do not guess treble clef globally unless an existing `assume_treble_clef` pathway already applies.
- Only assign pitch when required evidence is present. In-staff notes may be pitch-mapped only when clef context is explicit. Out-of-staff notes require explicit clef context AND valid ledger-line support.
- The new read-only field should clearly distinguish deterministic mapping, e.g., `logical_staff_pitch` or `clef_resolved_staff_pitch`.
- Fail closed if clef context is missing/ambiguous, staff position is malformed, or required ledger-line support for out-of-staff notes is missing.

### Non-Goals
- Do not implement clef recognition or guess clef from visual symbols (unless separately authorised).
- Do not implement accidentals, key signatures, rhythm inference, or rests.
- Do not alter existing note-candidate extraction, ledger-line extraction, or ledger-line grouping heuristics (unless a blocker is reported).
- Do not emit ScoreIR, MusicXML, or Guitar Pro output.
- Do not commit private fixtures or sensitive data.
