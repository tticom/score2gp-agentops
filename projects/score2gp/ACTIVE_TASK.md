## Current Active Task

## Product Task 143 — Discover safe eighth-note candidate composition rule

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 141 added safe staff/system identity to generic whole, half, and quarter note candidate evidence, completing the prerequisite for testing a staff-local composition join with flag/beam evidence. Governance Task 144 recorded this completion and authorised this discovery task.

Goal:
This should be a discovery-only task to inspect whether current generic note candidates plus flag/beam candidates can now support a conservative `eighth_note_candidate` composition rule.

Scope:
* Work in `tticom/score2gp`.
* Inspect current generic read-only candidate outputs for:
  * `quarter_note_candidate`
  * `flag_candidate`
  * `beam_candidate`
  * relevant `page_index`, `system_index`, `staff_index`, `bbox`, width, and height fields.
* Inspect current diagnostic models and public fixtures.
* Determine whether a conservative `eighth_note_candidate` composition rule can be safely defined from existing evidence.
* Prefer public fixture evidence only.
* Produce a short product discovery report.
* If a safe rule exists, recommend the next narrow implementation task.
* If no safe rule exists, recommend the smallest prerequisite diagnostic or fixture task.
* Preserve all current generic reporting outputs and compatibility paths.
* Avoid fixture churn.

Non-goals:
* Do not implement `eighth_note_candidate` reporting.
* Do not implement eighth-note recognition.
* Do not implement rests.
* Do not infer pitch.
* Do not infer staff position as musical semantics beyond existing staff identity.
* Do not infer rhythm or playable duration.
* Do not emit ScoreIR.
* Do not emit MusicXML.
* Do not emit Guitar Pro or GP output.
* Do not add OCR.
* Do not emit full notation events.
* Do not broaden into full notation recognition.
* Do not alter diagnostic extraction heuristics.
* Do not change governance records from the product repo.
* Do not commit generated artifacts, raw dumps, screenshots, private PDFs, GP files, logs, credentials, or unrelated files.

Next Step:
Execute Product Task 143 in the `score2gp` repository.
