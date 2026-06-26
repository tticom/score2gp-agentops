# Active Task

**Task**: Developer Implementation: Read-only StaffPositionDiagnostics
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## 1. Baseline
- Product PR #329 merged read-only MeasureBucketDiagnostics.
- Product PR #329 merge commit: 8af3518633f02cd9bcaf0e1413238eb093513f5e.
- Governance PR #222 merged Supervisor Decision Gate.
- Governance PR #222 merge commit: f10a7f140579ea8bad362d35ec8c6cee271c4760.
- Architect Outcome A for StaffPositionDiagnostics approved by Reviewer architecture verification.

## 2. Authorised Developer Scope
Implement a read-only StaffPositionDiagnostics layer that maps assigned notation candidates from MeasureBucketDiagnostics to staff-relative vertical positions using staff geometry and candidate geometry.

It may:
- consume MeasureBucketDiagnostics output;
- consume PdfStaffNotationGeometryDiagnostics / NotationStaffGeometry;
- derive candidate center_y;
- derive staff_step_index from staff line coordinates and staff spacing;
- classify candidate position as staff-line/space/ledger/outside/ambiguous;
- emit structured JSON diagnostics;
- pass through upstream failures safely.

It must not:
- infer pitch names;
- map G-clef to note names;
- infer key signatures;
- infer rhythm;
- infer duration;
- infer playback order;
- infer musical sequence;
- change ScoreIR;
- change GP export;
- claim whole-note recognition;
- use OCR;
- use MusicXML;
- use ML/training;
- depend on private fixtures.

## 3. Required Diagnostic Contract
**Candidate diagnostic name:**
`StaffPositionDiagnostics`

**Entry point:**
`extract_staff_position_diagnostics_dict(doc, page_index)`
A narrower helper/entry point is acceptable only if it is read-only, production-path compatible, and returns equivalent structured diagnostics.

**Input:**
MeasureBucketDiagnostics
PdfStaffNotationGeometryDiagnostics / NotationStaffGeometry

**Required top-level output fields:**
- `diagnostic_status`
- `positioned_candidates`
- `failure_reasons`

**Required per-candidate fields:**
- `page_index`
- `system_index`
- `staff_index`
- `measure_region_index`
- `candidate_type`
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

**Required candidate statuses:**
- `positioned`
- `ledger_positioned`
- `missing_staff_geometry`
- `outside_staff_bounds`
- `ambiguous_vertical_position`
- `ambiguous_notehead_center`
- `unsupported_candidate_type`
- `upstream_measure_bucket_failed`
- `upstream_assignment_failed`
Status naming can differ only if the same semantics are explicit and tested.

**Required failure reasons include:**
- `missing_staff_lines`
- `malformed_staff_spacing`
- `missing_candidate_bbox`
- `unreliable_candidate_center`
- `unsupported_candidate_type`
- `upstream_measure_bucket_failed`
- `upstream_assignment_failed`

## 4. Center-Y / Notehead-Center Mitigation
For stemmed candidates, full candidate bbox center_y may not equal notehead center_y.

Required mitigation:
- Expose center_y_source.
- Use full_bbox_center only if intentionally chosen and documented.
- Emit ambiguous_notehead_center or ambiguous_vertical_position where centre confidence is insufficient.
- Do not silently claim precise notehead position when evidence is weak.

## 5. Dependency Boundary
The implementation must not import from or depend on:
`src/score2gp/whole_note_recogniser.py`

Allowed approaches:
- extract/refactor a generic staff-position helper into an appropriate generic module;
- or duplicate the algebraic staff-step formula with tests;
- or create a new generic diagnostic module.

The formula may be based on the existing proven mapping:
`(notehead_y - line_y_coords[0]) / (staff_space / 2.0)`

But the future product code must not couple the generic diagnostic to whole-note semantic recognition.

## 6. Clef/G-Clef Boundary
- Staff-relative position does not require clef.
- Semantic pitch requires clef.
- Treble/G-clef may later anchor written pitch by identifying the G line.
- StaffPositionDiagnostics must not claim semantic pitch, sounding pitch, GP note pitch, or string/fret pitch.

## 7. Required Validation
The future Developer PR must include tests proving:
- quarter-note public fixture maps candidates to deterministic staff-relative positions or safe ambiguity statuses;
- half-note public fixture maps candidates to deterministic staff-relative positions or safe ambiguity statuses;
- whole-note public fixture maps candidates to deterministic staff-relative positions or safe ambiguity statuses;
- ledger-line public fixture returns ledger_positioned or equivalent with valid out-of-staff staff_step_index;
- empty buckets from multi-staff fixture pass through safely without exception;
- empty buckets from double-barline fixture pass through safely without claiming candidate splitting;
- upstream MeasureBucketDiagnostics failure returns structured failure;
- unsupported candidate type returns structured status;
- bbox center uncertainty is represented via center_y_source and ambiguity status where applicable;
- no pitch names, rhythm, duration, playback, ScoreIR, or GP output assertions are added.

Required focused test command for future Developer PR:
```bash
.venv/bin/pytest tests/test_pdf_staff_position_diagnostics.py tests/test_pdf_measure_bucket_diagnostics.py tests/test_pdf_candidate_measure_assignment.py tests/test_pdf_measure_grid_diagnostics.py tests/test_pdf_note_candidate_identity.py
```
If the new test file name differs, the PR body must explain why.

## 8. Required Future Reviews
After future Developer PR:
- Reviewer implementation conformance review
- PR readiness review

No merge without both.
