# Post Geometry Candidate Backlog Refresh

Date: 2026-07-08
Task: Req-117 / Task 35
Role: Orchestrator

## Decision

Set Req-118 / Task 37, `Populate page-level geometry candidate export`, as the next active Developer task.

## Rationale

Req-110 / Task 33 was completed in governance PR #260. The review approved the semantic-free geometry boundary but found a concrete product gap: diagnostic candidate fields can be populated, yet the page-level `geometry_candidates` export still serializes empty `GeometryCandidateSet` payloads.

Moving directly to semantic boundary research would force the Architect to choose between two candidate surfaces:

- populated `NotationStaffDiagnostics.left_margin_candidates` and `NotationStaffDiagnostics.x_aligned_cluster_candidates`;
- empty `inspect_pdf()["pages"][...]["geometry_candidates"]` payloads.

Task 37 resolves that ambiguity with a small product implementation and measurable tests before semantic research resumes.

## Queue Changes

- Marked Task 33 done after PR #260 merged.
- Marked Task 35 done by this refresh.
- Marked Task 36 done because product PR #345 exposed primitive geometries.
- Blocked Task 34 until Task 37 settles the export boundary.
- Added Req-118 / Task 37 and made it the active task.

## Next Autonomous Action

Developer should implement Task 37 in `tticom/score2gp` on branch `feature/populate-geometry-candidate-export-v0.1`, then open a product PR with test and artifact-audit evidence.
