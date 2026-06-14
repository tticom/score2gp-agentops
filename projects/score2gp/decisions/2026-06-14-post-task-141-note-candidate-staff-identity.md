# 2026-06-14 Post-Task 141 Note Candidate Staff Identity

## Context
Product Task 141 added safe staff/system identity to generic whole, half, and quarter note candidate evidence. This completes the prerequisite for testing a staff-local composition join with flag/beam evidence.

## Completion Summary
* **Product PR**: [PR #274](https://github.com/tticom/score2gp/pull/274)
* **Final Head SHA**: `b82c9a1b0b37d5f55319bda9ef17c63dd5c02c6d`
* **Merge Commit SHA**: `7f859b44d546df8c4156cbaf8d50c0e2f91601d2`

## Changed Files
* `fixtures/public/generated_standard_staff_half_note.json`
* `fixtures/public/generated_standard_staff_quarter_note.json`
* `fixtures/public/generated_standard_staff_whole_note.json`
* `src/score2gp/whole_note_recogniser.py`
* `tests/fixtures/pdf/generated_standard_staff_half_note.pdf`
* `tests/fixtures/pdf/generated_standard_staff_quarter_note.pdf`
* `tests/fixtures/pdf/generated_standard_staff_whole_note.pdf`
* `tests/test_note_candidate_recognition_cli.py`
* `tests/test_note_candidate_recognition_report.py`
* `tests/test_whole_note_recognition_cli.py`

## Checks Status
* **CI**: success
* **Raster Diagnostics Gate Advisory**: success

## User-Visible Capability
Whole, half, and quarter generic note candidates now include staff/system identity (`system_index` and `staff_index`). Staff association is explicitly bounded by both vertical and horizontal compatibility to safely prevent false identity assignment to artifacts outside the staff bounds.

`eighth_note_candidate` reporting was **not** added. Eighth-note recognition was **not** implemented.

## Known Limitations
* The product still lacks `eighth_note_candidate` reporting, eighth-note recognition, pitch inference, rest reporting, rhythm inference, ScoreIR, MusicXML, GP output, OCR, and full notation recognition.

## Codex Comment Disposition
* Codex identified vertical-only staff association as unsafe.
* The issue was accepted as a blocker.
* The fix added horizontal staff-bound compatibility before assigning staff identity.
* Regression test `test_associate_staves_horizontal_boundary` was added.
* Direct inline reply was made.
* The Codex thread was resolved.
* Final CI and Raster Diagnostics Gate Advisory checks passed.

## Authorisation
The following product task is authorised for execution:

**Product Task 143 — Discover safe eighth-note candidate composition rule**

This task is discovery-only. It must inspect whether current generic note candidates plus flag/beam candidates can now support a conservative `eighth_note_candidate` composition rule from existing evidence without semantic overreach.
