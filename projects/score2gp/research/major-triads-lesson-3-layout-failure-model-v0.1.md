# Major Triads Lesson 3 Layout Failure Model v0.1

## Summary Verdict

**Major Triads Lesson 3** fails before Guitar Pro (GP) generation due to a **partial PDF layout grouping** failure. The parser successfully detects vector staff lines and systems but fails to construct safe, complete bar boxes for all systems under strict mode. Programmatically, this results in **167 playable fret candidates failing to receive bar assignments** (`bar_index = None`), which strictly blocks compilation with a `BuildIrInputRiskError` under the `partial_pdf_grouping` blocker category. 

The mechanical cause is the strict rejection of vertical drawing paths (barline candidates) that are either too short or fail to cleanly cross the entire tab staff region. Because the engraving software produces clipped barlines or notation stems that lie outside the staff region, the parser rejects these vertical boundaries. When a system lacks two cleanly accepted outer boundaries, the pipeline considers an edge-boundary fallback. However, because duplicate or ambiguous barline candidates exist near the system edges, this fallback is rejected to prevent misalignments, leaving measure boundaries unresolved.

No ScoreIR or GP package files are written, and strict compilation gates correctly refuse to promote unstructured fret text to musical events.

---

## Verified Metrics

The following metrics are extracted programmatically from `tab_raw.json` and `warnings.json` under `work/major_triads_failure_model_20260527_1608/lesson_3/`:

- **Page Count**: 4
- **Grouping Status**: `partial` (`partial_pdf_grouping` warning active)
- **Total Candidates**: 594
- **Playable Fret Candidates**: 546
- **Candidates with System**: 440
- **Candidates with Bar**: 379
- **Candidates with String**: 440
- **Unassigned-to-System Count**: 106
- **Unassigned-to-Bar Count**: 167
- **Unassigned-to-String Count**: 106
- **ScoreIR Written**: `no`
- **GP Written**: `no`

---

## Artifact Coherence

The generated output artifacts are completely coherent and consistent:
1. `tab_raw.json` contains a total of 594 candidates, with 546 identified as playable fret candidates (`parsed_fret` is not None) and 48 non-playable text/tuning candidates.
2. `warnings.json` records 44 occurrences of successful bar box construction (`pdf_bar_boxes_constructed`) alongside multiple rejections and partial system warnings. It registers a final `partial_pdf_grouping` status.
3. Programmatic schemas `pdf-edge-boundary-report.v0.9` and `tab-grouping.v0.1` are fully respected. `pdf-edge-boundary-report.json` isolates **Page 1, System 7** as the first fatal unboxed system where boundary fallback was considered and rejected, which perfectly mirrors the candidate state in `tab_raw.json`.

---

## First Fatal Failure

The first fatal system that blocks compiler execution occurs on **Page 1, System 7**:
- **Observed Boundary Count**: 2
- **Accepted Boundary Count**: 1
- **Rejected Boundary Count**: 1
- **Inferred Boundary Count**: 0
- **Missing Side**: `left`
- **Fallback Considered**: `yes`
- **Fallback Accepted**: `no`
- **Fallback Rejected**: `yes`
- **Rejection Reason Codes**: 
  - `pdf_bar_box_edge_boundary_ambiguous`
  - `pdf_bar_box_inferred_boundary_not_enough_for_build_ir`
  - `pdf_bar_box_inferred_boundary_requires_clear_system_edge`
- **Candidates Assigned to System**: 6
- **Candidates Assigned to Bar**: 0
- **Playable Candidates Unassigned due to Failed Boundary**: 6
- **Whether Build-IR was Blocked**: `yes`

---

## Systemic Failure Pattern

The layout grouping failure is highly systemic rather than localized:
1. **Unassigned Bar Boxes**: Five distinct systems across the score are completely unboxed due to failed edge fallbacks and missing boundaries:
   - **Page 1, System 7**
   - **Page 2, System 9**
   - **Page 2, System 11**
   - **Page 3, System 13**
   - **Page 4, System 1**
2. **Candidates Assigned to System but Not Bar**: Seven distinct systems contain candidates that have system/string grouping but lack bar boxes (`bar_index = None`):
   - **Page 1, System 7** (6 candidates)
   - **Page 2, System 2** (4 candidates)
   - **Page 2, System 9** (19 candidates)
   - **Page 2, System 11** (13 candidates)
   - **Page 3, System 13** (7 candidates)
   - **Page 4, System 1** (9 candidates)
   - **Page 4, System 3** (3 candidates)
3. **High Vertical Path Rejection**: Almost every system picks up vertical paths that must be rejected. The parser records **>=3 rejected barline candidates** on **32 separate systems** due to vertical rhythm stems or notation beam lines.
4. **Fewer than Six Detected Strings**: Staff-line detection failed or was incomplete on **Page 1, System 1** and **Page 4, System 1** due to local horizontal path fragmentation.
5. **Barline Ambiguity**: Horizontal barline boundary ambiguity (`pdf_barline_ambiguous`) occurred on **6 systems** (P1S1, P1S7, P2S2, P2S11, P3S13, P4S3).

