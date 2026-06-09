# Current Private PDF Failure Triage — 2026-06-09

## Summary

Current failures are caused by missing diagnostics—specifically, primitive-level geometry (lines, curves, rectangles) bounds are not serialized in the output, blocking candidate extraction from relying on them. Aggregate counts are currently being exported instead. In addition, the system falsely reports `pdf_grouping_status: safe` even when severe partial grouping and extraction issues occur, leading to a high percentage of unmatched tab candidates.

## Environment

* Governance repo branch and HEAD: `main` at `5ebeb239`
* Product repo branch and HEAD: `test/pdf-curve-position-diagnostics-fixture-v0.1` at `dcfb717`
* Dirty/clean status: Clean
* Date/time: 2026-06-09
* Model used: Gemini 3.1 Pro (High) & Claude Opus 4.6 (Thinking)

## Private run corpus

| slug | PDF path | reference GP path | run dir | report path | log path | exit code | output exists | key observed failure |
|---|---|---|---|---|---|---|---|---|
| lesson3_pdf_only_full | .../Lesson-3.pdf | .../Lesson-3.gp | .../lesson3_... | .../report.json | .../run.log | 0 | true | High unmatched count, technique text unaligned |
| lesson5_pdf_only_full | .../Lesson-5.pdf | .../Lesson-5.gp | .../lesson5_... | .../report.json | .../run.log | 0 | true | 48% unmatched tabraw, partial grouping warnings |
| lesson6_pdf_only_full | .../Lesson-6.pdf | .../Lesson-6.gp | .../lesson6_... | .../report.json | .../run.log | 0 | true | 79% unmatched tabraw, 916 unmatched candidates |
| lesson7_pdf_only_full | .../Lesson-7.pdf | .../Lesson-7.gp | .../lesson7_... | .../report.json | .../run.log | 0 | true | High match ratio, but technique unaligned |
| derek_trucks_bb_king_...| .../Derek Trucks...| N/A | .../derek_... | .../report.json | .../run.log | 0 | true | 61% unmatched, false-safe grouping status |
| melodic_soloing_... | .../Melodic...| .../Melodic... | .../melodic_... | .../report.json | .../run.log | 0 | true | 50% unmatched, large-format spacing issues |

## Artifact inventory

The directory contains subdirectories for each of the 6 runs in the manifest. Notable files within each run:
- `report.json`: High-level metrics, summary counts, status, and pdf-only diagnostics.
- `warnings.json`: Detailed warning events with provenance blocks containing real bboxes of candidate findings.
- `run.log`: Console log showing sequential processing steps and echoing warnings.
- `score.ir.json`: Intermediary format mapping the extracted geometry into track/bar/system formats.
- `tab/tab_raw.json`: The extracted candidate pool containing real pdf word/text bounding boxes (x0/y0/x1/y1).
- `inspect/pages/*.png` and `tab/overlays/*.png`: Debug overlays and rasterizations of PDF pages.

## Findings by run

### `lesson3_pdf_only_full`
* Input PDF: `.../fixtures/private/Lesson-3.pdf`
* Reference GP: `.../fixtures/private/Lesson-3.gp`
* Command file path: `.../lesson3_pdf_only_full/command.txt`
* Report path: `.../lesson3_pdf_only_full/report.json`
* Log path: `.../lesson3_pdf_only_full/run.log`
* Exit code: 0
* Actual observed behaviour: Generates output GP cleanly, 10% unmatched tabraw candidates (51 unmatched). High frequency of barline diagnostics (barline too short / outside staff region).
* Expected high-level behaviour: Produce valid 64-bar GP score.
* Diagnostic evidence present: `tab_staff_bbox` (real coords), per-candidate bboxes.
* Diagnostic evidence missing: Primitive-level bounds, left margin, clustering bounds.
* Failure classification: downstream ScoreIR/build issue (Technique marker unaligned).
* Short relevant excerpts: `{"code": "tabraw-technique-text-not-aligned", "message": "Tab candidate '/' of kind 'technique-text' is not yet aligned to score timeline."}`

