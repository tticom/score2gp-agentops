# Decision: Post-Task 124 Filled/Stemmed Notehead Diagnostics

## Context
Product Task 124 was completed to add read-only diagnostic support for filled/stemmed notehead candidates. The task was recorded in Product PR #268.

* **Product PR URL:** https://github.com/tticom/score2gp/pull/268
* **Final Head SHA:** `24180b0ca3515ccff92800d992b5174466777556`
* **Merge Commit SHA:** `1a0dda116c26a517c64e5052b2b48f6c6f759cfe`
* **Checks Status:** All checks passed successfully.

### Changed Files
* `fixtures/public/expected_diagnostics_complex_cluster.json`
* `fixtures/public/expected_diagnostics_dense_margin.json`
* `fixtures/public/expected_diagnostics_negative_blank.json`
* `fixtures/public/expected_diagnostics_negative_noise.json`
* `fixtures/public/expected_diagnostics_negative_tab.json`
* `fixtures/public/expected_diagnostics_sparse.json`
* `fixtures/public/expected_diagnostics_wide_curves.json`
* `fixtures/public/generated_standard_staff_quarter_note.json`
* `fixtures/public/pdf_staff_geometry_diagnostics_schema.json`
* `src/score2gp/pdf_staff_geometry.py`
* `src/score2gp/pdf_staff_notation_diagnostics.py`
* `tests/fixtures/pdf/generated_standard_staff_quarter_note.pdf`
* `tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py`
* `tests/test_pdf_standard_staff_diagnostics_fixtures.py`

## Outcomes
* The diagnostic-only capability is now available. `quarter_note_candidates` exists as diagnostic evidence only.
* Product-facing quarter-note reporting was intentionally not added in Product Task 124.
* Existing `whole_note_candidate` and `half_note_candidate` reporting remains preserved.
* The reporting paths `score2gp note-candidate-recognition`, `score2gp whole-note-recognition`, and `scripts/note_candidate_recognition_report.py` remain preserved and unmodified.

## Codex Comment Disposition
* Codex asked to include quarter notes in recognition outputs.
* The comment was rejected as out of scope for Product Task 124.
* The rationale: Product Task 124 authorised diagnostic-only filled/stemmed notehead support, not product-facing quarter-note recognition/reporting. Quarter-note recognition/reporting requires separate governance authorisation.
* Direct inline replies were made.
* The Codex inline thread was resolved before merge.
