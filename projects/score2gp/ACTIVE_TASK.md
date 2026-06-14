## Current Active Task

## Product Task 137 — Expose read-only flag and beam diagnostic candidates through generic reporting

Status: ACTIVE

Owning repo: score2gp

Context:
Governance PR has authorised this task after the successful completion of Product Task 135, which added diagnostic-only flag and beam models and internal extraction.

Goal:
Expose existing diagnostic-only flag and beam candidate diagnostics through generic `note-candidate-recognition`.
Add read-only candidate types:
* `flag_candidate`
* `beam_candidate`
Use only the diagnostics added in Product Task 135.
Do not change flag/beam diagnostic extraction heuristics unless required to safely consume the existing diagnostic payload.
Preserve existing generic outputs:
* `whole_note_candidate`
* `half_note_candidate`
* `quarter_note_candidate`
* `x_aligned_cluster_candidate`
* `left_margin_candidate`
Preserve `score2gp whole-note-recognition` compatibility output.
Preserve `scripts/note_candidate_recognition_report.py`.
Add tests proving generic `note-candidate-recognition` emits flag and beam candidates where public fixture evidence supports it.
Add tests proving `whole-note-recognition` does not emit `flag_candidate` or `beam_candidate`.
Add tests proving existing candidate outputs are preserved.
Avoid fixture churn unless strictly required and justified.

Non-goals:
* Do not add `eighth_note_candidate` reporting.
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
* Do not alter diagnostic extraction heuristics except where narrowly required to consume the existing diagnostic payload safely.
* Do not change governance records from the product repo.
* Do not commit generated artifacts, raw dumps, screenshots, PDFs, GP files, logs, credentials, or unrelated files.

Next Step:
Execute Product Task 137 in the `score2gp` repository.
