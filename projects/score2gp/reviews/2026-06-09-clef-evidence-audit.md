# Clef Evidence Audit

**Status:** PROPOSED
**Date:** 2026-06-09

**Verdict: fixture evidence insufficient**

## Evidence inspected:
- **Public fixture input files found:** We inspected the tracked snapshot files under `fixtures/public/*.json`.
- **Expected diagnostics snapshots inspected:** A Python parsing script was used to walk all public snapshot dictionaries.
- **Candidate fields observed:** `left_margin_candidates` are populated in multiple fixtures (`expected_diagnostics_complex_cluster.json`, `expected_diagnostics_dense_margin.json`, `expected_diagnostics_sparse.json`, `expected_diagnostics_wide_curves.json`). The observed kinds are merely `vertical_stroke`, `text_span`, and `curve`, with basic font metadata like `Helvetica` and sizes.
- **Whether clef-like target evidence is documented:** No documented clef evidence exists. A comprehensive repository search for the term `clef` across `*.md`, `*.py`, and `*.json` returned **zero** matches. The fixtures do not intentionally or demonstrably encode clef classification.
- **Commands run:**
  - Python candidate extraction script walking `fixtures/public/*.json`.
  - `grep_search` looking for `clef` globally and within proximity to `left margin`.

## Insufficient Evidence Findings:
- **What is missing:** There is no tracked public input fixture that intentionally contains distinguishable "clef" evidence. The current `left_margin_candidates` are generic geometric primitives (strokes, text, curves). We cannot distinguish clef-like evidence from generic left-margin text or strokes without making semantic guesses or performing undocumented visual inspection of the underlying PDFs. 
- **Recommendation:** The next task must be a **fixture/evidence prerequisite task** to deliberately create and track public standard-staff fixtures that encode verifiable clef evidence. Task 48 (implementation of a read-only clef classifier) must remain blocked until this evidence exists.