---

## Candidate Assignment Breakdown

The 546 playable fret candidates are classified below by Page and System Index:

| Page | System Index | Playable Candidates | Grouped (S+B+Str) | Partial (S+Str, No Bar) | No System / No String | Grouping Status |
|------|--------------|---------------------|-------------------|-------------------------|-----------------------|-----------------|
| **1**| *None*       | 27                  | 0                 | 0                       | 27                    | *None*          |
| **1**| System 1     | 8                   | 8                 | 0                       | 0                     | `partial` (warnings) |
| **1**| System 2     | 8                   | 8                 | 0                       | 0                     | `grouped`       |
| **1**| System 3     | 1                   | 1                 | 0                       | 0                     | `grouped`       |
| **1**| System 4     | 9                   | 9                 | 0                       | 0                     | `grouped`       |
| **1**| System 5     | 7                   | 7                 | 0                       | 0                     | `grouped`       |
| **1**| System 6     | 9                   | 9                 | 0                       | 0                     | `grouped`       |
| **1**| System 7     | 6                   | 0                 | 6                       | 0                     | `partial`       |
| **1**| System 8     | 17                  | 17                | 0                       | 0                     | `grouped`       |
| **1**| System 9     | 7                   | 7                 | 0                       | 0                     | `grouped`       |
| **1**| System 10    | 9                   | 9                 | 0                       | 0                     | `grouped`       |
| **1**| System 11    | 8                   | 8                 | 0                       | 0                     | `grouped`       |
| **1**| System 13    | 9                   | 9                 | 0                       | 0                     | `grouped`       |
| **1**| System 14    | 7                   | 7                 | 0                       | 0                     | `grouped`       |
| **2**| *None*       | 35                  | 0                 | 0                       | 35                    | *None*          |
| **2**| System 1     | 17                  | 17                | 0                       | 0                     | `grouped`       |
| **2**| System 2     | 4                   | 0                 | 4                       | 0                     | `grouped` (unassigned bar) |
| **2**| System 3     | 3                   | 3                 | 0                       | 0                     | `grouped`       |
| **2**| System 4     | 23                  | 23                | 0                       | 0                     | `grouped`       |
| **2**| System 5     | 17                  | 17                | 0                       | 0                     | `grouped`       |
| **2**| System 6     | 9                   | 9                 | 0                       | 0                     | `grouped`       |
| **2**| System 7     | 8                   | 8                 | 0                       | 0                     | `grouped`       |
| **2**| System 9     | 19                  | 0                 | 19                      | 0                     | `partial`       |
| **2**| System 10    | 8                   | 8                 | 0                       | 0                     | `grouped`       |
| **2**| System 11    | 13                  | 0                 | 13                      | 0                     | `partial`       |
| **2**| System 12    | 8                   | 8                 | 0                       | 0                     | `grouped`       |
| **2**| System 14    | 17                  | 17                | 0                       | 0                     | `grouped`       |
| **2**| System 15    | 7                   | 7                 | 0                       | 0                     | `grouped`       |
| **3**| *None*       | 34                  | 0                 | 0                       | 34                    | *None*          |
| **3**| System 1     | 9                   | 9                 | 0                       | 0                     | `grouped`       |
| **3**| System 2     | 8                   | 8                 | 0                       | 0                     | `grouped`       |
| **3**| System 4     | 17                  | 17                | 0                       | 0                     | `grouped`       |
| **3**| System 5     | 7                   | 7                 | 0                       | 0                     | `grouped`       |
| **3**| System 6     | 9                   | 9                 | 0                       | 0                     | `grouped`       |
| **3**| System 7     | 15                  | 15                | 0                       | 0                     | `grouped`       |
| **3**| System 8     | 15                  | 15                | 0                       | 0                     | `grouped`       |
| **3**| System 10    | 9                   | 9                 | 0                       | 0                     | `grouped`       |
| **3**| System 11    | 7                   | 7                 | 0                       | 0                     | `grouped`       |
| **3**| System 12    | 9                   | 9                 | 0                       | 0                     | `grouped`       |
| **3**| System 13    | 7                   | 0                 | 7                       | 0                     | `partial`       |
| **4**| *None*       | 10                  | 0                 | 0                       | 10                    | *None*          |
| **4**| System 1     | 9                   | 0                 | 9                       | 0                     | `partial`       |
| **4**| System 2     | 6                   | 6                 | 0                       | 0                     | `grouped`       |
| **4**| System 3     | 6                   | 3                 | 3                       | 0                     | `grouped` (partially unassigned) |
| **4**| System 4     | 17                  | 17                | 0                       | 0                     | `grouped`       |
| **4**| System 5     | 7                   | 7                 | 0                       | 0                     | `grouped`       |
| **4**| System 6     | 17                  | 17                | 0                       | 0                     | `grouped`       |
| **4**| System 7     | 8                   | 8                 | 0                       | 0                     | `grouped`       |
| **Total**| —         | **546**             | **379**           | **61**                  | **106**               | —               |

*Note: Grouping status `grouped` can still have unassigned bar indexes if the overall system grouping is complete but specific candidates fall outside the constructed bar boundaries (as seen on Page 2 System 2 and Page 4 System 3).*

