## Current Active Task

## Product Task 139 — Discover safe eighth-note candidate composition boundary

Status: ACTIVE

Owning repo: score2gp

Context:
Governance PR has authorised this task after the successful completion of Product Task 137, which exposed read-only flag and beam candidate evidence through generic reporting.

Goal:
The product now exposes notehead/stem-style candidates and flag/beam candidates as read-only evidence, but it has not yet proven a safe boundary for composing those separate pieces into `eighth_note_candidate` evidence. Before implementing eighth-note candidate reporting, inspect whether current public fixtures and diagnostic payloads can support a conservative join rule.

Scope:
* Work in `tticom/score2gp`.
* Inspect existing generic read-only candidate outputs for:
  * `quarter_note_candidate`
  * `flag_candidate`
  * `beam_candidate`
  * relevant geometry fields and staff identity fields.
* Inspect current diagnostic models and public fixtures.
* Determine whether a safe, conservative `eighth_note_candidate` composition boundary can be defined from existing evidence.
* Prefer public fixture evidence only.
* Produce a short discovery report in the product task report.
* If a safe boundary exists, recommend the next narrow implementation task.
* If no safe boundary exists, recommend the smallest prerequisite diagnostic or fixture task.
* Preserve all current generic reporting outputs and compatibility paths.
* Avoid fixture churn.

Non-goals:
* Do not implement `eighth_note_candidate` reporting.
* Do not implement eighth-note recognition.
* Do not implement rests.
* Do not infer pitch.
* Do not infer staff position.
* Do not infer rhythm or playable duration.
* Do not emit ScoreIR.
* Do not emit MusicXML.
* Do not emit Guitar Pro or GP output.
* Do not add OCR.
* Do not emit full notation events.
* Do not broaden into full notation recognition.
* Do not alter diagnostic extraction heuristics.
* Do not change governance records from the product repo.
* Do not commit generated artifacts, raw dumps, screenshots, PDFs, GP files, logs, credentials, or unrelated files.

Next Step:
Execute Product Task 139 discovery in the `score2gp` repository.
