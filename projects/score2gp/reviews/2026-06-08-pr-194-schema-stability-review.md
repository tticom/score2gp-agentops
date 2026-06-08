# ScoreToGP PR Review: Diagnostics Schema Stability (PR #194)

**Durable Record Path**: `projects/score2gp/reviews/2026-06-08-pr-194-schema-stability-review.md`
**Reviewer ID**: `score2gp-reviewer`
**Target Commit**: `HEAD of feature/diagnostics-schema-stability-v0.1`

---

## 1. Executive Summary

- **Status**: `Needs Changes`
- **Merge Recommendation**: `Do Not Merge`
- **One-Sentence Reason**: The implementation correctly adds the explicit version contract, but relies on an existing weak test for the semantic firewall that only checks a sub-component rather than the top-level schema.

---

## 2. Review Dimensions

### Semantic Firewall Constraint
- **Status**: `Weak Evidence`
- **Analysis**: The task requires ensuring "no music theory terminology bleed" and that `test_schema_does_not_contain_semantic_names` continues to pass. While the test does pass, it currently only calls `StaffLeftMarginAggregateDiagnostics.model_json_schema()`. Because PR #194 introduces versioning at the `NotationStaffDiagnostics` root level, the semantic firewall test MUST assert against the top-level `NotationStaffDiagnostics.model_json_schema()`. Testing only the left-margin sub-component provides incomplete evidence that the rest of the schema (including the new `contract_version` literal) is free of semantic terminology.

### Test Quality and Schema Validation
- **Status**: `Verified`
- **Analysis**:
  - The developer successfully added `contract_version: Literal["notation-diagnostics.v0.1"] = "notation-diagnostics.v0.1"` to `NotationStaffDiagnostics`.
  - The developer appropriately updated tests across `test_pdf_staff_geometry_diagnostics.py`, `test_pdf_staff_primitive_clustering.py`, and `test_pdf_staff_left_margin_diagnostics.py` to assert `contract_version == "notation-diagnostics.v0.1"`.
  - The literal acts as a frozen version identifier successfully.

---

## 3. Required Fixes

To merge this PR, the developer must:
1. Elevate or expand `test_schema_does_not_contain_semantic_names` (currently in `tests/test_pdf_staff_left_margin_diagnostics.py`) to validate the top-level `NotationStaffDiagnostics.model_json_schema()` instead of just `StaffLeftMarginAggregateDiagnostics`. This guarantees that NO child components or version literals leak semantic terminology like "clef", "pitch", "duration", etc.

## 4. Suggested Next Steps
- Implement the required fix to the semantic test and update the PR for re-review.
