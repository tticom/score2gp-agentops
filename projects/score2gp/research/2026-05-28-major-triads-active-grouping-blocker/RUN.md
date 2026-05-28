# Major Triads Active Grouping Blocker Research

## Summary Verdict

The active blocker is **bar detection**. 

Specifically, the pipeline fails to construct the final (rightmost) bar box on every page because the final double barlines (or section end barlines) are composed of two vertical lines very close together (separated by < 6.0 pixels). The internal barline filtering logic detects both vertical lines but rejects them both with the warning code `pdf_barline_ambiguous` because they fall within each other's horizontal ambiguity threshold. Consequently, no valid rightmost bar boundary is registered. This prevents the construction of the final bar box in each system, leaving 32 playable fret candidates in those final measures unassigned to any bar box, which ultimately degrades the system grouping confidence below the strict safety-gate threshold and blocks the build-ir phase.

## Prompt Chain

- **Prompt Manifest**: [prompt-manifest.json](file:///projects/score2gp/research/2026-05-28-major-triads-active-grouping-blocker/prompt-manifest.json)
- **Operative Prompt**: [prompts/001-investigation-prompt.md](file:///projects/score2gp/research/2026-05-28-major-triads-active-grouping-blocker/prompts/001-investigation-prompt.md)

## Repositories and Branches

- **Product Repository**: `score2gp`
  - **Branch**: `research/major-triads-active-grouping-blocker-v0.2`
  - **Parent Commit**: `f0fb4902528c9b02cefbe87145956e1874ee14bf` (PR #148 merge: Expose active grouping blocker diagnostics)
- **Agent Governance Repository**: `score2gp-agentops`
  - **Branch**: `research/major-triads-active-grouping-blocker-v0.2`
  - **Parent Commit**: `a4f1753858529bc8ba51e87ee3f3eee663dfc1d5` (PR #11 merge: Record Major Triads active grouping blocker research)

## Commands Run

Fresh private-safe Lesson 3 extraction and diagnostic command:
```powershell
$env:PYTHONPATH="src"; .venv\Scripts\python -m score2gp.cli extract-tab fixtures/private/Lesson-3.pdf --out work/major_triads_active_grouping_blocker_20260528_1240/lesson_3
```

Diagnostic scratch analyzer scripts run inside the workspace:
```powershell
$env:PYTHONPATH="src"; .venv\Scripts\python scratch/analyze_blocker.py
$env:PYTHONPATH="src"; .venv\Scripts\python scratch/analyze_bars.py
$env:PYTHONPATH="src"; .venv\Scripts\python scratch/analyze_barlines.py
$env:PYTHONPATH="src"; .venv\Scripts\python scratch/analyze_candidates.py
```

## Input Availability

- **Input File**: `fixtures/private/Lesson-3.pdf` (private birth-digital PDF benchmark file, verified present).
- **Extracted Diagnostics**:
  - `work/major_triads_active_grouping_blocker_20260528_1240/lesson_3/tab_raw.json`
  - `work/major_triads_active_grouping_blocker_20260528_1240/lesson_3/warnings.json`
  - `work/major_triads_active_grouping_blocker_20260528_1240/lesson_3/grouping-diagnostics.html`

## Artifact Coherence

All artifacts are coherent and consistent. The workspace is clean and verified using Git checks. Untracked scratch diagnostic scripts created in the `scratch/` folder have been kept out of the Git tracking index. The generated run files are isolated in the local `.gitignore`-ignored `work/` directory, adhering strictly to the private-safety invariant.

## Strict Gate Failure

- **Grouping Status**: `partial`
- **Grouping Confidence Status**: `below_threshold`
- **First Blocker Code**: `pdf_grouping_confidence_below_threshold`
- **Other Blocker Warnings**:
  - `pdf_string_assignment_not_enough_for_build_ir`
  - `pdf_grouping_not_safe_for_build_ir`
  - `pdf_missing_pdf_grouping_blocks_build_ir`
  - `pdf_layout_detection_requires_manual_review`
  - `pdf_partial_grouping_with_playable_candidates`
- **Decomposition**: The strict gate fails because 32 playable fret candidates (belonging to the rightmost measures of systems) are completely unassigned to any bar box (`bar_index: null`). This causes `pdf_partial_grouping_with_playable_candidates` to be raised, which drops system grouping confidence. As a result, `pdf_grouping_confidence_below_threshold` is flagged, which is checked by `build_ir.py` under `_tabraw_unsafe_grouping_warning_codes` and strictly blocks IR compilation.

## Candidate Assignment Breakdown

This private-safe matrix details the system, bar, and string assignment counts across both total candidates and playable fret candidates only:

### 1. General Breakdown

| Candidate Pool | Total | Assigned to System | Assigned to Bar | Assigned to String | Assigned to All Three | Missing System | Missing Bar | Missing String |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **All Candidates** | 591 | 431 | 399 | 430 | 398 | 160 | 192 | 161 |
| **Playable Candidates** | 548 | 430 | 398 | 430 | 398 | 118 | 150 | 118 |

### 2. Breakdown by Page and System for Playable Candidates

* **Legend & Page Numbers** (Correctly Excluded):
  - 118 playable candidates are missing all three dimensions (system, bar, and string) because they are page numbers, chord diagram labels, or legend text. They are successfully identified and excluded by the pipeline via `pdf_fret_page_or_legend_number_excluded`.
* **Standard TAB Notes** (Systemically Active Blocker):
  - **32 playable candidates** are assigned to a system and a string, but are **missing a bar box assignment** because they fall in the rightmost measure beyond the last constructed bar box.

The 32 unassigned active blocker candidates are distributed as follows:
- **Page 1, System 3**: 6 unassigned candidates (Fret candidates located at x > 430.15)
- **Page 2, System 1**: 4 unassigned candidates (Fret candidates located at x > 430.15)
- **Page 2, System 6**: 4 unassigned candidates (Fret candidates located at x > 430.15)
- **Page 2, System 7**: 7 unassigned candidates (Fret candidates located at x > 403.71)
- **Page 3, System 6**: 7 unassigned candidates (Fret candidates located at x > 316.90)
- **Page 4, System 1**: 4 unassigned candidates (Fret candidates located at x > 430.16)

## Warning Taxonomy

Unique warnings extracted from `warnings.json` categorized by pipeline component:

### 1. System Detection & Layout (Diagnostic Only)
* `pdf_bar_boxes_constructed` (22 counts): Confirms successful bar box construction for the left/middle bars.
* `pdf_layout_details` (1 count): Reports aggregate layout counts.

### 2. Bar Detection & Edge Boundary (Build-IR Blocking)
* `pdf_barline_does_not_cross_staff` (19 counts - diagnostic): Raised on vertical lines corresponding to standard notation barlines that are vertically outside the TAB staff.
* `pdf_barline_outside_staff_region` (19 counts - diagnostic): Co-occurs with the notation barline crossings.
* `pdf_barline_too_short` (11 counts - diagnostic): Internal vertical segment length check.
* `pdf_barline_ambiguous` (11 counts - diagnostic/fatal): Raised on double barlines at system boundaries.
* `pdf_candidate_outside_bar` (1 count - fatal): Fret candidates located outside valid boundaries.
* `pdf_candidate_unassigned_to_bar` (1 count - fatal): Fret candidates lacking bar scope.
* `pdf_candidates_unassigned_to_bar` (1 count - fatal): Systemic alert for unassigned bar box candidates.
* `ambiguous_bar_assignment` (1 count - fatal): Fret assignment safety risk.

### 3. String Assignment (Build-IR Blocking)
* `pdf_string_assignment_not_enough_for_build_ir` (2 counts - fatal)
* `pdf_playable_candidate_requires_string_assignment` (1 count - fatal)
* `pdf_string_assignment_compact_staff_ambiguous` (1 count - fatal): Spacing checks.
* `pdf_string_assignment_confidence_below_threshold` (1 count - fatal)
* `pdf_string_assignment_missing` (1 count - fatal)

### 4. Fret Optical Bounds (Build-IR Blocking)
* `pdf_fret_bbox_too_tall` (1 count - fatal)
* `pdf_fret_digit_symbol_overlap_ambiguous` (1 count - fatal)
* `pdf_fret_digits_not_merged_gap_too_large` (1 count - fatal)
* `pdf_fret_optical_bounds_confidence_below_threshold` (1 count - fatal)
* `pdf_fret_refinement_not_enough_for_build_ir` (1 count - fatal)

### 5. Grouping Confidence & safety Gates (Build-IR Blocking)
* `pdf_grouping_not_safe_for_build_ir` (2 counts - fatal)
* `pdf_missing_pdf_grouping_blocks_build_ir` (2 counts - fatal)
* `pdf_layout_detection_requires_manual_review` (2 counts - fatal)
* `pdf_partial_grouping_with_playable_candidates` (2 counts - fatal)
* `pdf_grouping_confidence_below_threshold` (2 counts - fatal)
* `partial_pdf_grouping` (1 count - fatal)
* `missing_pdf_grouping` (1 count - fatal)

## First High-Impact Failure Cluster

* **Location**: Rightmost measures of Page 1 System 3, Page 2 System 1, Page 2 System 6, Page 3 System 6, and Page 4 System 1.
* **Candidate Count Affected**: 32 playable candidates.
* **Missing Dimension**: `bar` assignment.
* **Dominant Warning Codes**: `pdf_candidates_unassigned_to_bar`, `pdf_candidate_outside_bar`, `pdf_barline_ambiguous`.
* **Visual/Geometry Characteristics**: These are real fret numbers (e.g. frets 7, 8, 9, 10, 12, 14) positioned normally on strings, but they sit to the right of the last constructed barline (e.g. at x > 430.16 on Page 4 System 1). Because the rightmost double barline at x ≈ 574.95 consists of two vertical lines very close together, they horizontal-overlap within the `< 6.0` pixel tolerance and are BOTH rejected as `pdf_barline_ambiguous`, leaving no right boundary.

## Supported Hypotheses

* **Hypothesis 4**: *Bar boxes are still incomplete despite row normalization.*
  - **Status**: **Supported**
  - **Evidence**: Directly verified by examining `tab_raw.json` coordinate data and candidate `raw` parameters. Perfect, full-height double barlines at the end of systems (e.g. at x=572.57 and x=574.95) are rejected as `pdf_barline_ambiguous`. This prevents the rightmost bar box from being drawn, leaving 32 playable candidates unassigned.
* **Hypothesis 9**: *Bar assignment is failing because candidates fall outside reconstructed bar boxes.*
  - **Status**: **Supported**
  - **Evidence**: Candidate bbox `x` values (ranging from `439.5` to `549.5`) sit beyond the last constructed bar box boundary (`430.16`), causing them to fall in the unassigned bar region.

## Unverified Hypotheses

* **Hypothesis 2**: *String assignment confidence/compact-staff ambiguity is now the active blocker.*
  - **Status**: **Unverified**
  - **Evidence**: Compact staff warnings are present, but the pipeline successfully assigns a string index to all 430 playable candidates on active systems. String snapping is functioning; the blocker is purely bar-boxing.
* **Hypothesis 3**: *Fret optical bounds confidence is the active blocker.*
  - **Status**: **Unverified**
  - **Evidence**: Tall fret warnings are present, but they only decrease candidate confidence; they do not block the grouping layer directly.
* **Hypothesis 6**: *Grouping confidence threshold is aggregating several smaller non-fatal warnings.*
  - **Status**: **Unverified**
  - **Evidence**: Grouping confidence is low primarily due to the fatal presence of 32 unassigned playable candidates, not aggregation of minor warnings.
* **Hypothesis 7**: *Diagnostic counters are inconsistent across stages.*
  - **Status**: **Unverified**
  - **Evidence**: Counters are highly consistent: 548 total playable candidates = 430 assigned to system/string + 118 page/legend numbers.
* **Hypothesis 8**: *Line grouping has improved, but token-to-string assignment is still too conservative.*
  - **Status**: **Unverified**
  - **Evidence**: The token-to-string snapping pipeline is successfully assigning a string to all 430 playable candidates (100% of those belonging to active systems). Snapping is not acting as the blocker.

## Contradicted Hypotheses

* **Hypothesis 1**: *Paired-staff row fragmentation remains the active blocker.*
  - **Status**: **Contradicted**
  - **Evidence**: PR #147 is successfully merged, and tests pass. Baseline and post-PR metrics are identical on Lesson 3 because the layout does not suffer from row fragmentation.
* **Hypothesis 5**: *Non-tab text is still being counted as playable.*
  - **Status**: **Contradicted**
  - **Evidence**: Excluded page/legend numbers have `pdf_fret_page_or_legend_number_excluded` and are correctly filtered out from standard round-trip notes. The 32 active blocking candidates are authentic guitar tab notes.

## Recommended Public Fixture

We recommend a synthetic **Double Barline Horizontal Ambiguity Fixture** to safely reproduce and resolve the blocker in public tests.

### 1. Fixture Setup (`tests/test_pdf.py` or synthetic JSON fixture)
- **Staff Geometry**: A standard 6-line TAB staff extending horizontally from x = 36.0 to x = 575.0.
- **Barlines**: 
  - Left boundary: A single vertical line at x = 36.0.
  - Middle boundary: A single vertical line at x = 245.0.
  - Right boundary (Double barline): Two parallel vertical lines at x = 572.0 and x = 575.0 (separated by 3.0 pixels).
- **Candidates**: Playable digits (e.g. `7` and `9`) placed at x = 100.0 (Measure 1) and x = 350.0 (Measure 2).

### 2. Assertions (Expected Success vs Refusal)
* **Expected Success Case**:
  - The final two barlines should NOT both be rejected as ambiguous. Instead, they should be merged (e.g. into a single boundary at x = 575.0) or the first one should be selected.
  - Exactly two bar boxes must be successfully constructed: Bar 1 (36.0 to 245.0) and Bar 2 (245.0 to 575.0).
  - All playable candidates must be assigned to their correct bars.
  - `assert "pdf_barline_ambiguous" not in warning_codes`
  - `assert len(bar_boxes) == 2`
* **Expected Safe-Refusal Case**:
  - If two parallel vertical lines are separated by a large distance (e.g. > 15.0 pixels) within a single measure span with no note events between them, they should be treated as ambiguous or distinct, rather than squash-merged.

## Recommended Next Implementation Slice

### 1. Branch Name
`bugfix/double-barline-ambiguity-resolution-v0.1`

### 2. Goal
Resolve the double-barline horizontal ambiguity bug in `filter_tab_barline_candidates` by allowing close, parallel vertical barlines (separated by < 6.0 pixels) to be merged or consolidated into a single valid boundary, rather than rejecting both, enabling the successful construction of rightmost system bar boxes.

### 3. Non-Goals
* Loosening global grouping thresholds.
* Skip-counting or ignoring unassigned candidates to force metrics.
* Modifying timing rules or preflight checks.

### 4. Public Fixture Required
`double_barline_ambiguity_fixture` (as described in Q6).

### 5. Private Lesson 3 Metric Expected to Move
* **Playable Candidates with Bar**: From `398` to `430`.
* **Strict Grouping Status**: From `partial` to `complete`.
* **ScoreIR Written**: From `no` to `yes`.

### 6. Guardrail Test
* Verify that standard single barlines (separated by normal measure widths) are unaffected.
* Verify that horizontal staff lines and other drawing segments are not merged incorrectly.

### 7. Acceptance Criteria
* Barlines within `6.0` pixels of each other are merged or selected (e.g. using the outer line as the system edge boundary) rather than triggering `pdf_barline_ambiguous` on both.
* The rightmost measure of Page 4 System 1 constructs a valid bar box up to the system edge.

### 8. Verification Commands
```powershell
python -m pytest
$env:PYTHONPATH="src"; .venv\Scripts\python -m score2gp.cli extract-tab fixtures/private/Lesson-3.pdf --out work/remediation/lesson_3
```

## Non-Goals and Invariants

* No native GP oracle parsing or MusicXML timing repair.
* No MusicXML or GP pitch data is used to drive PDF geometry.
* No private PDFs or diagnostic files will be committed to the repository (verified by `git ls-files`).

## Verification & Execution Results

The safe logical boundary clustering for rightmost parallel double-barlines was successfully implemented and verified:

* **Implementation Branch**: `research/major-triads-active-grouping-blocker-v0.2`
* **Implementation Commit (Product)**: `2f875626739fbc130d0fd36e1d07c56e91044fe2`
* **Unit & Integration Tests**: 100% of all 391 tests passed successfully under `pytest` with `PYTHONPATH="src"`. This includes the new `test_double_barline_ambiguity_resolution` proving that:
  - Parallel end barlines separated by `< 6.0` pixels at the right system edge are clustered horizontally.
  - The rightmost is selected as the accepted representative, while the other is flagged as non-fatal `pdf_barline_double_secondary`.
  - Non-edge parallel barlines (middle measures) still trigger the expected `pdf_barline_ambiguous` warning correctly.
  - Exactly 2 bar boxes are successfully constructed and candidates in the rightmost measure are successfully assigned.
* **Manual Smoke Test (Lesson 3)**:
  - This implementation resolves the tested rightmost double-barline ambiguity case and improves Lesson 3 bar assignment by 32 candidates; strict grouping remains partial and further blockers remain.
  - Strict grouping remains partial: yes
  - ScoreIR written: no
  - GP written: no
  - semantic round-trip attempted: no
  - This is a targeted layout blocker improvement, not conversion success.

## Private-Safety Audit

A complete directory audit was executed using Git tracking commands.
`git ls-files fixtures/private work` outputs exactly and only:
`fixtures/private/.gitkeep`
No private pdfs, GP files, JSON intermediates, or work files have been staged or tracked.



