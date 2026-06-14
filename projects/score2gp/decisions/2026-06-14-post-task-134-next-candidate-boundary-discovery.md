# 2026-06-14 Post-Task 134 — Next Candidate Boundary Discovery

## Context
Product Task 134 was a discovery-only task in `tticom/score2gp`. It inspected existing diagnostics, models, extraction functions, public fixtures, and tests to identify the next safe read-only candidate reporting boundary. Product Task 134 did not modify product code and did not open a product PR.

## Discovery Summary
Score2GP does not currently expose an existing safe `eighth_note_candidate`, rest candidate, flag candidate, or beam candidate boundary. The product currently exposes read-only candidate/reporting evidence for:
* `whole_note_candidate`
* `half_note_candidate`
* `quarter_note_candidate`
* `x_aligned_cluster_candidate`
* `left_margin_candidate`

### Discovery Evidence
* `pdf_staff_notation_diagnostics.py` extracts whole, half, and quarter note candidates only from direct notehead/stem heuristics.
* `pdf_staff_geometry.py` defines top-level candidate diagnostics for whole, half, and quarter note candidates, plus staff-level `left_margin_candidates` and `x_aligned_cluster_candidates`.
* `pdf_geometry_candidate_extractor.py` currently extracts only left-margin and x-aligned cluster candidate objects.
* Generic primitive evidence includes curves, vertical strokes, diagonal strokes, horizontal strokes, rectangles, and text spans, but those are not yet grouped into explicit flag or beam candidates.

**Explicit conclusion**: No existing safe eighth/rest/flag/beam product-facing candidate boundary exists. The next authorised task must be diagnostic-only. Generic reporting exposure is deferred.

## Authorisation
Product Task 135 is authorised:
**Product Task 135 — Add diagnostic-only flag and beam primitive candidate boundary**

**Goal**:
* Work in `tticom/score2gp`.
* Add diagnostic-only models for flag and beam primitive candidates.
* Use existing geometric primitives only.
* Add fields to notation diagnostics for flag and beam candidate diagnostics.
* Add extraction/grouping logic that classifies existing primitive evidence into flag-like and beam-like diagnostic candidates.
* Keep output private-safe and read-only.
* Add targeted tests for model validation and diagnostic extraction.
* Use public fixtures only.
* Preserve existing whole-note, half-note, quarter-note, x-aligned-cluster, and left-margin candidate behaviour.
* Preserve `score2gp whole-note-recognition` compatibility output.
* Preserve generic `score2gp note-candidate-recognition` existing outputs.
* Avoid fixture churn unless a minimal public fixture update is strictly required and justified.

**Non-goals**:
* Do not expose `flag_candidate` or `beam_candidate` through `note-candidate-recognition` yet.
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

## Known Limitations
The product cannot report structured eighth notes, rests, explicit flags, or beams yet because the underlying diagnostic grouping and schema do not exist.
