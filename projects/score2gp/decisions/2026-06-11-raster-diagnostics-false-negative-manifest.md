# Decision: Task 68 — Next Diagnostic-Only Evidence Path

**Date:** 2026-06-11
**Status:** Accepted
**Context:** Product PR #240 (Task 67)

## 1. Task 67 Completion and Available Evidence
Task 67 is complete and has been merged (commit `94ba76a4f9ce0a184f81d35711bf989ba83f8753`). The available evidence now includes:
- A repeatable raster diagnostics gate report script (`scripts/raster_diagnostics_gate_report.py`).
- Quantitative counts for blank staves, TAB staves, noise, positive fixtures, false positives, false negatives, and unknowns.
- Two false negatives currently reported on positive private fixtures.

## 2. Block on Semantic Promotion
As established in Task 66, semantic promotion of `treble_clef_candidate` remains explicitly blocked. We continue on a purely diagnostic path.

## 3. Selected Next Diagnostic-Only Path
The next task must build upon the gate report to formalize the known false negatives.

**Decision:** We select a new product Task 69 focused on classifying the false-negative categories into a machine-readable manifest.

### Task 69 Requirements:
- Create a small tracked manifest for the currently verified false-negative evidence from PR #240, using anonymised category identifiers and safe metadata only. If prior corpus-review evidence is used, cite the committed governance document and distinguish false-negative instances from category names. Do not invent a category taxonomy.
- Integrate this manifest with the raster diagnostics gate report.
- The gate report should be able to cross-reference actual false negatives against the expected categories.

### Non-goals / Blocked Actions for Task 69:
- Do not perform threshold tuning.
- Do not perform classifier hardening.
- Do not emit ScoreIR.
- Do not authorise recognised clef objects.
- Do not authorise OCR.
- Do not authorise vector/raster fusion.
- Do not authorise semantic promotion of `treble_clef_candidate`.
- Do not commit private fixture names.
- Do not commit raw diagnostic JSON dumps.
- Do not commit page images.
- Do not commit screenshots.
- Do not commit PDF extracts.
- Do not commit GP files.
- Do not commit any private or copyrighted content.
