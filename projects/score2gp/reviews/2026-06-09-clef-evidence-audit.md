# Clef Evidence Audit

**Status:** PROPOSED
**Date:** 2026-06-09

**Verdict: public fixture evidence insufficient; new reference material is present and likely relevant, but visual opening-symbol evidence is not yet verified.**

## 1. Public fixture snapshot audit
- **Public fixture input files found:** We inspected the tracked snapshot files under `fixtures/public/*.json`.
- **Expected diagnostics snapshots inspected:** A Python parsing script was used to walk all public snapshot dictionaries.
- **Candidate fields observed:** `left_margin_candidates` are populated in multiple fixtures (`expected_diagnostics_complex_cluster.json`, `expected_diagnostics_dense_margin.json`, `expected_diagnostics_sparse.json`, `expected_diagnostics_wide_curves.json`). The observed kinds are merely `vertical_stroke`, `text_span`, and `curve`, with basic font metadata like `Helvetica` and sizes.
- **Whether clef-like target evidence is documented:** No documented clef evidence exists. A comprehensive repository search for the term `clef` across `*.md`, `*.py`, and `*.json` returned **zero** matches. The fixtures do not intentionally or demonstrably encode clef classification.

## 2. New reference material audit
- **Reference directory:** `reference/tab-notation-reference-images/2026-06-09`
- **Files inspected:** The directory contains over 60 PNG image files (e.g., `Capo Notation.png`, `Pick Scrape.png`, `Screenshot 2026-06-09 103745.png`).
- **Method of inspection:** Shell `find` and `file` commands were used to list and check dimensions (mostly ~900x450), and a subset of files was opened via image viewer. *Note: Partial visual confirmation showed treble clefs on standard staves, but key signatures and time signatures were not strictly verified across the dataset.*

## 3. What is now unblocked
**Task 48 — Analyse private/reference opening-symbol fixture diagnostics**

This task should run the existing diagnostics pipeline over the newly available fixture/reference material and map extracted candidates to the visible treble clef, key signature, and time signature regions.

## 4. What remains blocked
- Read-only clef classifier implementation remains blocked until diagnostics extraction over the new material proves real candidate evidence is present and reproducible.
- ScoreIR emission remains blocked.
- Key/time signature recognition remains blocked.
- Any semantic grouping rule remains blocked until separately designed.
