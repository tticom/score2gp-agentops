# Decision: Post-Task 143 Eighth-Note Fixture Prerequisite

## Context
Product Task 143 was discovery-only. The goal was to discover whether current generic candidate evidence is sufficient to safely implement `eighth_note_candidate` reporting.

## Findings
- `quarter_note_candidate`, `flag_candidate`, and `beam_candidate` outputs correctly expose `page_index`, `system_index`, `staff_index`, and `bbox`.
- In `generated_standard_staff_quarter_note.pdf`, 2 `quarter_note_candidate` and 8 `flag_candidate` records were produced with populated identities and bboxes.
- In `generated_standard_staff_complex_cluster.pdf`, 1 `beam_candidate` and 0 `quarter_note_candidate` records were produced.
- **Beam evidence is absent:** There is no public fixture evidence containing both `quarter_note_candidate` and `beam_candidate` on the same staff.
- **Flag evidence is ambiguous:** Existing flag evidence appears synthetic/geometric rather than sufficient realistic eighth-note geometry.
- `staff_space` is not surfaced in generic `read_only_recognition_outcomes`. A future join rule cannot rely on "1.0 staff space" unless that value is explicitly exposed or the rule strictly uses existing geometry fields.

## Conclusion
Product Task 143 is complete. It produced no product implementation.
Implementing `eighth_note_candidate` is blocked by insufficient public fixture evidence. Staff identity and bbox fields exist, but they are not enough without realistic fixture evidence to define a robust join boundary.

## Authorisation
Product Task 145 is authorised as a prerequisite fixture task.
**Explicit constraint:** Product Task 145 must NOT implement `eighth_note_candidate` reporting. It is strictly limited to adding generated public fixture coverage for eighth-note geometry.
