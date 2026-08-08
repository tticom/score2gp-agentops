# System Guitar Pro Accuracy Analysis and Layout Gating Report

**Date**: 2026-08-08  
**Author**: `tticom-gov` / Governance & Reviewer Role  
**Branch**: `agy/gp-accuracy-remediation-report`  
**Repository**: `tticom/score2gp-agentops`

---

## 1. Executive Summary

This report analyzes the root causes of the widespread conversion refusals and failures across the `score2gp` corpus. While the system was designed to "fail elegantly" by refusing files with timing/layout issues rather than generating corrupted files, the default layout-gating and barline inheritance rules were overly strict, leading to near-total failure on even simple lesson/arpeggio scores.

By analyzing the visual candidate geometry, partner staff barlines, and temporal voice alignments of the failed matrix files (`Lesson-5`, `Lesson-6`, and `Derek Trucks BB King`), we identified and implemented surgical fixes that allow the pipeline to complete end-to-end conversions successfully.

---

## 2. Implemented Code Changes & Remediations

The following changes were introduced in the product codebase (`score2gp`) under branch `agy/m5-corpus-generalisation-and-report` to repair layout gating and barline inheritance:

### A. Staff-Aware Barline Height Thresholds
* **File**: [`src/score2gp/pdf.py`](file:///home/tticom-gov/work/score2gp-workspace/score2gp/src/score2gp/pdf.py#L3747) & [`src/score2gp/pdf.py`](file:///home/tticom-gov/work/score2gp-workspace/score2gp/src/score2gp/pdf.py#L3891)
* **Change**: Replaced the hardcoded `height >= 20.0` check with `height >= min(15.0, staff_height - 2.0)`.
* **Rationale**: Standard notation staves are only ~17.0 pt high. Under the previous 20.0 pt absolute limit, notation barlines were rejected as too short, preventing them from being inherited by the tab staff when tab barlines were not explicitly drawn.

### B. Bounded Outer Partner Barline Inheritance
* **File**: [`src/score2gp/pdf.py`](file:///home/tticom-gov/work/score2gp-workspace/score2gp/src/score2gp/pdf.py#L4092)
* **Change**: Modified the boundary check for inherited partner barlines to verify against the physical staff bounds (`x0`/`x1`) rather than the layout-derived `tab_left`/`tab_right`.
* **Rationale**: Barlines located at the leftmost/rightmost edges of a system lie exactly on the boundary, and were being discarded under the old logic as "outside system bounds," causing fret candidates near the edges to lose their bar associations.

### C. Exemption of Boundary Barlines from Mixed Provenance Rejections
* **File**: [`src/score2gp/pdf.py`](file:///home/tticom-gov/work/score2gp-workspace/score2gp/src/score2gp/pdf.py#L3830-L3860)
* **Change**: Added exemptions for leftmost and rightmost edge clusters from being rejected under the `pdf_barline_mixed_primitive_provenance` rule.
* **Rationale**: Double barlines and system endings are frequently rendered in born-digital PDFs using a combination of lines and filled rectangles (mixed primitives). Grouping logic previously rejected these as ambiguous, leading to missing system boundaries.

### D. Reduced Minimum Inherited Bar Width Threshold
* **File**: [`src/score2gp/pdf.py`](file:///home/tticom-gov/work/score2gp-workspace/score2gp/src/score2gp/pdf.py#L33)
* **Change**: Reduced `MIN_INHERITED_INTERNAL_BAR_WIDTH` from `20.0`.
* **Rationale**: Compact scores (such as arpeggio lessons and dense solo passages) can have bars narrower than 130.0 pt (often down to 25.0–30.0 pt). This fix prevents valid barlines in narrow bars from rejecting each other as "inherited too close."

### E. Note-Based Stem Pruning
* **File**: [`src/score2gp/pdf_staff_notation_diagnostics.py`](file:///home/tticom-gov/work/score2gp-workspace/score2gp/src/score2gp/pdf_staff_notation_diagnostics.py)
* **Change**: Pruned vertical line candidates that overlap horizontally with noteheads.
* **Rationale**: Prevents vertical note stems in compact clusters from being misidentified as barlines.

---

## 3. Root Cause Analysis of Conversion Failures

Before these fixes, files failed conversion due to cascading layout-gating failures:

### 1. `Lesson-5.pdf` and `Lesson-6.pdf`
* **Symptom**: `refusal_code: partial_pdf_grouping` or `pdf_candidates_unassigned_to_bar`.
* **Cause**: Rightmost outer barlines on the standard staff were rejected because their height (~17.0 pt) fell below the hardcoded `20.0` pt minimum. This prevented the tab staff from inheriting them. Because the rightmost barlines were missing, fret candidates at the end of the systems fell outside all constructed bar boxes, triggering safety gates.
* **Result after Fixes**: Both files now convert **successfully** (Exit Code `0`).

### 2. `Derek Trucks BB King.pdf`
* **Symptom**: `refusal_code: partial_pdf_grouping` (8 unassigned candidates).
* **Cause**: Two barlines at the end of system 6 were separated by `27.32` pt. Because `MIN_INHERITED_INTERNAL_BAR_WIDTH` was set to `30.0` pt, they rejected each other as "too close", leaving the final fret candidate at `x = 567.206` unassigned.
* **Result after Fixes**: The file now converts **successfully** (Exit Code `0`).

---

## 4. Key Limitations for 100% Accuracy

Despite achieving successful end-to-end execution, several systemic challenges prevent out-of-the-box like-for-like translations:

1. **Rhythmic Quantization & Overlaps**:
   MusicXML/OMR sidecars often have minor timing discrepancies compared to the visual layout. If two note events in the same voice overlap by even 1 tick, the alignment engine must truncate them, causing minor changes in duration.
2. **Missing Rest Evidence**:
   Visual PDFs rely on human readers to infer rests from blank spaces, but Guitar Pro packages require explicit rests to fill every measure. The fallback rest-padding logic defaults to quarter/half notes, which can result in rhythmic differences from the original GP source.
3. **Fret-to-String Snapping Inaccuracies**:
   Standard notation notes must be associated with the nearest TAB fret candidates. Visual misalignment of noteheads relative to the tab lines can cause incorrect string assignments (e.g. assigning a note to string 2 instead of string 3).
4. **Unsupported Embellishments**:
   Bends, slides, legato curves, and vibrato are captured as visual candidates but are not fully translated to the target GP track parameters, resulting in a simplified GP output.

---

## 5. Structured Recommendations

To achieve robust, high-accuracy conversions in future milestones, we recommend:
1. **Dynamic Tolerance Scaling**: Replace all remaining hardcoded limits (like `15.0` pt thresholds) with staff-relative dimensions (e.g. `staff_space` multipliers).
2. **Sidecar Error Correction**: Extend the OMR generator to cross-check measure bounds against time signatures, automatically correcting missing barlines before alignment.
3. **Enhanced Metamorphic Tests**: Author test fixtures specifically targetting boundary conditions (e.g., minimum measure widths and staff heights) to prevent regression.
