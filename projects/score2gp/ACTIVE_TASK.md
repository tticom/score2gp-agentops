## Current Active Task

## Product Task 145 — Add generated public eighth-note geometry fixtures

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 143 discovery proved that while structural identity (`system_index`, `staff_index`, `bbox`) is correctly populated for candidates, there is currently NO public fixture containing both `quarter_note_candidate` and `beam_candidate` simultaneously. Furthermore, the flag candidates in existing fixtures are synthetic quadrants. We cannot safely tune or prove an `eighth_note_candidate` join boundary without valid geometry to test against.

Goal:
Create generated public fixture evidence for future eighth-note candidate composition.

Scope:
* Work in `tticom/score2gp`.
* Add generated public fixture coverage for eighth-note geometry.
* Include at least one solitary flagged eighth note.
* Include at least one beamed pair of eighth notes.
* Ensure the fixture can produce the necessary existing generic candidate evidence:
  * `quarter_note_candidate`
  * `flag_candidate`
  * `beam_candidate`
  * populated `page_index`
  * populated `system_index`
  * populated `staff_index`
  * populated `bbox`
* Add or update tests/expected diagnostics only as needed to prove the fixture evidence.
* Preserve existing candidate extraction behaviour.

Non-goals:
* Do not implement `eighth_note_candidate` reporting.
* Do not implement eighth-note recognition.
* Do not infer pitch.
* Do not infer rhythm or playable duration.
* Do not emit ScoreIR.
* Do not emit MusicXML.
* Do not emit Guitar Pro or GP output.
* Do not add OCR.
* Do not alter existing extraction heuristics. If fixture work discovers that heuristic changes are required, stop and report the blocker for a separate governance decision.
* Do not commit private PDFs, generated scratch dumps, screenshots, logs, credentials, or unrelated artifacts.

Next Step:
Execute Product Task 145 in the `score2gp` repository.
