## Current Active Task

## Product Task 134 — Discover next safe read-only candidate reporting boundary

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 132 completed by exposing read-only `left_margin_candidates` through the generic `note-candidate-recognition` pathway while explicitly preserving whole-note compatibility outcomes. The product now reports whole, half, and quarter note candidates, as well as x-aligned clusters and left margins. The product still lacks eighth-note recognition, rests, pitch inference, staff-position inference, rhythm inference, ScoreIR, MusicXML, GP output, and OCR.

Goal:
This is a product discovery task. Inspect existing product diagnostics, models, fixtures, and tests to identify the next safe product-facing read-only candidate output.
The preferred target is eighth-note candidate reporting, but only if existing diagnostics already safely expose enough evidence. Do not authorise implementation yet unless the discovery proves the existing boundary is safe.

Non-goals:
* This is a no-code discovery task; do not modify code in the product repository, but you may inspect it and report findings.
* Do not implement eighth-note recognition.
* Do not implement rests.
* Do not authorise new primitive extraction.
* Do not authorise pitch inference.
* Do not authorise staff-position inference.
* Do not authorise rhythm or playable-duration inference.
* Do not authorise ScoreIR, MusicXML, GP output, OCR, or full notation events.
* Do not authorise broad notation recognition.
* Do not commit generated artifacts, raw JSON dumps, screenshots, PDFs, GP files, logs, PR body files, private files, credentials, or unrelated files.

Next Step:
Execute Product Task 134 in the `score2gp` repository.
