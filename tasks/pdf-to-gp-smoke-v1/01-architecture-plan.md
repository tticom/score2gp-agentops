# Architecture Plan - PDF-to-GP Layout Refinement and Column Grid Projection

This document presents the Research Architect's system analysis, failure model diagnosis, and design plan for unblocking intermediate representation (`ScoreIR`) and Guitar Pro (`.gp`) file conversion on the **Major Triads Lesson 3** private benchmark.

---

## 1. Current Pipeline Summary

The `score2gp` pipeline operates in a staged command-line sequence to translate vector-based born-digital PDFs into Guitar Pro scores:
1. **PDF Inspection & Scaffolding (`pdf.py`)**: Uses PyMuPDF to extract horizontal vector staff segments, vertical barline vectors, page boundaries, and text candidates.
2. **Local Line Grouping**: Clusters adjacent horizontal segments into Y-coordinate bands to identify guitar tablature staves (TAB systems).
3. **Bar Bounding Box Construction**: Validates vertical line candidates as true barlines using relative crossing margins, constructing complete closed bar measure boundary boxes.
4. **Fret Text Assignment**: Extracts text candidates, filters playable fret digits, and maps them spatially into staff systems, strings (snapping to Y coordinates of six staff lines), and constructed bar boxes.
5. **MusicXML Timing Preflight (`musicxml.py`)**: Runs a deterministic voice timeline simulation to validate compound meter grids, backup/forward movements, and same-voice/cross-voice overlaps.
6. **Timeline Alignment (`ascii_alignment.py`)**: Compares PDF fret-candidate X-coordinates with MusicXML onset groups to construct diagnostic x-to-onset distance maps.
7. **Strict Build-IR Compilation (`build_ir.py`)**: Gathers all layout and timing evidence and outputs a validated `ScoreIR` Intermediate Representation. Gating is strict: any unassigned playable candidate or unboxed system blocks compilation with a `BuildIrInputRiskError`.
8. **GPIF Package Generation (`gp_package.py` / `gpif.py`)**: Compiles valid `ScoreIR` into Guitar Pro 7 binary zip packages containing compliant XML-based `Content.gpif` payloads.

---

## 2. Current Test Status

- **Status**: **99.7% Pass Rate** (389 passed, 1 skipped, 1 environment-related subprocess failure).
- **Verification**: Running pytest against the codebase executes **391 test items** representing diverse layout, timing preflight, GPIF validation, and E2E integration proof cases. 
- **Subprocess Resolution Note**: The single failure (`test_cli_diagnose_command` under `test_system_integration_diagnostics.py`) is an environmental artifact of the Windows host execution path. The test triggers a subprocess call to `python -m score2gp.cli`, which invokes the global system interpreter lacking the editable `score2gp` installation package rather than the active workspace virtual environment. This is an integration environment configuration issue, not a pipeline or code logic defect.
- **Design Invariant**: All tests are completely public-safe and driven by deterministic, synthetic fixtures, keeping copyrighted materials isolated outside Git control.

---

## 3. Current Conversion Status

- **Status**: **FAILED (Blocked at Gate MT3-B / MT3-C)**
- **Strict Conversion Status**: `fail`
- **Primary Blocker Category**: `missing_pdf_grouping` (triggered by strict safety-gate check `pdf_missing_pdf_grouping_blocks_build_ir`)
- **Generated File Existence**: `ScoreIR written (no)` / `GP written (no)`
- **Observed Counts (Major Triads Lesson 3)**:
  - Total Playable Fret Candidates: **546**
  - Fret Candidates with System: **440** (106 candidates lack system assignment)
  - Fret Candidates with String: **440**
  - Fret Candidates with Bar Box: **379** (**167 playable fret candidates are completely unassigned to any bar boundary**)
  - Grouping Status: `partial` (strict compiler gate refuses to compile unassigned fret events)

---

## 4. Observed Failures and Limitations

The raw visual PDF inspection confirms that all measures (1 to 24) and their corresponding fret text candidates exist on the printed pages. However, the geometric compiler fails due to the following systemic OMR layout parsing limitations:
1. **Notation-vs-TAB Staff Conflation**: The line grouping engine clusters horizontal vector segments locally without classifying 5-line standard notation staves versus 6-line guitar TAB staves. This results in standard note stems (56 segments) and TAB rhythm stems (36 segments) being evaluated as barlines, introducing massive telemetry clutter and false positives.
2. **Collinear System Splitting**: Unified horizontal staff systems that span the full visual margins (approx. 538 points) are fragmented by local grouping loops, splitting single visual rows into pseudo-left and pseudo-right systems (inflating system counts from 6 visual rows to 13 inferred systems on Page 1).
3. **Clipped or Short Edge Barlines**: Vertical boundaries at system edges are frequently rendered shorter than absolute crossing heights or lie outside strict bounding boxes, causing them to be rejected.
4. **Edge Boundary Fallback Rejection**: When a boundary is missing, the fallback engine attempts to infer one. However, due to horizontal system splitting and vertical notation stem duplicates near the margin coordinates, the fallback is flagged as ambiguous (`pdf_bar_box_edge_boundary_ambiguous`) and rejected.

---

## 5. Likely Root Cause Category

- **Recognition Theory & Algorithm**: The current local bounding-box and absolute tolerance model is mathematically fragile and lacks systemic structural layout awareness. It operates locally on isolated horizontal and vertical segments rather than pre-classifying staves and filtering vertical lines based on authoritative staff boundaries.
- **Algorithm & Staff Conflation**: The layout detector does not pre-classify five-line notation staves versus six-line TAB staves before grouping, resulting in horizontal line fragmentation and allowing vertical standard note stems to compete as false candidate barlines.