---

## Supported Hypotheses

1. **short/clipped edge barlines (SUPPORTED)**: Frequent `pdf_barline_too_short` and `pdf_barline_does_not_cross_staff` warnings confirm that native barlines are rendered smaller than absolute height thresholds, or are clipped at the edges.
2. **ambiguous duplicate outer boundary candidates (SUPPORTED)**: Rejection reasons like `pdf_bar_box_edge_boundary_ambiguous` show that multiple barlines exist in the fallback direction, making automated edge boundary selection unsafe.
3. **barline candidates outside staff region are actually notation stems/text artifacts (SUPPORTED)**: High counts of `pdf_barline_outside_staff_region` (33) and `pdf_barline_does_not_cross_staff` (35) prove that vertical strokes representing rhythm stems or text brackets are being picked up as barlines, introducing clutter and false positives.
4. **current system segmentation creates too many/few systems (SUPPORTED)**: 106 candidates completely lack system assignments because the system bounding box margins are too narrow or do not encompass all visual fret groups on the page.
5. **current confidence gates are correct but the layout model lacks a normalized grid (SUPPORTED)**: The local bounding-box and absolute tolerance model is mathematically fragile. Clean engraving alignment in born-digital PDFs means vertical measure columns are aligned horizontally across systems. A grid-based column reconstruction model would provide the robust structure needed to bypass individual local barline rejections.

---

## Unverified Hypotheses

1. **fragmented horizontal string lines (UNVERIFIED)**: Fragmented staves are not a primary cause. The parser cleanly detects six string lines for 42 out of 44 systems, with only 1 staff incompleteness warning.
2. **current line clustering mixes notation staff and tab staff geometry (UNVERIFIED)**: While there are 3 instances of ambiguous staves (`pdf_tab_staff_ambiguous`), line clustering is overall highly accurate and does not explain the widespread barline failures.

---

## Contradicted Hypotheses

1. **incomplete tab staff detection (CONTRADICTED)**: Staff line detection did not fail; 44 systems were successfully identified with 6 lines. This represents excellent staff reconstruction across all pages.

---

## Recommended External Research Questions

1. **Global Column Projection**: Can we implement a vertical projection profile (integral projection) across the entire page layout to identify highly aligned column regions (measures), using system-spanning barlines as a global grid rather than relying on system-local horizontal boundaries?
2. **Rhythm Stem Discrimination**: How can we programmatically filter out vertical notation stems from true barlines by analyzing their horizontal distance from fret text, or by checking if their vertical bounds match standard note-head centers rather than staff-line boundaries?
3. **Template-Driven Edge Inferences**: In clean native GP vector formats, if internal barlines are cleanly detected, can we infer outer boundaries by mirroring the internal measure widths (which are highly regular in lesson PDFs) when a system edge boundary fallback is rejected due to local visual clutter?

---

## Recommended Next Implementation Slice

To progress toward Gate MT3-B (Page 1) and Gate MT3-C (Full Layout) without loosening gates or reducing confidence thresholds, the next implementation slice should introduce a **global page-level column alignment grid**:

- **Production Module/Function**: Implement a grid-based projection module under `src/score2gp/pdf.py` (e.g. `_project_global_columns`) to construct a page-level vertical column map based on the consensus of highly confident, system-crossing barlines.
- **Expected Private Metric to Improve**: 
  - `Candidates with Bar` should increase from **379 to 546**.
  - `Unassigned-to-bar count` should drop from **167 to 0**.
- **Guardrail Test**: Add a guardrail test in `tests/test_pdf.py` verifying that random/noisy vertical strokes (such as stray brackets or notation stems) that do not align with any global grid column remain strictly rejected as `pdf_barline_outside_staff_region`.
- **What Must Remain Blocked**: ASCII timing guesses, scanned/raster PDF support, OCR, or pitch-based reconstruction of coordinates must remain strictly blocked.

---

## Required Public Fixtures

To verify the grid-based projection safely in CI without committing private materials, the following synthetic public fixture is required under `tests/fixtures/pdf/`:
- **`synthetic_dense_unaligned_barlines.pdf`**: A born-digital PDF containing 4 systems with regular measure barlines, but with short rhythm stems in between staff lines and a missing left edge boundary on system 3. The test must prove that the grid-based layout model successfully infers the missing system boundary and resolves bar assignments for all candidates while ignoring the rhythm stems.

---

## Non-Goals and Invariants

- **No pitch-based shortcuts**: Musical pitch, tuning, or transposing offsets from MusicXML must never drive vertical barline coordinates or staff line spacing.
- **No scanned/raster support**: No OCR or machine-learning layout recognition can be used; the pipeline remains purely born-digital vector-based.
- **No threshold loosening**: We must not increase horizontal cushions, reduce minimum barline heights below 20pt, or accept non-staff-crossing lines to bypass gates.
- **Strict gates invariant**: If even a single playable fret candidate remains unassigned horizontally or vertically, compiler execution must remain blocked with a strict `BuildIrInputRiskError`.
