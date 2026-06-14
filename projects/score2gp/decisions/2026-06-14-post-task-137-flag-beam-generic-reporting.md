# Decision: Post Task 137 Flag/Beam Generic Reporting

## Product Task 137 Completion Summary
Product Task 137 successfully exposed diagnostic-derived `flag_candidate` and `beam_candidate` evidence through the generic read-only `note-candidate-recognition` path and through `scripts/note_candidate_recognition_report.py`. 

## Product PR #273 Evidence
* **Product PR URL:** https://github.com/tticom/score2gp/pull/273
* **Final Head SHA:** `a7540997288807f5011c35a148663da77c778088`
* **Merge Commit SHA:** `eddfa3635501ec55d197ffdafb0f55d5a9456527`
* **Changed Files:**
  * `scripts/note_candidate_recognition_report.py`
  * `src/score2gp/cli.py`
  * `src/score2gp/whole_note_recogniser.py`
  * `tests/test_note_candidate_recognition_cli.py`
  * `tests/test_note_candidate_recognition_report.py`
  * `tests/test_whole_note_recognition_cli.py`
* **Checks Status:** Success (CI and Raster Diagnostics Gate Advisory are green).

## User-Visible Capability Now Available
The `score2gp note-candidate-recognition` generic reporting capability now emits:
* `whole_note_candidate`
* `half_note_candidate`
* `quarter_note_candidate`
* `x_aligned_cluster_candidate`
* `left_margin_candidate`
* `flag_candidate`
* `beam_candidate`

**Explicit preservation statements:**
* `flag_candidate` and `beam_candidate` are exposed only as read-only diagnostic-derived evidence.
* The `whole-note-recognition` compatibility output remains preserved and isolated from these candidates.
* No `eighth_note_candidate` reporting was added.
* No eighth-note recognition was implemented.

## Known Limitations
* `eighth_note_candidate` reporting is not yet implemented.
* Eighth-note recognition is not yet implemented.
* Rests, pitch inference, staff-position inference, rhythm or playable-duration inference, ScoreIR, MusicXML, GP output, OCR, and full notation recognition remain completely unimplemented.

## Codex Comment Disposition
* Codex identified missing staff identity for flag/beam candidate evidence (system_index and staff_index were being read from the wrong level).
* The issue was accepted as a blocker.
* The fix reads `system_index` and `staff_index` from the nested `staff` geometry payload instead of the outer loop object.
* Tests were strengthened to assert non-null expected identity values for emitted flag/beam candidates.
* A direct inline reply was made to Codex on the PR.
* The Codex thread was resolved.
* Final CI and Raster Diagnostics Gate Advisory checks passed.
