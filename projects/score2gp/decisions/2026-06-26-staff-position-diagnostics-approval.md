# StaffPositionDiagnostics Architecture Approval and Developer Authorisation

**Date**: 2026-06-26
**Status**: Authorised

## Context
Following the merge of read-only `MeasureBucketDiagnostics` (Product PR #329, Governance PR #222), the Architect reported Outcome A for a subsequent read-only `StaffPositionDiagnostics` capability. Reviewer architecture verification has now approved this baseline.

## 1. Baseline
- Product PR #329 merged read-only `MeasureBucketDiagnostics`.
- Product PR #329 merge commit: 8af3518633f02cd9bcaf0e1413238eb093513f5e.
- Governance PR #222 merged Supervisor Decision Gate.
- Governance PR #222 merge commit: f10a7f140579ea8bad362d35ec8c6cee271c4760.

## 2. Architect Outcome A Summary
The Architect concluded:
- **Outcome A**: A read-only StaffPositionDiagnostics path is viable using existing staff geometry and candidate geometry.

Concrete evidence basis:
- `NotationStaffGeometry` exposes staff line coordinates / `line_y_coords`.
- `MeasureBucketDiagnostics` exposes assigned candidates grouped by measure.
- `MeasureBucketCandidate` exposes `candidate_bbox` and `center_x`.
- `center_y` can be derived from `candidate_bbox`, but must be treated as source-qualified evidence.
- `staff_step_index` can be computed from staff line coordinates and staff spacing.
- Staff-relative position is geometric and does not require clef.
- Semantic pitch does require clef.

## 3. Reviewer Architecture Verification Summary
Reviewer architecture verification returned:
- **Verdict: approve architecture**

Required reviewer caveats:
- Bbox center may not equal notehead center for stemmed notes.
- `center_y_source` is required.
- `ambiguous_notehead_center` or `ambiguous_vertical_position` is required when centre confidence is insufficient.
- Generic StaffPositionDiagnostics must not import from or depend on `whole_note_recogniser.py`.
- Staff-relative position must remain separate from semantic pitch.
- Treble/G-clef may later anchor written pitch but is not part of this Developer task.

## 4. Approved Developer Scope
Developer is authorised only to implement:
- Read-only `StaffPositionDiagnostics` mapping assigned notation candidates to staff-relative vertical positions.

This is explicitly NOT authorised:
- pitch names;
- G-clef-to-note-name mapping;
- key signatures;
- rhythm;
- duration;
- playback order;
- musical sequence;
- ScoreIR changes;
- GP export changes;
- whole-note recognition claim;
- OCR;
- MusicXML;
- ML/training.

## 5. Diagnostic Contract
Required per-candidate evidence fields:
- `candidate_bbox`
- `center_x`
- `center_y`
- `center_y_source`
- `staff_step_index`
- `nearest_staff_line_index`
- `nearest_staff_space_index`
- `staff_spacing`
- `staff_line_y_coords` or `staff_geometry_id`
- `position_status`
- `failure_reasons`

Required statuses:
- `positioned`
- `ledger_positioned`
- `missing_staff_geometry`
- `outside_staff_bounds`
- `ambiguous_vertical_position`
- `ambiguous_notehead_center`
- `unsupported_candidate_type`
- `upstream_measure_bucket_failed`
- `upstream_assignment_failed`

## 6. Validation Requirements
Future Developer validation scope:
- quarter-note fixture;
- half-note fixture;
- whole-note fixture;
- ledger-line fixture;
- empty multi-staff bucket handling;
- empty double-barline bucket handling without claiming candidate splitting;
- upstream failure handling;
- unsupported candidate handling;
- bbox center uncertainty represented;
- no pitch/rhythm/duration/playback/ScoreIR/GP assertions.

## 7. Required Future Reviews
- Reviewer implementation conformance review
- PR readiness review
