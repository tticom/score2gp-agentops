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

While these vector sources do not share identical basenames with the visual screenshots, they provide vector-source material; named treble-clef PDF smoke is still required to prove treble-clef mapping.

## 6. Diagnostics entry point check
Existing diagnostic entry points and helpers discovered:
* `src/score2gp/pdf_staff_notation_diagnostics.py`
* `src/score2gp/pdf_geometry_candidate_extractor.py`
* Generative fixture scripts (e.g., `tests/fixtures/pdf/make_standard_staff_expected_diagnostics.py`)

These runners successfully depend on PDF extraction (`pymupdf`) and can process the vector sources found in the `fixtures` directory.

## 7. Optional vector-PDF smoke
A diagnostics smoke test over the generative `wide_curves` fixture demonstrates successful candidate extraction. Note that this is parsed from existing JSON, not regenerated live.
* **Command:** `python3 -c "import json; [print(c) for c in json.load(open('fixtures/public/expected_diagnostics_wide_curves.json'))[0]['left_margin_candidates']]"` (Exit code: 0)
* **Input:** Existing JSON output for the generative standard staff vector fixture (`expected_diagnostics_wide_curves.json`).
* **Completed:** Yes
* **`left_margin_candidates`:** Populated
  * **Count:** 2
  * **Kinds:** `['vertical_stroke', 'curve']`
  * **Geometry:** x_range=80.0..150.0, y_range=85.0..134.0
* **Mapping plausibility:** The `wide_curves` fixture proves that vector fixtures can produce left-margin `vertical_stroke` and `curve` candidates. It does not by itself prove treble-clef mapping unless the fixture is documented or visually verified as containing a treble clef.

## 8. Source-normalisation verdict
**vector source available; treble-clef diagnostics mapping still requires a named treble-clef PDF smoke**

* Vector-source material exists under the `fixtures` directory.
* Treble-clef diagnostic mapping is not yet proven until an actual treble-clef vector source (such as `Lesson-3.pdf`) is explicitly smoke-tested and mapped against its visual region.

## 9. Recommended next task
**Task 50 — Map treble-clef candidate diagnostics from vector-source fixtures using a named treble-clef PDF smoke**

## 10. What remains blocked
* Product recogniser implementation remains blocked.
* ScoreIR emission remains blocked.
* Key signature recognition remains blocked.
* Time signature recognition remains blocked.
* Image/OCR recognition remains out of scope unless separately authorised.
* Semantic grouping remains blocked until separately designed.
