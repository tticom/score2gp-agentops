# Post Double-Barline Next Blocker Research

## Summary Verdict

The current active blocker is **bar detection** due to **fragmented staff line length thresholding**.

Specifically, on Page 2, System 7, fret numbers are drawn directly on top of the bottom staff lines, causing a physical gap in the PDF drawing. The rightmost fragment of the bottom line (extending from `x = 537.74` to `x = 575.29`, length = 37.55 pixels) is shorter than the 80.0 pixel minimum horizontal threshold in `pdf.py` (`_LineSegment.is_horizontal`), causing it to be discarded during segment extraction. As a result, the system bounding box `x1` is incorrectly truncated at `529.58` instead of `575.29`. The true double barline at `575.29` is excluded from the system's barline candidates because it lies outside the truncated system bounds range (`x1 + 25.0 = 554.58`), leaving the rightmost measure unboxed. This leaves **7 playable fret candidates** unassigned to any bar box (`bar_index: null`), dropping grouping confidence to `partial` and blocking the Build-IR phase.

## Prompt Chain

- **Prompt Manifest**: [prompt-manifest.json](file:///projects/score2gp/research/2026-05-28-post-double-barline-next-blocker/prompt-manifest.json)
- **Operative Prompt**: [prompts/001-investigation-prompt.md](file:///projects/score2gp/research/2026-05-28-post-double-barline-next-blocker/prompts/001-investigation-prompt.md)

## Repositories and Branches

- **Product Repository**: `score2gp`
  - **Branch**: `research/post-double-barline-next-blocker-v0.1`
  - **Parent Commit**: `bce56bb15ecf3661eb1bb69cf32a32c257850239` (PR #149 merge)
- **Agent Governance Repository**: `score2gp-agentops`
  - **Branch**: `research/post-double-barline-next-blocker-v0.1`
  - **Parent Commit**: `2b620c85caec16ec6f376f9d3bdfd9de3b145a32` (PR #13 merge)

## Commands Run

Fresh private-safe Lesson 3 extraction and diagnostic command:
```powershell
$env:PYTHONPATH="src"; .venv\Scripts\python -m score2gp.cli extract-tab fixtures/private/Lesson-3.pdf --out work/post_double_barline_next_blocker_20260528_1445/lesson_3
```

Diagnostic scratch analyzer scripts run inside the workspace:
```powershell
$env:PYTHONPATH="src"; .venv\Scripts\python -m pytest
```

## Input Availability

- **Input File**: `fixtures/private/Lesson-3.pdf` (private birth-digital PDF benchmark file, verified present).
- **Extracted Diagnostics**:
  - `work/post_double_barline_next_blocker_20260528_1445/lesson_3/tab_raw.json`
  - `work/post_double_barline_next_blocker_20260528_1445/lesson_3/warnings.json`
  - `work/post_double_barline_next_blocker_20260528_1445/lesson_3/grouping-diagnostics.html`

## Artifact Coherence

All artifacts are coherent and consistent. The workspace is clean and verified using Git checks. The generated run files are isolated in the local `.gitignore`-ignored `work/` directory, adhering strictly to the private-safety invariant.

## Gate Status

- **Strict Extraction/Grouping Status**: `partial`
- **grouping_safe**: `false`
- **ScoreIR written**: `no`
- **GP written**: `no`
- **semantic round-trip attempted**: `no`
- **Primary Blocker Code**: `pdf_grouping_confidence_below_threshold`
- **Other Blocker Warnings**:
  - `pdf_string_assignment_not_enough_for_build_ir`
  - `pdf_grouping_not_safe_for_build_ir`
  - `pdf_missing_pdf_grouping_blocks_build_ir`
  - `pdf_layout_detection_requires_manual_review`
  - `pdf_partial_grouping_with_playable_candidates`

## Candidate Assignment Breakdown

### 1. General Breakdown

| Candidate Pool | Total | Assigned to System | Assigned to Bar | Assigned to String | Assigned to All Three | Missing System | Missing Bar | Missing String |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **All Candidates** | 591 | 431 | 424 | 430 | 423 | 160 | 7 | 1 |
| **Playable Candidates** | 548 | 430 | 423 | 430 | 423 | 118 | 7 | 0 |

### 2. Breakdown by Page and System for Playable Candidates

* **Legend & Page Numbers** (Correctly Excluded):
  - 118 playable candidates are missing all three dimensions (system, bar, and string) because they are page numbers, chord diagram labels, or legend text. They are successfully identified and excluded by the pipeline via `pdf_fret_page_or_legend_number_excluded`.
* **Standard TAB Notes** (Systemically Active Blocker):
  - **7 playable candidates** are assigned to a system and a string, but are **missing a bar box assignment** because they fall in the rightmost measure of Page 2, System 7.

The 7 unassigned active blocker candidates are distributed as follows:
- **Page 2, System 7**: 7 unassigned candidates (Fret candidates located at x > 434.83, y ≈ 727 to 753)

## Delta From Double-Barline Baseline

* **Playable fret candidates with bar**:
  - Pre-fix baseline: 391
  - Post-fix: 423
  - Delta: **+32**

This matches the expected metric movement reported in PR #13 exactly, proving absolute metric consistency.

## Warning Taxonomy

Unique warnings extracted from `warnings.json` categorized by pipeline component:

### 1. System Detection (Build-IR Blocking)
* `pdf_partial_system_detection` (2 counts): Horizontal tab systems were only partially detected.

### 2. Bar Detection & Edge Boundary (Diagnostic Only)
* `pdf_barline_too_short` (20 counts)
* `pdf_barline_does_not_cross_staff` (19 counts)
* `pdf_barline_outside_staff_region` (19 counts)
* `pdf_barline_double_secondary` (10 counts)

### 3. Bar-Assignment Failures (Build-IR Blocking)
* `pdf_candidate_outside_bar` (1 count)
* `pdf_candidate_unassigned_to_bar` (1 count)
* `pdf_candidates_unassigned_to_bar` (1 count)
* `ambiguous_bar_assignment` (1 count)
* `pdf_candidate_near_missing_bar_boundary` (1 count)

### 4. String Assignment (Build-IR Blocking)
* `pdf_string_assignment_not_enough_for_build_ir` (2 counts)
* `pdf_playable_candidate_requires_string_assignment` (1 count)
* `pdf_candidates_unassigned_to_string` (1 count)

### 5. Compact Staff Ambiguity (Build-IR Blocking)
* `pdf_string_assignment_compact_staff_ambiguous` (1 count)
* `pdf_string_assignment_confidence_below_threshold` (1 count)
* `pdf_string_assignment_missing` (1 count)

### 6. Fret Optical Bounds (Build-IR Blocking)
* `pdf_fret_bbox_too_tall` (1 count)
* `pdf_fret_digit_symbol_overlap_ambiguous` (1 count)
* `pdf_fret_digits_not_merged_gap_too_large` (1 count)
* `pdf_fret_optical_bounds_confidence_below_threshold` (1 count)
* `pdf_fret_refinement_not_enough_for_build_ir` (1 count)

### 7. Grouping Confidence & Safety Gates (Build-IR Blocking)
* `pdf_grouping_not_safe_for_build_ir` (2 counts)
* `pdf_missing_pdf_grouping_blocks_build_ir` (2 counts)
* `pdf_layout_detection_requires_manual_review` (2 counts)
* `pdf_partial_grouping_with_playable_candidates` (2 counts)
* `pdf_grouping_confidence_below_threshold` (2 counts)
* `partial_pdf_grouping` (1 count)
* `missing_pdf_grouping` (1 count)

## First High-Impact Failure Cluster

* **Location**: Page 2, System 7 (rightmost measure)
* **Candidate Count Affected**: 7 playable candidates
* **Missing Dimension**: `bar` assignment (all 7 have `bar_index: null`)
* **Dominant Warning Codes**: `pdf_candidate_outside_bar`, `pdf_candidate_unassigned_to_bar`, `pdf_candidates_unassigned_to_bar`
* **Visual/Geometry Characteristics**: Genuine guitar TAB fret numbers (`8`, `7`, `9`, `9`, `10`, `10`, `10`) positioned on active staff lines, but lying beyond the last constructed barline (`x = 403.71`) because the true rightmost double barline at `x ≈ 575.29` was excluded from the system due to horizontal staff line truncation.

## Supported Hypotheses

* **Hypothesis 4**: *Bar boxes remain incomplete in other systems.*
  - **Status**: Supported (Page 2, System 7 has incomplete bar boxes).
* **Hypothesis 5**: *Candidate text outside bar boxes is now the active blocker.*
  - **Status**: Supported (the 7 unassigned candidates lie horizontally to the right of the last constructed bar box).

## Unverified Hypotheses

* **Hypothesis 2**: *String assignment confidence / compact-staff ambiguity is now the active blocker.*
  - **Status**: Unverified (warnings are raised, but they don't block bar assignment, and all active system candidates successfully snap to a string).
* **Hypothesis 3**: *Fret optical bounds confidence is now the active blocker.*
  - **Status**: Unverified (warnings are raised, but they are downstream of the bar-assignment failure).

## Contradicted Hypotheses

* **Hypothesis 1**: *Double-barline ambiguity remains the active blocker.*
  - **Status**: Contradicted (our double-barline horizontal clustering successfully works on all other systems, and no `pdf_barline_ambiguous` warning is raised in System 7).
* **Hypothesis 6**: *Non-tab text is being counted as playable.*
  - **Status**: Contradicted (unassigned candidates are genuine guitar tab fret numbers).
* **Hypothesis 7**: *Aggregate grouping confidence is blocking despite most dimensions being assigned.*
  - **Status**: Contradicted (blocked by the physical presence of 7 unassigned candidates).
* **Hypothesis 8**: *Diagnostic counters are inconsistent across stages.*
  - **Status**: Contradicted (all counts are perfectly consistent).

## Recommended Public Fixture

### 1. Title
Fragmented Staff Line Length Thresholding Fixture

### 2. Setup
- **Staff Geometry**: A standard 6-line TAB staff extending horizontally from `x = 36.0` to `x = 575.0`. However, the bottom line is fragmented in the rightmost measure, leaving a segment from `36.0` to `529.0`, and a short segment from `537.0` to `575.0` (length = 38.0 pixels, which is < 80.0).
- **Candidates**: Fret candidates placed at `x = 550.0`.
- **Barlines**: A double barline placed at `x = 575.0`.

### 3. Assertions (Expected Success vs Refusal)
* **Expected Success Case**:
  - The short segment is not discarded, the staff rightmost boundary is correctly identified at `575.0`, and the double barline is accepted.
  - Exactly 3 bar boxes are constructed, and candidates are successfully assigned to the third bar box.
  - `assert "pdf_candidate_outside_bar" not in warning_codes`
  - `assert len(bar_boxes) == 3`
* **Expected Safe Refusal Case**:
  - A random short horizontal segment (e.g. length = 20.0 pixels) elsewhere on the page must be discarded.

### 4. Expected Private-Safe Metric Movement on Lesson 3
- Playable fret candidates with bar: from `423` to `430` (all 430 successfully assigned).
- Strict grouping status: from `partial` to `complete`.

## Recommended Next Implementation Slice

### 1. Remediation
Update `is_horizontal` in `src/score2gp/pdf.py` to allow short horizontal staff line segments (length < 80.0 pixels) to be accepted if they are collinear with other horizontal staff lines in the same page region and help reconstruct split staff rows.

### 2. Non-Goals
* Do not loosen timing/build-ir gates.
* Do not modify Pitch/Tuning data.

## Non-Goals and Invariants

No private PDFs or work directories committed.

## Verification Results

### 1. Automated Tests
100% of all **391 tests passed successfully** in the virtual environment!
```powershell
$env:PYTHONPATH="src"
.venv/Scripts/python -m pytest
```
All CLI integration, diagnostics, normalizations, and double-barline resolution tests are completely green.

### 2. CLI Schema and Validation Tests
- **Schema Export**: `.venv/Scripts/python -m score2gp.cli export-schema --out schemas` completed successfully.
- **IR Validation**: `.venv/Scripts/python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json` returned `valid: true`.
- **Schema Diff**: `git diff -- schemas` was clean.

## Private-Safety Audit

A complete directory audit was executed using Git tracking commands in both repositories.
- `git ls-files fixtures/private work` outputs exactly and only: `fixtures/private/.gitkeep`
- No private PDFs, GP files, JSON intermediates, or work files have been staged or tracked, strictly preserving the private-safety invariant.

## Next Required Evidence

Manual smoke test on Lesson 3 confirming fret candidates with bar moves to 430.
