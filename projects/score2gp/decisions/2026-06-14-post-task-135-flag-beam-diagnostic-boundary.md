# Decision: Authorise generic flag/beam candidate reporting (Post-Task 135)

## Product Task 135 Completion Summary
Product Task 135 was successfully completed. It implemented diagnostic-only flag and beam candidate models and extraction logic based strictly on geometric heuristics. The newly extracted models were stored safely within notation diagnostics.

* **Product PR #272 URL**: https://github.com/tticom/score2gp/pull/272
* **Final head SHA**: `b3e6746c4e876afb8ad1cad51cb8cb7927ed36be`
* **Merge commit SHA**: `3f4848daa821516663e183f490a4127fdd67f6d9`
* **Changed files**:
  * `src/score2gp/pdf_staff_geometry.py`
  * `src/score2gp/pdf_staff_notation_diagnostics.py`
  * `tests/test_pdf_staff_geometry_diagnostics.py`
  * `fixtures/public/pdf_staff_geometry_diagnostics_schema.json`
  * `fixtures/public/expected_diagnostics_complex_cluster.json`
  * `fixtures/public/expected_diagnostics_dense_margin.json`
  * `fixtures/public/expected_diagnostics_negative_blank.json`
  * `fixtures/public/expected_diagnostics_sparse.json`
  * `fixtures/public/expected_diagnostics_wide_curves.json`
* **Checks status**: CI and Raster Diagnostics Gate Advisory passed successfully.
* **User-visible capability status**: Score2GP currently reports read-only candidate evidence for `whole_note_candidate`, `half_note_candidate`, `quarter_note_candidate`, `x_aligned_cluster_candidate`, and `left_margin_candidate`.
* **Explicit statement that flag/beam support is currently diagnostic-only**: Flag/beam support is currently diagnostic-only.
* **Explicit statement that generic `note-candidate-recognition` exposure is not yet present**: Generic `note-candidate-recognition` exposure is not yet present.
* **Explicit statement that no eighth-note recognition was added**: No eighth-note recognition was added.
* **Explicit statement that current recognition remains read-only candidate evidence only**: Current recognition remains read-only candidate evidence only.
* **Known limitations**: Beam and flag detection remains geometry-only and entirely internal to diagnostics. There is no public candidate boundary exposed for them yet.

## Codex Comment Disposition
* Codex identified snapshot regeneration as required.
* The issue was accepted as already fixed after public expected diagnostics snapshots were regenerated.
* A direct inline reply was made.
* The Codex thread was resolved.
* Final CI and Raster Diagnostics Gate Advisory checks passed.

## Supervisor Review Disposition
* Supervisor review identified over-broad beam detection.
* The issue was accepted as a blocker.
* Square/near-square rectangles were being emitted as beam candidates.
* The fix tightened `rect` beam classification to require wide, shallow geometry.
* Regression test `test_square_rectangles_not_emitted_as_beams` was added.
* Public complex-cluster snapshot was updated to remove the 8×8 square rectangle false positives.
* Final checks passed.
