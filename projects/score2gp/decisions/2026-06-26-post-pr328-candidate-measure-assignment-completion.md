# Post-PR #328 Candidate-to-Measure Assignment Completion

**Date:** 2026-06-26
**Status:** Completed
**Authorised Next Role:** Architect
**Developer Implementation:** Not authorised

## Summary
Product PR #328 has been successfully merged, establishing the read-only candidate-to-measure diagnostic assignment capability.

## Product PR #328 Record
- **URL:** https://github.com/tticom/score2gp/pull/328
- **Final Merged Head SHA:** `c38c0714ffbc950b7248974d55ed29d3aada5bc0`
- **Merge Commit:** `0492612bafebe857c5d136c2911acb1bf4d9323d`
- **Exact product files changed:**
  - `src/score2gp/pdf_staff_geometry.py`
  - `src/score2gp/pdf_staff_notation_diagnostics.py`
  - `tests/test_pdf_candidate_measure_assignment.py`

## Final Capability Summary
- Added read-only candidate-to-measure diagnostic assignment.
- Diagnostic models: `CandidateToMeasureAssignment` and `CandidateMeasureAssignmentDiagnostics`.
- Output statuses: `assigned`, `identity_none`, `staff_unmatched`, `out_of_bounds`, `boundary_ambiguous`.

### Final Codex-driven Fix
- Page-level measure-grid failures are properly honoured.
- If the corresponding measure-grid page has `status == "fail"` or `status == "unsupported"`, assignment diagnostics now safely return `{"assignments": [], "diagnostic_status": "fail", "failure_reasons": ["measure_grid_diagnostics_failed"]}` to prevent missing regions from being misclassified as `staff_unmatched`.

## Validation Evidence
- `pytest tests/test_pdf_candidate_measure_assignment.py`: 9 passed
- `pytest tests/test_pdf_measure_grid_diagnostics.py`: 5 passed
- `pytest tests/test_pdf_note_candidate_identity.py`: 3 passed
- Artifact hygiene was verified clean.

## Known Limitations
- Candidate identity remains geometric and heuristic.
- Mock injection is used where public fixtures lack real notation candidates.
- Diagnostic assignment is not rhythm, duration, note semantics, ScoreIR, or GP export.
- **Stale PR Body Caveat:** Product PR #328 body is stale relative to final merge state because it still records earlier conformance approval for head SHA `7abd7e995ddee0b6ca6ca9fdaca0746a993a6f00` and `8 passed`. This governance record captures the corrected final state (`c38c0714ffbc950b7248974d55ed29d3aada5bc0`, 9 tests).

## Authorised Next Task: Architect Decision
Authorise Architect to answer this bounded question:

Can the current read-only diagnostic evidence support a safe next product step that produces new decision-useful evidence beyond candidate-to-measure assignment?

The Architect must choose exactly one outcome:
- **Outcome A:** measure-local candidate ordering / measure-bucket diagnostic is viable using current public-fixture evidence, and a bounded Developer diagnostic task can be proposed later.
- **Outcome B:** current evidence is insufficient for measure-local ordering, but a smaller diagnostic/evidence task is viable and should be proposed.
- **Outcome C:** current evidence is insufficient and no further Developer task is authorised without a new approach or pivot.

The Architect must not authorise implementation. Architecture verification is required next.

## Required Next Review
- PR readiness review for this governance PR.
- After merge, Architect decision task.
