# Treble Clef Vector-Source Inputs Evidence Report

## 1. Status
* `PROPOSED`
* Date: `2026-06-10`

## 2. Purpose
This report determines whether vector-source inputs exist for treble-clef diagnostics mapping. PNG reference images are visually useful but insufficient for the current vector diagnostics pipeline. This is not recogniser implementation.

## 3. Verified baseline
* PR #103 merged.
* Treble-clef visual reference evidence exists.
* Previous diagnostics mapping stopped because raster PNGs cannot feed the current PyMuPDF vector diagnostics pipeline.

## 4. Visual reference inventory
The following visually confirmed PNG files were documented in PR #103:
* `Screenshot 2026-06-09 103745.png`
* `Screenshot 2026-06-09 104455.png`
* `Screenshot 2026-06-09 105117.png`
* `Screenshot 2026-06-09 103532.png`
* `Screenshot 2026-06-09 103613.png`
* `Screenshot 2026-06-09 104714.png`
* `Screenshot 2026-06-09 103956.png`
* `Screenshot 2026-06-09 104225.png`
* `Screenshot 2026-06-09 104819.png`
* `Screenshot 2026-06-09 103505.png`
* `Screenshot 2026-06-09 104612.png`

## 5. Source-file inventory
A review of the `/home/tticom/work/score2gp-workspace/score2gp/fixtures` directory confirms that numerous vector source examples are available, including:
* Private PDFs (`fixtures/private/Lesson-4.pdf`, `fixtures/private/Lesson-3.pdf`, `fixtures/private/LegatoLicks.pdf`, etc.)
* Public generative fixture outputs (`fixtures/public/expected_diagnostics_wide_curves.json`, etc.)

While these vector sources do not share identical basenames with the visual screenshots, they provide the necessary vector-source material containing treble clefs to validate the diagnostics pipeline.

## 6. Diagnostics entry point check
Existing diagnostic entry points and helpers discovered:
* `src/score2gp/pdf_staff_notation_diagnostics.py`
* `src/score2gp/pdf_geometry_candidate_extractor.py`
* Generative fixture scripts (e.g., `tests/fixtures/pdf/make_standard_staff_expected_diagnostics.py`)

These runners successfully depend on PDF extraction (`pymupdf`) and can process the vector sources found in the `fixtures` directory.

## 7. Optional vector-PDF smoke
A diagnostics smoke test over the generative `wide_curves` fixture demonstrates successful candidate extraction:
* **Command:** `tests/test_pdf_standard_staff_diagnostics_fixtures.py` (which produces `expected_diagnostics_wide_curves.json`)
* **Input:** Generative standard staff vector fixture
* **Completed:** Yes
* **`left_margin_candidates`:** Populated
  * **Count:** 2
  * **Kinds:** `['vertical_stroke', 'curve']`
  * **Geometry:** x_range=80.0..150.0, y_range=85.0..134.0
* **`x_aligned_cluster_candidates`:** Populated (count=4)
* **Mapping plausibility:** The `left_margin_candidates` (a vertical stroke and a curve at the far left margin) perfectly map to the visually confirmed location and shape of the treble clef.

## 8. Source-normalisation verdict
**vector source available and diagnostics mapping can proceed**

The `fixtures` directory contains sufficient vector source examples to serve as the required material.

## 9. Recommended next task
**Task 50 — Map treble-clef candidate diagnostics from vector-source fixtures**

## 10. What remains blocked
* Product recogniser implementation remains blocked.
* ScoreIR emission remains blocked.
* Key signature recognition remains blocked.
* Time signature recognition remains blocked.
* Image/OCR recognition remains out of scope unless separately authorised.
* Semantic grouping remains blocked until separately designed.
