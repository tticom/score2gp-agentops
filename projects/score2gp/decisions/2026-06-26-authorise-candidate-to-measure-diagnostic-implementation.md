# 2026-06-26 Governance: Authorise Candidate-to-Measure Diagnostic Implementation

## Context
Score2GP has now approved an architecture for read-only candidate-to-measure diagnostic assignment.

Baseline chain:
- **Product PR #326**: Merged measure-grid diagnostics with commit `7565e751e0dea624a209aeb4233373338296262a`.
  - Capability: read-only measure-grid diagnostics with measure regions exposing `start_x` and `end_x`.
- **Product PR #327**: Merged nullable heuristic candidate identity diagnostics with commit `963bbf393bc5e619e30d82ebff22652c1a94615a`.
  - Capability: notation candidate diagnostics expose nullable `page_index`, `system_index`, and `staff_index`.
  - Limitation: identity is nearest-staff-center heuristic evidence, not true extraction-context preservation.
- **Governance PR #216**: Merged architecture-decision authorisation with commit `60cfee91a2134c4a591efde149f5606550ae258b`.
  - Authorised Architect research/decision.
- **Architecture PR #217**: Merged approved Outcome A architecture with commit `93b9e2e37220195def5bc3cc213a2510fa9744b8`.
  - Approved head SHA: `624e4da25dbf7dd4f7891c22b2a5dbd2f775a928`.
  - Outcome: Outcome A approved.
  - Decision: candidate-to-measure diagnostic assignment is viable as a bounded read-only diagnostic architecture.
  - Developer implementation was not authorised by PR #217 itself.

## Goal
Update governance state to authorise Developer implementation of a read-only candidate-to-measure diagnostic assignment array in `tticom/score2gp`.

## Non-goals
Do not authorise:
- ScoreIR changes;
- GP export changes;
- rhythm/duration inference;
- whole-note recognition;
- note/rest semantic recognition;
- MusicXML changes;
- OCR;
- ML/training;
- tab-only timing changes;
- private fixture usage;
- generated artifact commits;
- changes to conversion output semantics.

## Developer Implementation Contract
Authorise Developer to implement **only**:
A read-only diagnostic array that maps notation candidates to measure-grid regions using the approved Outcome A rule.

The implementation must:
- Use existing candidate diagnostics with `bbox`, `page_index`, `system_index`, and `staff_index`.
- Use existing measure-grid staff/region diagnostics.
- Compute candidate `center_x` from `bbox`.
- Match page/system/staff identity exactly.
- Assign only when exactly one measure region safely matches.
- Preserve unassigned/ambiguous candidates with explicit statuses.
- Avoid ScoreIR, GP export, rhythm, duration, semantic note/rest recognition, MusicXML, OCR, ML/training, and tab-only timing changes.

### Required Statuses
- `assigned`
- `identity_none`
- `staff_unmatched`
- `out_of_bounds`
- `boundary_ambiguous`

### Required Boundary Rules
- `MEASURE_BOUNDARY_TOLERANCE_PT = 1.0`
- reject out-of-bounds before boundary checks;
- internal boundaries within tolerance produce `boundary_ambiguous`;
- use half-open intervals for non-final regions: `start_x <= center_x < end_x`;
- use closed interval for final region: `start_x <= center_x <= end_x`;
- zero or multiple matches produce `boundary_ambiguous`.

## Required Developer Tests
The Developer implementation must include tests proving:
- single-staff quarter-note assignment on approved public fixture;
- ledger-line candidate assignment to a measure;
- double/repeat adjacent barline fixture does not create false/empty assignment regions;
- `identity_none` status when candidate identity is missing;
- `staff_unmatched` status when candidate identity has no matching measure-grid staff;
- `out_of_bounds` status when `center_x` is outside measure-grid bounds;
- `boundary_ambiguous` status when `center_x` is within `MEASURE_BOUNDARY_TOLERANCE_PT` of an internal boundary;
- multi-staff routing using mock drawing-path injection near, but not exactly on, public fixture staff centers because `generated_standard_staff_multi_staff.pdf` lacks real note candidates;
- no ScoreIR changes;
- no GP export changes;
- no rhythm/duration inference;
- no note/rest semantic recognition changes.

## Next Review
After Developer implementation completes, the next required review is Reviewer implementation conformance review.
