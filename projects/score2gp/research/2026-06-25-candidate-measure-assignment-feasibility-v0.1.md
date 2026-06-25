# Architect Research: Candidate-to-Measure Spatial Assignment Feasibility

## Verified Baseline
- **Product PR:** https://github.com/tticom/score2gp/pull/326
- **Product PR Head SHA:** `e63c4919d8cc488a69e2dd27d0ba0f3a4476c747`
- **Product PR Merge Commit:** `7565e751e0dea624a209aeb4233373338296262a`
- **Governance PR:** https://github.com/tticom/score2gp-agentops/pull/213
- **Governance PR Merge Commit:** `efc3a7ace72ea7456b7b45c25a6735ee3119c61c`

## Executive Summary
**Outcome B selected.** Measure-grid diagnostics provide excellent bounded horizontal regions per staff. However, existing notation candidates (`WholeNoteCandidateDiagnostics`, `HalfNoteCandidateDiagnostics`, `QuarterNoteCandidateDiagnostics`) are currently exposed as global page-level arrays and entirely lack staff identity. Because their Y-bounds can fall outside the strict 5-line `staff_bounds` (e.g. ledger lines), assigning candidates to staves via pure Y-coordinate intersection is inherently ambiguous in multi-staff systems. Developer implementation of candidate-to-measure assignment cannot proceed until staff identity is preserved for candidate evidence.

## Files and Functions Inspected
- `src/score2gp/pdf_staff_geometry.py`: Inspected `PdfStaffNotationGeometryDiagnostics`, `WholeNoteCandidateDiagnostics`, `QuarterNoteCandidateDiagnostics`, `MeasureGridDiagnostics`, and `MeasureGridStaff`.
- `src/score2gp/pdf_staff_notation_diagnostics.py`: Inspected `extract_notation_diagnostics_dict`, `extract_measure_grid_diagnostics_dict`, `build_notation_diagnostics`, and `_extract_note_candidates`.
- `tests/test_pdf_measure_grid_diagnostics.py`

## Fixtures Inspected (via Scratch Scripts)
- `generated_standard_staff_quarter_note.pdf`
- `generated_standard_staff_multi_staff.pdf`
- `generated_standard_staff_ledger_lines.pdf`
- `generated_paired_notation_tab_system_double_barline.pdf`

## Evidence Gathering

### 1. Notation Candidate Evidence
- **Fact:** Notation candidates (whole, half, quarter) are produced and stored in `PdfStaffNotationGeometryDiagnostics` at the root level (`whole_note_candidates`, etc.).
- **Fact:** These candidates expose geometric evidence including `bbox` `[x0, y0, x1, y1]`, `width`, `height`, `aspect_ratio`, and for stemmed notes, `stem_bbox`.
- **Fact:** The candidates **do not** contain `page_index`, `system_index`, or `staff_index`. They have no explicit linkage to the staff they belong to.

### 2. Measure-Grid Diagnostics Compatibility
- **Fact:** `MeasureGridDiagnostics` provides a clear hierarchy: `pages` -> `systems` -> `staves` -> `measure_regions`.
- **Fact:** Each measure region exposes `start_x` and `end_x`.
- **Fact:** Each staff exposes `staff_bounds`, which tightly binds the 5 staff lines (e.g., `y0=100.0, y1=134.0`).
- **Inference:** Candidate horizontal X-bounds (or their `stem_bbox` X coordinates or calculated `center_x`) are in the same coordinate space and are geometrically compatible with measure region `start_x`/`end_x`.

### 3. Staff Identity Preservation
- **Fact:** Staff identity is **not** preserved for note candidates in the current diagnostics.
- **Inference:** In multi-staff systems (e.g. `generated_standard_staff_multi_staff.pdf`), attempting to map a candidate to a staff via Y-coordinate intersection with `staff_bounds` will be ambiguous for notes on ledger lines (e.g. `generated_standard_staff_ledger_lines.pdf`). A note below Staff 1 might geometrically overlap the coordinate space above Staff 2.
- **Conclusion:** Without staff identity firmly established during extraction (before the candidates are grouped globally), cross-staff assignment errors are unavoidable.

### 4. Barlines and X-axis Ambiguity
- **Fact:** Double/repeat barlines are successfully collapsed by `MeasureGridDiagnostics`, avoiding false empty regions.
- **Hypothesis:** For candidates near internal barlines, using the candidate's `bbox` could span across a barline X-coordinate. However, using the candidate's `center_x` (derived from `bbox` or `stem_bbox`) would unambiguously resolve it to a single measure region once staff identity is known.

## Smallest Additional Diagnostic Evidence Needed
Because staff identity is missing, we cannot proceed with full candidate-to-measure assignment implementation. The smallest required next step is to **add staff identity to candidate extraction**.

**Smallest Additional Diagnostic Evidence Requirement:**
Update `PdfStaffNotationGeometryDiagnostics` and its extraction logic to preserve staff identity. For example, move `whole_note_candidates`, `half_note_candidates`, and `quarter_note_candidates` inside `NotationStaffDiagnostics`, or add explicit `staff_index`/`system_index` fields to the candidate diagnostic models. This follow-up is not authorised for Developer implementation until Reviewer architecture verification approves Outcome B and the next requirement.

## Conclusion
**Outcome B.** Developer implementation of candidate-to-measure assignment remains blocked. We must first fix candidate staff-identity preservation in the structural diagnostics layer.
