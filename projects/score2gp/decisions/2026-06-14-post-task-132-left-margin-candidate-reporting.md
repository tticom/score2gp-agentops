# 2026-06-14 Post-Task 132 — Left Margin Candidate Reporting

## Context
Product Task 132 was authorised via Governance PR #154.
Product PR #271 in `tticom/score2gp` completed Product Task 132 by adding read-only reporting for `left_margin_candidates`.

### Verified State
* **Product PR #271 URL**: `https://github.com/tticom/score2gp/pull/271`
* **Final head SHA**: `c3c1902fda912404ed2b2ca44db102b7d1c03aae`
* **Merge commit SHA**: `3d7d01ed2d07f8b6e690e48244fa1227650af68b`
* **Changed files count**: 6
* **Changed files**:
  * `scripts/note_candidate_recognition_report.py`
  * `src/score2gp/cli.py`
  * `src/score2gp/whole_note_recogniser.py`
  * `tests/test_note_candidate_recognition_cli.py`
  * `tests/test_note_candidate_recognition_report.py`
  * `tests/test_whole_note_recognition_cli.py`
* **Checks status**: `CI` and `Raster Diagnostics Gate Advisory` were successful.

### User-Visible Capability
* Score2GP has read-only candidate recognition/reporting for:
  * `whole_note_candidate`
  * `half_note_candidate`
  * `quarter_note_candidate`
  * `x_aligned_cluster_candidate`
  * `left_margin_candidate`
* `left_margin_candidate` is exposed only through the generic read-only `note-candidate-recognition` path.
* `whole-note-recognition` compatibility output remains strictly preserved.
* `scripts/note_candidate_recognition_report.py` remains preserved.
* Current recognition remains read-only candidate evidence only.

## Codex Comment Disposition
* Codex identified duplicate notation diagnostics extraction when both generic diagnostic-derived candidate streams were enabled.
* The comment was accepted as a blocker.
* The fix cached `page_diags` once per page when either optional stream is requested.
* The cached diagnostics are reused for both x-aligned cluster and left-margin candidate extraction.
* A direct inline reply was made.
* The Codex inline thread was resolved after verification.
* Final CI and Raster Diagnostics Gate Advisory checks passed.

## PR Readiness Evidence
- PR state: merged
- Head SHA: `c3c1902fda912404ed2b2ca44db102b7d1c03aae`
- Mergeable: N/A (merged)
- Changed files: `scripts/note_candidate_recognition_report.py`, `src/score2gp/cli.py`, `src/score2gp/whole_note_recogniser.py`, `tests/test_note_candidate_recognition_cli.py`, `tests/test_note_candidate_recognition_report.py`, `tests/test_whole_note_recognition_cli.py`
- CI/checks: `CI` success and `Raster Diagnostics Gate Advisory` success
- Codex review submissions: one Codex review submission
- Codex inline comments: one inline comment about duplicate diagnostics extraction
- Review threads: one Codex inline thread
- Unresolved threads: zero after supervisor resolution
- Codex comment disposition: accepted as blocker, fixed by caching `page_diags` once per page, direct inline reply made, thread resolved after verification
- Regression tests added/updated: tests covering left-margin reporting and whole-note compatibility isolation
- Known limitations: still read-only candidate evidence only; no eighth-note recognition, rests, pitch inference, staff-position inference, rhythm/playable-duration inference, ScoreIR, MusicXML, GP output, OCR, or full notation recognition

## Authorisation
Product Task 134 is authorised:
**Product Task 134 — Discover next safe read-only candidate reporting boundary**

**Goal**:
This is a product discovery task. Inspect existing product diagnostics, models, fixtures, and tests to identify the next safe product-facing read-only candidate output. The preferred target is eighth-note candidate reporting, but only if existing diagnostics already safely expose enough evidence. Do not authorise implementation yet unless the discovery proves the existing boundary is safe.

**Scope and Exclusions**:
* This is a discovery-only task; do not modify code in the product repository.
* Preserve current whole-note, half-note, quarter-note, x-aligned-cluster, and left-margin candidate reporting.
* Preserve generic and compatibility reporting paths.
* **Do not** implement new product-facing recognition output.
* **Do not** implement or authorise new primitive extraction.
* **Do not** implement or authorise pitch inference, staff-position inference, rhythm inference, or playable-duration inference.
* **Do not** authorise ScoreIR, MusicXML, GP output, OCR, or full notation events.
* **Do not** implement rests, eighth-note, or beam output.
