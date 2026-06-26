# StaffPositionDiagnostics Architecture Approval and Developer Authorisation

**Date**: 2026-06-26
**Status**: Authorised

## Context
Following the merge of read-only `MeasureBucketDiagnostics` (Product PR #329, Governance PR #222), the Architect reported Outcome A for a subsequent read-only `StaffPositionDiagnostics` capability. Reviewer architecture verification has now approved this baseline.

## Approved Architecture Outcome
A read-only staff-position layer is viable using existing bounding-box and staff-line coordinates, entirely separate from musical semantics or rhythm/playback sequencing.

## Authorised Developer Task
The active governance task is updated to authorise the Developer to implement `StaffPositionDiagnostics`. The new diagnostic will output a `staff_step_index` and associated metadata for assigned notation candidates.

## Key Constraints & Mitigations
- **center_y/notehead-center caveat**: Bounding boxes for stemmed candidates may skew the `center_y`. The Developer implementation must expose `center_y_source` and apply `ambiguous_notehead_center` / `ambiguous_vertical_position` when the exact notehead center cannot be confidently mapped.
- **Dependency block**: The Developer implementation must not import from or depend on `src/score2gp/whole_note_recogniser.py`.
- **Clef/G-clef boundary**: Staff-relative position does not require a clef. Semantic pitch does. `StaffPositionDiagnostics` must not claim semantic pitch.
- **Non-goals**: No final pitch names, no sounding pitch, no rhythm/duration, no ScoreIR changes, no GP export changes. 

## Required Next Steps
- Developer implementation in `tticom/score2gp`.
- Reviewer implementation conformance review.
- PR readiness review.
