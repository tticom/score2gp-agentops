# Major Triads Lesson 3 Benchmark Results

## 1. Extraction & Layout Geometry Metrics
- **Page Count**: 4
- **Detected Systems**: 23
- **Detected Bar Boxes**: 115
- **Detected String Lines**: 137
- **Playable Candidates**: 473
- **Playable Candidates with System**: 473
- **Playable Candidates with Bar**: 374
- **Playable Candidates with String**: 473

## 2. Strict Build-IR Status
- **Strict Grouping Status**: refused
- **ScoreIR Written**: no
- **GP Written**: no
- **Primary Blocker Category**: `pdf_only_tab_grouping_unsafe`
- **Grouping Warning Codes**: 
  - `missing_pdf_grouping`
  - `pdf_candidate_on_bar_boundary`
  - `pdf_candidate_outside_bar`
  - `pdf_candidate_unassigned_to_bar`
  - `pdf_candidates_unassigned_to_bar`
  - `pdf_fret_optical_bounds_confidence_below_threshold`
  - `pdf_fret_refinement_not_enough_for_build_ir`
  - `pdf_grouping_confidence_below_threshold`
  - `pdf_grouping_not_safe_for_build_ir`
  - `pdf_layout_detection_requires_manual_review`
  - `pdf_missing_pdf_grouping_blocks_build_ir`
  - `pdf_partial_grouping_one_system_unboxed`
  - `pdf_partial_grouping_with_playable_candidates`

## 3. Semantic Round-Trip Metrics
*(Metrics are N/A because Strict Build-IR failed entirely and blocked execution.)*
- **Oracle Note Count**: 30
- **Recovered Note Count**: 0 (N/A)
- **String Match Rate**: N/A
- **Fret Match Rate**: N/A
- **Full Match Rate**: N/A
- **Poor Bars**: N/A
- **Unknown Bars**: N/A
