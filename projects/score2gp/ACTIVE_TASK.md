## Current Active Task

## Product Task 141 — Add staff identity to generic note candidate evidence

Status: ACTIVE

Owning repo: score2gp

Context:
Governance PR has authorised this task after the successful completion of Product Task 139 discovery, which revealed that existing whole/half/quarter note candidates lack the `system_index` and `staff_index` necessary to safely test a staff-local composition join with flag/beam evidence.

Goal:
This task should add a safe staff-association boundary for whole/half/quarter note candidates and expose `system_index` and `staff_index` on their generic read-only outputs.

Scope:
* Work in `tticom/score2gp`.
* Add staff/system identity to generic whole, half, and quarter note candidate evidence.
* Ensure `whole_note_candidate`, `half_note_candidate`, and `quarter_note_candidate` generic outputs include:
  * `page_index`
  * `system_index`
  * `staff_index`
  * `bbox`
* Add a safe staff-association boundary for existing note candidate evidence.
* Prefer using existing notation/staff diagnostics and public fixtures.
* Preserve existing generic candidate outputs:
  * `x_aligned_cluster_candidate`
  * `left_margin_candidate`
  * `flag_candidate`
  * `beam_candidate`
* Preserve `score2gp whole-note-recognition` compatibility output unless explicitly and safely updated with regression coverage.
* Preserve `scripts/note_candidate_recognition_report.py`.
* Add tests proving note candidates include non-null `system_index` and `staff_index`.
* Add tests proving existing candidate outputs remain preserved.
* Add or identify a minimal public fixture that can later support eighth-note composition-boundary testing only if this can be done without fixture churn or semantic overreach.

Non-goals:
* Do not implement `eighth_note_candidate` reporting.
* Do not implement eighth-note recognition.
* Do not infer pitch.
* Do not infer rhythm or playable duration.
* Do not infer staff position as musical semantics beyond existing staff identity.
* Do not implement rests.
* Do not emit ScoreIR.
* Do not emit MusicXML.
* Do not emit Guitar Pro or GP output.
* Do not add OCR.
* Do not emit full notation events.
* Do not broaden into full notation recognition.
* Do not change flag/beam diagnostic heuristics.
* Do not change governance records from the product repo.
* Do not commit generated artifacts, raw dumps, screenshots, private PDFs, GP files, logs, credentials, or unrelated files.

Next Step:
Execute Product Task 141 in the `score2gp` repository.
