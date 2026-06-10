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
A thorough inventory search (`find` and `git grep`) across the repository for corresponding vector source files (`.pdf`, `.gp`, `.gpx`, `.musicxml`, `.mxl`, `.xml`, etc.) yielded no results matching these references. No metadata or fixtures map these screenshots to any tracked source score.

## 6. Diagnostics entry point check
Existing diagnostic entry points and helpers discovered:
* `src/score2gp/pdf_staff_notation_diagnostics.py`
* `src/score2gp/pdf_geometry_candidate_extractor.py`
* `scripts/private_diagnostic_smoke.py`

These runners depend entirely on PDF extraction (`pymupdf`). No raster-based OCR runner exists.

## 7. Optional vector-PDF smoke
Not performed. No vector source is available.

## 8. Source-normalisation verdict
**vector source missing; maintainer must provide corresponding PDF/source files**

Requirement: Original vector PDF files corresponding to the visually confirmed screenshots, or source score files plus a reproducible export path to a vector PDF, are required.

## 9. Recommended next task
**Task 50 — Add vector PDF source fixtures for visually confirmed treble-clef references**

## 10. What remains blocked
* Product recogniser implementation remains blocked.
* ScoreIR emission remains blocked.
* Key signature recognition remains blocked.
* Time signature recognition remains blocked.
* Image/OCR recognition remains out of scope unless separately authorised.
* Semantic grouping remains blocked until separately designed.
