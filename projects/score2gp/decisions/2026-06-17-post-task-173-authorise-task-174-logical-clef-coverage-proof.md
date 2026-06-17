# Decision Record: Post-Task 173 - Authorise Task 174 (Logical Clef Coverage Proof)

## Product Task 173 Completion Summary
Product Task 173 bridged logical clef candidate evidence into the clef-resolved pitch mapping pipeline. It:
* surfaced bbox data from `classify_logical_clef_candidate`;
* integrated logical clef evidence from `LeftMarginPrimitiveCandidate` into `extract_treble_clef_candidate_evidence`;
* allowed `logical_diagnostic_candidate_evidence` and `unified_diagnostic_candidate_evidence` in the clef-resolved diagnostic mapping boundary;
* required raster/logical bbox compatibility before emitting `unified_diagnostic_candidate_evidence`;
* failed closed for conflicting raster/logical bboxes;
* moved raster import behind the page guard so logical-only extraction does not require raster dependencies;
* required `render_scale` to be present and positive before raster evidence is used;
* updated coverage-report clef policy so logical/unified sources are counted consistently;
* preserved read-only diagnostic boundaries;
* did not implement playable output, ScoreIR, MusicXML, GP output, rhythm, accidentals, key signatures, rests, or OCR.

## Governance & Product PR Verifications
* **Governance PR #181:** Verified merged.
* **Product PR #291:** Verified merged.
* **Product PR #292:** Verified merged.
  * Head SHA: `83b8954f9128c4f692e97d7ee4a6876b58c0eda3`
  * Merge Commit: `35600ca88bcb34059cf48a8a5c391b885c62dadb`
  * Files Changed: `3` files (`src/score2gp/logical_clef_candidate_classifier.py`, `src/score2gp/whole_note_recogniser.py`, `tests/test_logical_clef_bridge.py`)

## Product PR #292 Validation Evidence
* **Full test result:** 729 passed in about 30s.
* **Focused bridge result:** 7 passed in 0.16s.
* **Task 170-style coverage analysis:** Completed successfully.

## Product PR #292 Codex Disposition
All Codex P2 findings were resolved:
* raster import moved behind page guard;
* missing/malformed render_scale now fails closed;
* coverage report now counts logical/unified source types consistently.

## Safety/Privacy/Artifact Hygiene Result
Clean. No private artifacts, logs, or uncommitted files leaked. Verified via `git ls-files` check.

## Current Limitation
* The bridge works in focused tests.
* Current authorised public generated fixture aggregate remains unchanged.
* No broad coverage improvement is visible yet because the public fixture set lacks recognisable logical treble-clef primitives natively.

## Reason for Product Task 174
Before playable output or canonical pitch adoption, the project needs a safe public/synthetic proof that logical clef evidence can move a whole-note candidate from missing-clef skip to clef-resolved pitch mapping.

## Explicit Boundary
* Product Task 174 may add or update public/generated/synthetic tests and diagnostics only.
* It must not authorise playable output or canonical pitch output.
