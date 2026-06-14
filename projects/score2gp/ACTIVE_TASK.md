## Current Active Task

## Product Task 132 — Add read-only left-margin candidate reporting boundary

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 130 completed by exposing read-only `x_aligned_cluster_candidates` through the generic `note-candidate-recognition` pathway while explicitly preserving whole-note compatibility outcomes.

Goal:
Add read-only reporting for `left_margin_candidates`.
Expose existing diagnostic `left_margin_candidates` through the generic read-only `note-candidate-recognition` reporting path.
Emit output as read-only diagnostic-derived candidate evidence only.
Use a clear candidate type such as `left_margin_candidate`.
Preserve existing `whole_note_candidate`, `half_note_candidate`, `quarter_note_candidate`, and `x_aligned_cluster_candidate` outputs.
Preserve generic `score2gp note-candidate-recognition`.
Preserve compatibility `score2gp whole-note-recognition`.
Preserve `scripts/note_candidate_recognition_report.py`.
Keep compatibility outputs isolated exactly as in Product Task 130.
Add tests proving left-margin candidate reporting and preservation of existing note and x-aligned-cluster reporting.
Add or update regression tests proving `whole-note-recognition` does not emit left-margin candidates.
Use existing safe public fixture evidence, especially `fixtures/public/expected_diagnostics_complex_cluster.json` or the corresponding generated public fixture/PDF if needed.
Avoid fixture churn.
Stop and report if the existing diagnostic field is unavailable or cannot safely support reporting.

Non-goals:
* Do not add new primitive extraction.
* Do not alter diagnostic clustering or margin extraction unless absolutely required to consume existing `left_margin_candidates`.
* Do not add pitch inference.
* Do not add staff-position inference.
* Do not add rhythm or playable-duration inference.
* Do not emit ScoreIR.
* Do not emit MusicXML.
* Do not emit Guitar Pro or GP output.
* Do not add OCR.
* Do not add rests as product-facing recognition output.
* Do not add eighth-note recognition as product-facing recognition output.
* Do not emit beam-spanning recognition output.
* Do not emit full notation events.
* Do not broaden into full notation recognition.
* Do not change governance records from the product repo.

Next Step:
Execute Product Task 132 in the `score2gp` repository.