### `lesson5_pdf_only_full`
* Input PDF: `.../fixtures/private/Lesson-5.pdf`
* Reference GP: `.../fixtures/private/Lesson-5.gp`
* Command file path: `.../lesson5_pdf_only_full/command.txt`
* Report path: `.../lesson5_pdf_only_full/report.json`
* Log path: `.../lesson5_pdf_only_full/run.log`
* Exit code: 0
* Actual observed behaviour: 48% unmatched tabraw candidates (275 unmatched vs 297 matched). Partial grouping warnings present but status is falsely safe.
* Expected high-level behaviour: Accurate candidate matching.
* Diagnostic evidence present: `tab_staff_bbox`, `system_index`, per-candidate bboxes.
* Diagnostic evidence missing: Primitive-level bounds, system_connectors (empty).
* Failure classification: system/staff grouping failed (partially) and candidate extraction missing context.
* Short relevant excerpts: `partial_pdf_grouping` warning triggers with 572 total candidates but only 297 playable fret.

### `lesson6_pdf_only_full`
* Input PDF: `.../fixtures/private/Lesson-6.pdf`
* Reference GP: `.../fixtures/private/Lesson-6.gp`
* Command file path: `.../lesson6_pdf_only_full/command.txt`
* Report path: `.../lesson6_pdf_only_full/report.json`
* Log path: `.../lesson6_pdf_only_full/run.log`
* Exit code: 0
* Actual observed behaviour: Massive 79% unmatched candidate failure (916 unmatched out of 1154).
* Expected high-level behaviour: Meaningful match ratio.
* Diagnostic evidence present: Same as above.
* Diagnostic evidence missing: Primitive-level geometry evidence, left margin arrays.
* Failure classification: system/staff grouping failed / downstream processing failed.
* Short relevant excerpts: `{"code": "pdf_grouping_not_safe_for_build_ir", ...}`

### `lesson7_pdf_only_full`
* Input PDF: `.../fixtures/private/Lesson-7.pdf`
* Reference GP: `.../fixtures/private/Lesson-7.gp`
* Command file path: `.../lesson7_pdf_only_full/command.txt`
* Report path: `.../lesson7_pdf_only_full/report.json`
* Log path: `.../lesson7_pdf_only_full/run.log`
* Exit code: 0
* Actual observed behaviour: 90% match ratio, but multiple technique text items unaligned.
* Expected high-level behaviour: Full match of all candidates.
* Diagnostic evidence present: Fret candidate bboxes, staff bboxes.
* Diagnostic evidence missing: Primitive counts, left_margin bounds.
* Failure classification: downstream ScoreIR/build issue (unaligned symbols).
* Short relevant excerpts: `{"code": "technique_attachment_requires_note_target"}`

### `derek_trucks_bb_king_pdf_only_full`
* Input PDF: `.../fixtures/private/Derek Trucks BB King.pdf`
* Reference GP: N/A
* Command file path: `.../command.txt`
* Report path: `.../report.json`
* Log path: `.../run.log`
* Exit code: 0
* Actual observed behaviour: 61% unmatched candidates, severe grouping warnings (`pdf_grouping_not_safe_for_build_ir`, `pdf_missing_pdf_grouping_blocks_build_ir`) but report claims grouping is safe.
* Expected high-level behaviour: Recognition without severe partial grouping warnings, or graceful refusal.
* Diagnostic evidence present: Bboxes in warning provenances.
* Diagnostic evidence missing: Ground truth GP, explicit primitive arrays.
* Failure classification: system/staff grouping failed (false-safe).
* Short relevant excerpts: `pdf_partial_grouping_with_playable_candidates`

