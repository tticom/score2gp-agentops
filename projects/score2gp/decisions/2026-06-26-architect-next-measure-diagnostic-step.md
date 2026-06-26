# Architect Decision: Next Measure-Level Diagnostic Step

**Date:** 2026-06-26
**Status:** Outcome A Selected (Revised)
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
- `center_x` provides a deterministic basis for left-to-right visual geometric sorting within that bucket, provided candidates do not overlap or share near-identical X coordinates.

## Hypotheses
- We can define a `MeasureBucket` diagnostic model that consumes the flat `CandidateToMeasureAssignment` array and outputs a structured hierarchy (Page -> System -> Staff -> Measure -> Ordered Candidates).
- This sorting and grouping is purely spatial/geometric and does not require semantic pitch, rhythm, or duration inference.

## Unknowns
- Whether public fixtures have sufficiently complex candidate density to stress-test sorting rules, though mock injection can continue to fill gaps.

## Risks
- Ordering candidates by `center_x` might be mistaken for sequential playback time (rhythm). We must explicitly constrain the next task as *geometric* ordering, not *rhythmic* ordering.
- Developer implementation could overstep into ScoreIR/GP output generation. The task must be strictly bounded to diagnostic JSON models.
- Assuming deterministic semantic tie-breakers for chord-like/overlapping candidates is unsafe. We must explicitly trap ties/overlaps as ambiguous instead of silently misordering them.

## Decision: Outcome A
**Measure-local candidate ordering / measure-bucket diagnostic is viable using current public-fixture evidence, and a bounded Developer diagnostic task can be proposed later.**

### Proposed Next Developer Task (Pending Authorisation)
- **Goal:** Implement a read-only `MeasureBucketDiagnostics` layer.
- **Input:** Output from `extract_candidate_measure_assignment_diagnostics_dict`.
- **Included Candidates:** Only candidates with `assignment_status == "assigned"`.
- **Excluded Candidates:** Unassigned candidates remain in upstream assignment diagnostics and are not silently bucketed.
- **Grouping Keys:** `page_index`, `system_index`, `staff_index`, `measure_region_index`.
- **Bucket Output Fields:** `page_index`, `system_index`, `staff_index`, `measure_region_index`, `bucket_status`, `ordered_candidates`, `candidate_count`, `failure_reasons`.
- **Candidate Fields Retained:** `candidate_type`, `candidate_bbox`, `center_x`, and original assignment identity fields.
- **Empty Bucket Handling:** Valid measure regions with no assigned candidates emit `bucket_status == "empty"`.
- **Upstream Failure Handling:** If candidate-to-measure diagnostics fail, `MeasureBucketDiagnostics` returns `diagnostic_status == "fail"` with inherited failure reasons and no buckets.
- **Sorting Rule:** Primary sort by `center_x`. Only claim bucket status `ordered` if adjacent sorted candidates differ by more than `CENTER_X_TIE_TOLERANCE_PT` (e.g., 0.5pt).
- **Ambiguity Rule:** Equal/near-equal `center_x` produces `bucket_status == "center_x_ambiguous"`. Chord-like/overlapping same-center candidates are treated as `center_x_ambiguous`. A deterministic fallback order (e.g. `center_x`, `candidate_bbox[1]`, `candidate_bbox[0]`, `candidate_type`, original input index) must be used for inspection stability only, but must not be claimed as meaningful order.
- **Non-Goals:** Rhythmic inference, duration inference, playback order, ScoreIR compilation, GP export, whole-note semantic recognition.
- **Fixture/Test Plan:**
  - Single-staff quarter-note fixture: assigned candidates bucketed and ordered.
  - Ledger-line fixture: candidates bucketed without staff identity regression.
  - Multi-staff mock injection: candidates grouped by staff and measure.
  - Double-barline fixture: no false empty split or boundary ambiguity.
  - `center_x_ambiguous` mock injection: equal/near-equal center_x candidates produce safe ambiguity.
  - Upstream page-level grid failure mock: inherited failure.
- **Stop/Pivot Conditions:** Stop if ordering requires stem/beam/flag parsing; stop if bucket structure implies rhythm or playback sequence; stop if public fixture/mock evidence cannot prove deterministic grouping and safe ambiguity.

## Required Next Review
- **Reviewer architecture verification** of this revised decision.
- Developer implementation remains strictly blocked until governance explicitly authorises the implementation task.
