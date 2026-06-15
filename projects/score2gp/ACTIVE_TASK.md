# Active Product Task

## Product Task 164 — Add ledger-line grouping to note candidates

### Scope
- Work in `tticom/score2gp`.
- Implement read-only `ledger_line_candidate` grouping to valid `whole_note_candidate`, `half_note_candidate`, `quarter_note_candidate`, and `eighth_note_candidate` objects.
- A note candidate should include an array of `attached_ledger_lines` referencing the candidate IDs of associated ledger lines.
- Grouping should be performed after `staff_position_index` is computed for both notes and ledger lines.
- A ledger line should only be attached if its `staff_position_index` logically corresponds to or supports the note's `staff_position_index` (e.g. intervening ledger lines must be present).
- A ledger line should vertically overlap or tightly align with the note candidate to be grouped.
- Add tests proving notes above/below the staff correctly group their corresponding ledger lines.
- Add tests proving notes within the staff bounds do not attach spurious ledger lines.
- Fail closed: if a ledger line is geometrically ambiguous or doesn't logically support the note's position, it should remain ungrouped rather than falsely assigned.

### Non-Goals
- Do not alter existing note-candidate extraction logic.
- Do not implement pitch inference.
- Do not implement clef recognition.
- Do not implement accidentals.
- Do not commit private fixtures or sensitive data.
