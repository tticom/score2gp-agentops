# Developer Task: Diagnostics Schema Stability and Versioning

**Role:** Developer
**Context:** Following PR #192 and PR #193, we introduced `XAlignedClusterAggregateDiagnostics` and `StaffLeftMarginAggregateDiagnostics` into `NotationStaffDiagnostics`. While the semantic strictness of these structures has been verified, they currently lack explicit versioning contracts.

## Objective
Establish a formal schema versioning strategy for the new geometry diagnostics components (`pdf_staff_geometry.py`) to ensure future primitive expansions or algorithm adjustments do not silently break down-stream expectations (e.g. rhythm inference).

## Requirements

1. **Investigate Versioning Strategy:**
   - Review current structures in `src/score2gp/pdf_staff_geometry.py`.
   - Propose an explicit versioning field (e.g. `schema_version`) for `NotationStaffDiagnostics` or its sub-components.

2. **Implement Schema Versioning:**
   - Add a frozen version literal to `NotationStaffDiagnostics` (e.g. `contract_version = "notation-diagnostics.v0.1"`).
   - Update tests in `test_pdf_staff_geometry_diagnostics.py`, `test_pdf_staff_primitive_clustering.py`, and `test_pdf_staff_left_margin_diagnostics.py` to assert the presence of this explicit schema version.

3. **No Semantic Bleed:**
   - Ensure `test_schema_does_not_contain_semantic_names` continues to pass. 
   - No music-theory terminology (clef, pitch, duration) should be introduced during this versioning upgrade.

## Acceptance Criteria
- [ ] `pdf_staff_geometry.py` includes a definitive schema version literal for standard-staff geometry diagnostics.
- [ ] Downstream tests validate the presence and correctness of this schema version.
- [ ] No regression in existing geometry tests.
- [ ] The schema continues to exclude semantic terminology.
- [ ] The changes are isolated to a new branch, ready for review.

## Stop Conditions
- Do **not** attempt to consume these diagnostics for timing inference yet. This task is strictly about schema stability.
- Do **not** apply versioning to the legacy `build_ir` ascii-timing paths, limit scope to the standard notation geometry diagnostics.
