## Current Active Task

## Task 130 — Add read-only x-aligned cluster candidate reporting boundary

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 128 completed discovery of the next safe boundary.
Outcome A was verified: existing diagnostics safely expose `x_aligned_cluster_candidates` as primitive-derived boundaries, supported by existing models, extraction logic, and test fixtures (e.g. `expected_diagnostics_complex_cluster.json`). No product code changes were made during discovery.

Goal:
Add read-only reporting for `x_aligned_cluster_candidates`.
Expose existing diagnostic `x_aligned_cluster_candidates` through the generic read-only `note-candidate-recognition` reporting path.
Emit output as read-only diagnostic-derived candidate evidence only, using a clear symbol type like `x_aligned_cluster_candidate`.
Preserve existing `whole_note_candidate`, `half_note_candidate`, and `quarter_note_candidate` outputs.
Preserve generic `score2gp note-candidate-recognition` and compatibility `score2gp whole-note-recognition`.
Preserve `scripts/note_candidate_recognition_report.py`.
Add tests proving x-aligned cluster candidate reporting and preservation of existing note reporting.
Use existing safe public fixture evidence. Avoid fixture churn.
Stop and report if the existing diagnostic field is unavailable or cannot safely support reporting.

Non-goals:
* Do not expose `left_margin_candidates`; reserve that for a later task.
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
Execute Product Task 130 in the `score2gp` repository.
