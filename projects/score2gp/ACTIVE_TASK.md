## Current Active Task

## Product Task 135 — Add diagnostic-only flag and beam primitive candidate boundary

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 134 completed discovery and found that no safe existing eighth/rest/flag/beam product-facing candidate boundary exists. Primitives like curves and strokes are extracted but not explicitly clustered into flag or beam candidates.

Goal:
Add diagnostic-only models for flag and beam primitive candidates using existing geometric primitives only.
Add fields to notation diagnostics for flag and beam candidate diagnostics.
Add extraction/grouping logic that classifies existing primitive evidence into flag-like and beam-like diagnostic candidates.
Keep output private-safe and read-only.
Add targeted tests for model validation and diagnostic extraction using public fixtures only.
Preserve existing whole-note, half-note, quarter-note, x-aligned-cluster, and left-margin candidate behaviour.
Preserve `score2gp whole-note-recognition` compatibility output.
Preserve generic `score2gp note-candidate-recognition` existing outputs.
Avoid fixture churn unless a minimal public fixture update is strictly required and justified.

Non-goals:
* Do not expose `flag_candidate` or `beam_candidate` through `note-candidate-recognition` yet (generic reporting exposure is deferred).
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
* Do not modify governance records from the product repo.
* Do not commit generated artifacts, raw dumps, screenshots, PDFs, GP files, logs, credentials, or unrelated files.

Next Step:
Execute Product Task 135 in the `score2gp` repository.
