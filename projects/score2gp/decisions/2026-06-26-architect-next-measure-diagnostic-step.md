# Architect Decision: Next Measure-Level Diagnostic Step

**Date:** 2026-06-26
**Status:** Outcome A Selected
**Authorised Next Role:** Reviewer (Architecture Verification)
**Developer Implementation:** Not authorised

## Baseline Evidence
- **Governance baseline:** PR #219 (merge commit `5efc2ada7b2a39c3ae76f60038e608209e91529b`)
- **Product PR #328 final head:** `c38c0714ffbc950b7248974d55ed29d3aada5bc0`
- **Product PR #328 merge commit:** `0492612bafebe857c5d136c2911acb1bf4d9323d`
- **Tests verified:**
  - 9 candidate-measure tests passed
  - 5 measure-grid tests passed
  - 3 note-candidate identity tests passed

## Verified Capabilities (Facts)
- The read-only diagnostic assignment assigns candidates to specific `measure_region_index` bounds.
- Unsafe edge cases are explicitly trapped as `identity_none`, `staff_unmatched`, `out_of_bounds`, and `boundary_ambiguous`.
- Page-level measure grid failures properly halt assignment to prevent silent `staff_unmatched` output.
- Each `assigned` candidate includes `center_x` and `candidate_bbox` for localized spatial grouping.

## Inferences
- Since valid candidates are firmly anchored to a validated measure region (via `measure_region_index` and staff/system identifiers), we can safely group them into "measure buckets".
- `center_x` provides a deterministic basis for left-to-right visual geometric sorting within that bucket.

## Hypotheses
- We can define a `MeasureBucket` diagnostic model that consumes the flat `CandidateToMeasureAssignment` array and outputs a structured hierarchy (Page -> System -> Staff -> Measure -> Ordered Candidates).
- This sorting and grouping is purely spatial/geometric and does not require semantic pitch, rhythm, or duration inference.

## Unknowns
- Whether overlapping geometries (e.g., chords) perfectly sort left-to-right without tie-breaking heuristics, though geometric centers suffice for a baseline diagnostic.
- Whether public fixtures have sufficiently complex candidate density to stress-test sorting rules, though mock injection can continue to fill gaps.

## Risks
- Ordering candidates by `center_x` might be mistaken for sequential playback time (rhythm). We must explicitly constrain the next task as *geometric* ordering, not *rhythmic* ordering.
- Developer implementation could overstep into ScoreIR/GP output generation. The task must be strictly bounded to diagnostic JSON models.

## Decision: Outcome A
**Measure-local candidate ordering / measure-bucket diagnostic is viable using current public-fixture evidence, and a bounded Developer diagnostic task can be proposed later.**

### Proposed Next Developer Task (Pending Authorisation)
- **Goal:** Implement a read-only `MeasureBucketDiagnostics` layer.
- **Input:** Output from `extract_candidate_measure_assignment_diagnostics_dict`.
- **Output:** A nested dictionary grouping `assigned` candidates into `MeasureBucket` objects, sorted internally by `center_x`.
- **Success Statuses:** `pass`
- **Failure Statuses:** Inherit failures from upstream (e.g., `measure_grid_diagnostics_failed`, `notation_diagnostics_failed`), plus a distinct bucket failure if data is fundamentally corrupted.
- **Stop/Pivot conditions:** Stop if grouping requires semantic inference (e.g., parsing stems/flags) or if sorting fundamentally breaks on standard notation public fixtures.
- **Non-Goals:** Rhythmic inference, duration inference, ScoreIR compilation, GP export, whole-note semantic recognition.

## Required Next Review
- **Reviewer architecture verification** of this decision.
- Developer implementation remains strictly blocked until governance explicitly authorises the implementation task.