### `melodic_soloing_masterclass_pdf_only_full`
* Input PDF: `.../fixtures/private/Melodic Soloing Masterclass.pdf`
* Reference GP: `.../fixtures/private/Melodic Soloing Masterclass.gp`
* Command file path: `.../command.txt`
* Report path: `.../report.json`
* Log path: `.../run.log`
* Exit code: 0
* Actual observed behaviour: Large staff spacing triggers distinct errors (`pdf_fret_bbox_too_tall`, `pdf_large_tab_staff_spacing_detected`). 50% unmatched ratio.
* Expected high-level behaviour: Robust handling of large-spaced fonts.
* Diagnostic evidence present: Real coords showing large staff heights (132.874pt).
* Diagnostic evidence missing: Primitive bounds.
* Failure classification: left-margin capture failure / large-format scaling failure.
* Short relevant excerpts: `{"code": "pdf_fret_bbox_too_tall"}`

## Cross-run pattern

- **False Safe Grouping:** `pdf_grouping_status` routinely reports `"safe"` even when warnings clearly indicate partial grouping or critical blockages (e.g., `pdf_grouping_not_safe_for_build_ir`).
- **High Unmatched Ratios:** Complex lessons exhibit huge surplus unmatched tabraw candidates (up to 79%), indicating severe candidate extraction misses.
- **Empty Structural Connectors:** `system_connectors` fields are universally empty `[]`.
- **Missing Primitive Bounds:** All structural processing relies entirely on raw PDF candidate text bounding boxes. Visual primitives (lines/curves/rectangles) are purely aggregated and their individual bounds are lost.

## Evidence model assessment

* Do current diagnostics expose real primitive-level bounds?
  **No.** `PrimitiveGeometry` objects containing `x0/y0/x1/y1` exist internally within `pdf_staff_notation_diagnostics.py` but they are never serialized. They are reduced to scalar counts for serialization.
* Are aggregate counts still the blocker?
  **Yes.** `clustering` and `left_margin` diagnostics output only typed aggregates (e.g., `x_aligned_cluster_count`). No coordinates are produced, preventing subsequent candidate extraction from leveraging genuine geometries.
* Is any fake/synthesized geometry being created?
  **No.** Bounding boxes present in the system strictly belong to raw PDF text extractions (`page`, `x0`, `y0`, `x1`, `y1`).
* Is the system preserving enough evidence to support candidate extraction?
  **No.** Because primitive bounds (curves/lines) are stripped and aggregated, an optical extraction pass has no serialized bounding boxes to rely on to establish structure or relationships (like finding fret boundaries precisely via visual lines).

## Recommended next implementation task

* **title**: Expose primitive-level geometry bounds in diagnostics payload
* **goal**: Ensure `PrimitiveGeometry` instances (with real `x0/y0/x1/y1` fields) are cleanly serialized and made available to downstream processes, thereby removing the reliance on aggregate counts and unblocking the optical candidate extraction sequence.
* **non-goals**: Do not build the candidate extractors themselves yet. Do not implement complex heuristic geometric mapping or fix the "false safe" grouping logic in this immediate task.
* **likely files**: `src/score2gp/pdf_staff_geometry.py`, `src/score2gp/pdf_staff_notation_diagnostics.py`, and the accompanying JSON schemas.
* **acceptance criteria**: `PrimitiveGeometry` arrays or corresponding objects are present in the JSON serialization, and unit tests verify that a known primitive outputs correct bounds matching its source PDF geometry.
* **validation commands**: `pytest tests/test_pdf_staff_geometry_diagnostics.py -v`
* **stop conditions**: If exposing these arrays inflates the JSON payload unmanageably for standard runs, pause to design a filtering/scoping mechanism.

## Tasks not recommended yet

* **Add candidate models/extractors**: Explicitly blocked because they cannot reliably extract structural elements without the exposed primitive geometry.
* **Improve staff/system grouping**: Fails without accurate geometric evidence.
* **Fix downstream ScoreIR/build handling**: This is treating symptoms of the missing structural confidence.

## What was not tested

* I did not open and visually review the private PDFs or GP outputs.
* No internal code modification or candidate-generation tests were executed.
* I did not deeply parse the GP binary files or recreate the extraction heuristics locally.
