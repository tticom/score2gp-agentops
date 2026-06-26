# 2026-06-26 Architecture Decision: Candidate-to-Measure Assignment Viability

## Context
Score2GP has completed the previous diagnostic loops:
- **Product PR #326**: Merged `7565e751e0dea624a209aeb4233373338296262a`, providing read-only measure-grid diagnostics (`start_x`, `end_x`).
- **Architecture PR #214**: Concluded measure-grid was insufficient alone because notation candidates lacked staff identity.
- **Governance PR #215**: Authorised a Developer diagnostic task.
- **Product PR #327**: Merged `963bbf393bc5e619e30d82ebff22652c1a94615a`, adding nullable heuristic `page_index`, `system_index`, and `staff_index` to candidate diagnostics via nearest-staff-center distance.
- **Governance PR #216**: Merged `60cfee91a2134c4a591efde149f5606550ae258b`, blocking Developer implementation and setting this architecture research gate.

## Blocker
Can Score2GP safely and deterministically assign notation candidates to measure regions using PR #326 measure grids and PR #327 heuristic identity?

## Fact, Inference, Hypothesis, Unknown, Risk
- **Fact**: Notation candidates possess a `bbox` and optional heuristic `staff_index`, `system_index`, `page_index`.
- **Fact**: `MeasureGridStaff` divides a staff into `MeasureGridRegion`s with `start_x` and `end_x`.
- **Fact**: Double/repeat adjacent barlines are already collapsed by PR #326.
- **Fact**: The identity assignment in PR #327 successfully handles ledger lines and multi-staff proximity (proven by `tests/test_pdf_note_candidate_identity.py`).
- **Inference**: A candidate's geometric horizontal center (`(bbox[0] + bbox[2]) / 2.0`) can be checked against `start_x` and `end_x` of the measure regions.
- **Hypothesis**: Candidates can be safely assigned to measures purely geometrically without needing semantic note/rest recognition.
- **Unknown**: Exact behaviour of highly ambiguous candidates exactly on a barline in complex scanned scores.
- **Risk**: The heuristic identity is nullable and not true extraction-context preservation, meaning it could fail or return `None` in extreme layouts or overlapping staves.

## Chosen Outcome
**Outcome A: Viable architecture using current evidence.**

Current evidence (measure-grid regions + nullable heuristic staff identity) supports a deterministic, read-only, candidate-to-measure assignment architecture.

### 1. Deterministic Assignment Rule
- **Filter**: Discard or mark as `ambiguous_identity` any candidate with `page_index=None`, `system_index=None`, or `staff_index=None`.
- **Match Staff**: Locate the `MeasureGridStaff` with the matching `page_index`, `system_index`, and `staff_index`. If no such staff grid exists, mark as `unmatched_staff`.
- **Locate Center**: Compute `center_x = (candidate.bbox[0] + candidate.bbox[2]) / 2.0`.
- **Assign to Region**: Find the `MeasureGridRegion` within the staff where `start_x <= center_x <= end_x`.
- **Handle Boundaries**: If `center_x` is outside the bounds of the first or last measure, or falls into a gap between regions, mark as `out_of_bounds`. If `center_x` is within a tiny tolerance (e.g., `< 1.0` units) of a region boundary and overlaps two regions, mark as `boundary_ambiguous`.

### 2. Ambiguity and Failure Rules
Any candidate failing the assignment rule is preserved but marked with an explicit failure reason:
- `identity_none`
- `staff_unmatched`
- `out_of_bounds`
- `boundary_ambiguous`

This ensures no unsafe assumptions or forced assignments occur.

### 3. Identity Limitations
The heuristic nearest-staff-center distance is acceptable because any candidate that is truly ambiguous between staves will eventually be caught by subsequent rhythm-validation layers (which are out of scope for now). The assignment explicitly respects `None` and does not attempt to guess context if the distance heuristic fails to run.

### 4. Edge Cases Handled
- **Multi-staff**: Handled by matching `staff_index` and `system_index`.
- **Ledger-lines**: PR #327 proven to assign correct staff identity for ledger-line notes.
- **Double/repeat adjacent barlines**: PR #326 proven to collapse these, so they do not produce false empty regions.

### 5. Required Fixture Evidence & Tests
Before any Developer implementation is merged, the following test coverage is required:
- `generated_standard_staff_quarter_note.pdf`: Ensure single staff quarter note assignment.
- `generated_standard_staff_multi_staff.pdf`: Ensure notes on different staves are assigned to the correct staff's measure grid.
- `generated_standard_staff_ledger_lines.pdf`: Ensure ledger line notes are assigned to the correct measure.
- `generated_paired_notation_tab_system_double_barline.pdf`: Ensure double barlines don't cause candidate assignment ambiguity.

### 6. Explicit Boundaries and Non-Goals
This architecture authorises **only** a read-only diagnostic array mapping candidate bounding boxes to measure region indices.
It **does not** authorise:
- rhythm/duration inference;
- whole-note vs quarter-note semantics;
- note/rest semantic recognition;
- ScoreIR changes;
- GP export changes;
- MusicXML changes;
- ML/training.

## Next Review
Developer implementation is **not authorised** until Reviewer architecture verification approves this Outcome A.
