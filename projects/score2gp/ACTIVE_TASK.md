# Active Task

**Task**: Developer Implementation: Read-only MeasureBucketDiagnostics
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## 1. Baseline
- Governance PR #220 merged.
- Merge commit: `3d82f587d57ddf06f2122c13fc5ce9c694b2a332`.
- Approved architecture decision file: `projects/score2gp/decisions/2026-06-26-architect-next-measure-diagnostic-step.md`.
- Product baseline: Product PR #328 merge commit `0492612bafebe857c5d136c2911acb1bf4d9323d`.

## 2. Authorised implementation scope
The future Developer may implement a read-only `MeasureBucketDiagnostics` layer that consumes output from `extract_candidate_measure_assignment_diagnostics_dict`.

It may group only candidates where:
`assignment_status == "assigned"`

It must group by:
`page_index`
`system_index`
`staff_index`
`measure_region_index`

It may expose bucket fields:
`page_index`
`system_index`
`staff_index`
`measure_region_index`
`bucket_status`
`ordered_candidates`
`candidate_count`
`failure_reasons`

It must retain candidate fields needed for diagnostic inspection, including:
`candidate_type`
`candidate_bbox`
`center_x`
original assignment identity fields

## 3. Required statuses
The future Developer task must support:
`ordered`
`empty`
`center_x_ambiguous`
`upstream_failed`

## 4. Safe ambiguity contract
The future Developer must define a fixed `CENTER_X_TIE_TOLERANCE_PT`, for example `0.5`.

A bucket may be marked `ordered` only if adjacent sorted candidates differ by more than the tie tolerance.

Equal or near-equal `center_x` values must produce:
`bucket_status == "center_x_ambiguous"`

Chord-like or overlapping same-center candidates must also produce:
`bucket_status == "center_x_ambiguous"`

A deterministic fallback order may be used only for inspection stability.
Fallback order must not be claimed as musical sequence, rhythm, duration, playback order, or visual truth beyond stable diagnostic display.

## 5. Required validation for future Developer PR
Require at minimum:
- Single-staff quarter-note fixture: assigned candidates bucketed and ordered.
- Ledger-line fixture: candidates bucketed without staff identity regression.
- Multi-staff mock injection: candidates grouped by staff and measure.
- Double-barline fixture: no false empty split or boundary ambiguity.
- `center_x_ambiguous` mock injection: equal or near-equal `center_x` candidates produce safe ambiguity.
- Upstream page-level grid failure mock: inherited failure.
- Existing candidate-to-measure tests remain green.
- Existing measure-grid tests remain green.
- Existing note-candidate identity tests remain green.

## 6. Required next reviews
After this governance PR:
- PR readiness review.

After the future Developer implementation PR:
- Reviewer implementation conformance review.
- PR readiness review.
