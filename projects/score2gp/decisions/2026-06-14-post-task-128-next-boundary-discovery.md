# 2026-06-14 Post-Task 128: Next Candidate Boundary Discovery

## Product Task 128 Summary
Product Task 128 was a discovery-only task executed in `tticom/score2gp` to identify the next safe, primitive-derived candidate-evidence boundary after quarter notes.

* **Outcome:** Outcome A (Safe next boundary is already supported by existing diagnostics and fixtures).
* **Code Changes:** No product PR was opened, no product files were changed, and no commits were made.

## Verified Product Evidence

1. **x-aligned clusters**:
   * The current `NotationStaffDiagnostics` schema explicitly defines `x_aligned_cluster_candidates`.
   * `XAlignedPrimitiveClusterCandidate` is fully defined as a schema in `pdf_geometry_candidates.py`.
   * `build_notation_diagnostics` (in `pdf_staff_notation_diagnostics.py`) extracts `x_aligned_cluster_candidates` from existing grouping diagnostics.
   * Public snapshots, specifically `fixtures/public/expected_diagnostics_complex_cluster.json`, contain populated lists for `x_aligned_cluster_candidates`.
2. **left-margin candidates**:
   * `left_margin_candidates` are also explicitly defined and populated in the aforementioned schema, model, logic, and fixtures, but are not authorised for the immediate next implementation task.
3. **Eighth notes, rests, and beam-spanning**:
   * Extensive grep searches (`grep -riE "eighth|rest|beam"`) across source code, diagnostic builders, and test fixture generators confirm that no code or models classify eighth notes, rests, or horizontally spanning beams. Existing grouping (`cluster_x_aligned_primitives`) focuses strictly on vertically aligned elements within a narrow column, meaning beaming across clusters is unsupported.
   * Eighth-note, rest, and beam-spanning recognition boundaries are not currently safe to authorise without precursor diagnostic tasks.

## Authorisation
We recommend and authorise **Product Task 130** to expose the already-supported `x_aligned_cluster_candidates` through the generic read-only `note-candidate-recognition` reporting path. This continues the approach of building stable evidence seams from existing diagnostics without premature musical inference.