---

## 6. Wrong or Risky Assumptions

1. **Assumption: Local horizontal line clustering is sufficient for TAB staff-system detection.**
   - *Why it is wrong*: Horizontally split vector paths cause the same physical staff row to be grouped into separate left and right systems, breaking measure geometry.
2. **Assumption: Vertical barlines can be validated locally using absolute Y-overlap and staff crossing height thresholds.**
   - *Why it is wrong*: Conflating notation note stems above the TAB system creates duplicate, competing barline candidates that trigger global rejections.
3. **Assumption: Missing system boundaries can be inferred using local margins without page-level alignment consensus.**
   - *Why it is wrong*: Ambiguous text or rhythm stems near the margin columns cause edge fallbacks to abort, leaving systems unboxed.

---

## 7. Evidence Supporting the Conclusion

- **Page 1, System 2 & 3 Overlap**: In `extracted.tabraw.json`, `System Bar 2` covers `x=[36.7, 318.4]`, `y=[145.5, 177.4]` while `System Bar 3` covers `x=[232.8, 575.3]`, `y=[145.5, 177.4]`. They cover the exact same Y-span but represent split horizontal segments of a single visual staff row.
- **Page 1, System 7 Fallback Failure**: Edge fallback was considered and fatally rejected with the warnings `pdf_bar_box_edge_boundary_ambiguous` and `pdf_bar_box_inferred_boundary_not_enough_for_build_ir`, leaving 6 fret candidates unassigned to any bar boundary.
- **Vertical Segment Classification**: 56 vertical lines reside in the notation staff above, and 36 inside the TAB staff, clogging the barline parser with 92 false candidate boundaries and triggering 34 `pdf_barline_outside_staff_region` warnings.

---

## 8. What Should Change Next (Revised & Approved Scope)

Based on the Sceptical Verdict and the Technical Product Owner's feedback, the initially proposed **"Global Page-Level Column Grid Alignment System"** has been **rejected** as out of scope due to extreme fragility, page-wide column consensus errors on non-uniform sheets, and high overfitting risk.

Instead, we must transition the PDF layout engine to utilize **robust, local deterministic layout algorithms** under `src/score2gp/pdf.py`:

1. **Horizontal Collinear Line Merging**: Pre-merge horizontal vector segments that share the same Y-coordinate and are collinear or overlap within a horizontal gap tolerance (e.g., 10.0 points) before performing line grouping. This consolidates left/right fragments into a single authoritative staff row, completely eliminating collinear system splitting.
2. **TAB-vs-Notation Staff Pre-Classification**: Pre-classify horizontal groupings. Guitar TAB staves must have exactly six strings (or be verified as TAB staves). Standard 5-line notation staves must be identified and strictly excluded from forming or cluttering TAB systems.
3. **TAB-Grid Intersect Filtering**: When filtering vertical line segments (candidate barlines), match them strictly based on whether they cleanly intersect the Y-extent of the authoritative 6-string TAB staff region. Vertical paths that lie entirely inside the notation staff (note stems/beams) or are too short (rhythm stems inside the TAB staff) must be ignored, drastically reducing candidate barline telemetry noise.

---

## 9. Smallest Useful Implementation Slice

1. **Horizontal Collinear Merging**: Refactor horizontal line processing in `src/score2gp/pdf.py` to merge collinear or overlapping horizontal vector segments within a horizontal gap tolerance of 10.0 points.
2. **Pre-grouping segment merging**: Incorporate this merging into `_tab_line_groups` to ensure staff lines are grouped as solid, full-width rows.
3. **TAB-vs-Notation Pre-Classification**: Isolate standard 5-line notation staves and ignore them when forming TAB systems.
4. **TAB-Grid Intersect Filtering**: Match barlines strictly against the Y-extent of the six-string TAB staff coordinates to ignore notation-only note stems and TAB rhythm stems.

---

## 10. Files and Modules Likely to Change

- **`src/score2gp/pdf.py`**: Refactoring of horizontal line processing, pre-grouping line merging, and vertical candidate filtering.
- **`tests/test_pdf.py`**: Unit tests verifying collinear merging and staff pre-classification.

---

## 11. Tests Proving the Change

- **Synthetic Public Fixture**: `tests/fixtures/pdf/generated_paired_notation_tab_system.pdf` (representing a standard notation staff paired directly above a six-string TAB staff, complete with notation-only stems, TAB rhythm stems, and a missing left edge boundary on one system).
- **Test Assertions**:
  1. Verify the standard 5-line notation staff is ignored and does not form a TAB system.
  2. Confirm the 6-line TAB staff is grouped as exactly one visual row spanning the full margins.
  3. Assert that vertical note stems inside the notation staff are ignored as barlines.
  4. Verify that all fret candidates assign cleanly to strings and bars with zero unassigned playable tokens.

---

## 12. Risks and Backout Plan

- **Risk**: Over-merging horizontal segments could group unrelated annotations or chord symbols if they happen to line up horizontally.
- **Backout Plan**:
  - Keep the horizontal gap tolerance narrow (e.g., 10.0 points) so that only true collinear staff line segments are merged.
  - Rely strictly on the 5-string/6-string structure and gaps criteria in `classify_staff_line_group` to filter out any malformed segments.

---

## 13. Recommendation

- **Clear Recommendation: PROCEED with local geometric layout refinements**
  - Proceed to implement collinear horizontal merging, paired TAB pre-classification, and TAB-grid intersection filtering under the narrowed constraints defined by the TPO.
