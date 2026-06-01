# Run Record: Bar Alignment Quality Gate v0.1

Durable record of the Bar Alignment Quality Gate implementation, public classification test suite, and E2E validation against the private benchmark ladder.

## Metadata
- **Run ID**: `2026-06-01-bar-alignment-quality-gate`
- **Product Repository**: `tticom/score2gp`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Branch**: `feature/bar-alignment-quality-gate-v0.1`
- **Agentops Branch**: `agent/bar-alignment-quality-gate-v0.1`

---

## 1. Architectural Strategy & Quality Gate

We resolved a key parser-level overcounting defect and established a robust, evidence-backed bar alignment quality gate in the post-serialization post-processing pipeline.

### Parser Correction in `inspect_gp`
We discovered that the +4 bar mismatch finding for Lessons 3–7 was **not** caused by the booklet compiler or cover pages. Instead, it was 100% a parsing artifact of `root.findall(".//Bar")` matching non-musical `<Bar>` tags under `<Automation>` structures in relational layouts (tempo automation, channel strip automations, etc.).

We corrected `_summarize_gpif(root)` to:
- Query true track musical bars strictly via `root.findall(".//Bars/Bar")`.
- Expose separate metrics for `raw_bar_tag_count`, `musical_track_bar_count`, `master_bar_count`, `automation_bar_tag_count`, and `template_prelude_bar_count`.
- Apply a robust fallback strategy (`track_bars` -> `master_bars` -> `raw_bars`), tracking fallback usage explicitly.

### Quality Gate & Classification
Refactored `classify_gp_quality` to compute `bar_alignment_status` and enforce strict priorities:
1. Note coverage and empty output checks take absolute priority over bar alignment.
2. If `template_prelude_bar_count > 0` and true track bars match `scoreir_bar_count`, the status is `"expected_template_bars_accounted"`.
3. If they match and `template_prelude_bar_count == 0`, status is `"aligned"`.
4. Otherwise, status is `"mismatch"`, which strictly classifies as `gp_output_bar_alignment_suspect`.

---

## 2. Private Smoke & Quality Audit Results

The quality audit was successfully executed across all private inputs under default `allow_remediation=False` path.

### Post-Serialization Quality Audit Table

| Input Label | ScoreIR Bars | Raw XML Bar Tags | True Musical Bars | Automation Bars | Template Prelude Bars | Alignment Status | Final Classification |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `private_input_custom_lesson_3` | 66 | 70 | 66 | 4 | 0 | `aligned` | `gp_output_technique_loss_expected` |
| `private_input_custom_lesson_4` | 79 | 83 | 79 | 4 | 0 | `aligned` | `gp_output_technique_loss_expected` |
| `private_input_custom_lesson_5` | 43 | 47 | 43 | 4 | 0 | `aligned` | `gp_output_technique_loss_expected` |
| `private_input_custom_lesson_6` | 72 | 76 | 72 | 4 | 0 | `aligned` | `gp_output_technique_loss_expected` |
| `private_input_custom_lesson_7` | 93 | 97 | 93 | 4 | 0 | `aligned` | `gp_output_technique_loss_expected` |
| `private_input_custom_melodic_soloing` | 18 | 22 | 18 | 4 | 0 | `aligned` | `gp_output_empty_or_near_empty` |

*Note: All Lessons 3-7 report `raw_bar_tag_count = musical_track_bar_count + automation_bar_tag_count` (`70 = 66 + 4`), `template_prelude_bar_count = 0`, and `bar_alignment_status = aligned`.*

---

## 3. Detailed Per-Score Metrics (Private-Safe)

Durable, private-safe metrics extracted for every private input file:

### `private_input_1`
- **ScoreIR Note Count**: `0`
- **GPIF Note Count**: `0`
- **Playable Fret Candidate Count**: `153`
- **Matched Fret Candidate Count**: `0`
- **Unmatched Fret Candidate Count**: `153`
- **Non-Playable Technique/Text Candidate Count**: `106`
- **Warning-code Counts**:
  - `partial_pdf_grouping`: 1
  - `pdf_bar_boxes_constructed`: 9
  - `pdf_barline_double_secondary`: 1
  - `pdf_barline_too_short`: 2
  - `pdf_fret_digit_symbol_overlap_ambiguous`: 1
  - `pdf_fret_digits_not_merged_gap_too_large`: 1
  - `pdf_fret_optical_bounds_confidence_below_threshold`: 1
  - `pdf_fret_refinement_not_enough_for_build_ir`: 1
  - `pdf_grouping_confidence_below_threshold`: 2
  - `pdf_grouping_not_safe_for_build_ir`: 2
  - `pdf_layout_details`: 1
  - `pdf_layout_detection_requires_manual_review`: 2
  - `pdf_missing_pdf_grouping_blocks_build_ir`: 2
  - `pdf_partial_grouping_with_playable_candidates`: 2
  - `tab-extraction-incomplete`: 1
- **Artifact Paths (Private-Safe)**:
  - `warnings_json`: `private_input_1/warnings.json`

### `private_input_2`
- **ScoreIR Note Count**: `0`
- **GPIF Note Count**: `0`
- **Playable Fret Candidate Count**: `54`
- **Matched Fret Candidate Count**: `0`
- **Unmatched Fret Candidate Count**: `54`
- **Non-Playable Technique/Text Candidate Count**: `25`
- **Warning-code Counts**:
  - `ascii_tab_detected`: 1
  - `ascii_tab_measure_boundary_missing`: 1
  - `ascii_tab_timing_unavailable`: 1
  - `missing_pdf_grouping`: 1
  - `partial_pdf_grouping`: 1
  - `pdf-tab-system-not-detected`: 1
  - `pdf_ascii_system_detected`: 2
  - `pdf_ascii_system_measure_boundaries_missing`: 2
  - `pdf_ascii_system_timing_unavailable`: 2
  - `pdf_drawn_geometry_present_but_staff_unresolved`: 2
  - `pdf_drawn_staff_lines_unresolved`: 2
  - `pdf_drawn_system_not_detected`: 2
  - `pdf_grouping_not_safe_for_build_ir`: 2
  - `pdf_input_class_ascii_tab_requires_alignment`: 2
  - `pdf_input_class_drawn_tab_requires_barlines`: 2
  - `pdf_layout_details`: 1
  - `pdf_layout_detection_requires_manual_review`: 2
  - `pdf_missing_pdf_grouping_blocks_build_ir`: 2
  - `pdf_no_systems_detected`: 2
  - `pdf_partial_grouping_with_playable_candidates`: 2
  - `pdf_string_lines_missing`: 2
  - `pdf_system_detected_bar_detection_missing`: 2
  - `pdf_system_detection_not_enough_for_build_ir`: 2
  - `pdf_tab_candidates_present_but_system_not_detected`: 2
  - `pdf_tab_staff_lines_fragmented`: 2
  - `pdf_tab_staff_missing`: 2
  - `pdf_text_geometry_present_but_no_safe_system`: 2
  - `tab-extraction-incomplete`: 1
  - `unsupported_ascii_tab_rhythm`: 1
- **Artifact Paths (Private-Safe)**:
  - `warnings_json`: `private_input_2/warnings.json`

### `private_input_custom`
- **ScoreIR Note Count**: `0`
- **GPIF Note Count**: `0`
- **Playable Fret Candidate Count**: `0`
- **Matched Fret Candidate Count**: `0`
- **Unmatched Fret Candidate Count**: `0`
- **Non-Playable Technique/Text Candidate Count**: `3`
- **Warning-code Counts**:
  - `partial_pdf_grouping`: 1
  - `pdf-tab-system-not-detected`: 1
  - `pdf_drawn_system_not_detected`: 2
  - `pdf_grouping_not_safe_for_build_ir`: 2
  - `pdf_layout_details`: 1
  - `pdf_layout_detection_requires_manual_review`: 2
  - `pdf_missing_pdf_grouping_blocks_build_ir`: 2
  - `pdf_no_systems_detected`: 2
  - `pdf_string_lines_missing`: 2
  - `pdf_system_detection_not_enough_for_build_ir`: 2
  - `pdf_tab_staff_missing`: 2
  - `tab-extraction-incomplete`: 1
- **Artifact Paths (Private-Safe)**:
  - `warnings_json`: `private_input_custom/warnings.json`

### `private_input_custom_lesson_3`
- **ScoreIR Note Count**: `451`
- **GPIF Note Count**: `451`
- **Playable Fret Candidate Count**: `454`
- **Matched Fret Candidate Count**: `451`
- **Unmatched Fret Candidate Count**: `3`
- **Non-Playable Technique/Text Candidate Count**: `4`
- **Warning-code Counts**:
  - `partial_pdf_grouping`: 1
  - `pdf_bar_boxes_constructed`: 23
  - `pdf_barline_does_not_cross_staff`: 20
  - `pdf_barline_double_secondary`: 10
  - `pdf_barline_outside_staff_region`: 20
  - `pdf_barline_too_short`: 21
  - `pdf_candidate_outside_bar`: 1
  - `pdf_candidate_outside_system`: 1
  - `pdf_fret_digits_not_merged_gap_too_large`: 1
  - `pdf_fret_optical_bounds_confidence_below_threshold`: 1
  - `pdf_fret_refinement_not_enough_for_build_ir`: 1
  - `pdf_grouping_confidence_below_threshold`: 2
  - `pdf_grouping_not_safe_for_build_ir`: 2
  - `pdf_layout_details`: 1
  - `pdf_layout_detection_requires_manual_review`: 2
  - `pdf_missing_pdf_grouping_blocks_build_ir`: 2
  - `pdf_partial_grouping_with_playable_candidates`: 2
  - `pdf_timing_mapping_not_implemented`: 1
  - `pdf_tuning_standard_detected`: 1
  - `tab-extraction-incomplete`: 1
- **Artifact Paths (Private-Safe)**:
  - `gp_package`: `private_input_custom_lesson_3/smoke.gp`
  - `score_ir_json`: `private_input_custom_lesson_3/score.ir.json`
  - `warnings_json`: `private_input_custom_lesson_3/warnings.json`

### `private_input_custom_lesson_4`
- **ScoreIR Note Count**: `546`
- **GPIF Note Count**: `546`
- **Playable Fret Candidate Count**: `549`
- **Matched Fret Candidate Count**: `546`
- **Unmatched Fret Candidate Count**: `3`
- **Non-Playable Technique/Text Candidate Count**: `31`
- **Warning-code Counts**:
  - `partial_pdf_grouping`: 1
  - `pdf_bar_boxes_constructed`: 29
  - `pdf_barline_does_not_cross_staff`: 24
  - `pdf_barline_double_secondary`: 15
  - `pdf_barline_outside_staff_region`: 24
  - `pdf_barline_too_short`: 28
  - `pdf_candidate_outside_bar`: 1
  - `pdf_candidate_outside_system`: 1
  - `pdf_fret_digits_not_merged_gap_too_large`: 1
  - `pdf_fret_optical_bounds_confidence_below_threshold`: 1
  - `pdf_fret_refinement_not_enough_for_build_ir`: 1
  - `pdf_grouping_confidence_below_threshold`: 2
  - `pdf_grouping_not_safe_for_build_ir`: 2
  - `pdf_layout_details`: 1
  - `pdf_layout_detection_requires_manual_review`: 2
  - `pdf_missing_pdf_grouping_blocks_build_ir`: 2
  - `pdf_partial_grouping_with_playable_candidates`: 2
  - `pdf_timing_mapping_not_implemented`: 1
  - `pdf_tuning_standard_detected`: 1
  - `tab-extraction-incomplete`: 1
- **Artifact Paths (Private-Safe)**:
  - `gp_package`: `private_input_custom_lesson_4/smoke.gp`
  - `score_ir_json`: `private_input_custom_lesson_4/score.ir.json`
  - `warnings_json`: `private_input_custom_lesson_4/warnings.json`

### `private_input_custom_lesson_5`
- **ScoreIR Note Count**: `295`
- **GPIF Note Count**: `295`
- **Playable Fret Candidate Count**: `297`
- **Matched Fret Candidate Count**: `295`
- **Unmatched Fret Candidate Count**: `2`
- **Non-Playable Technique/Text Candidate Count**: `21`
- **Warning-code Counts**:
  - `partial_pdf_grouping`: 1
  - `pdf_bar_boxes_constructed`: 11
  - `pdf_barline_does_not_cross_staff`: 5
  - `pdf_barline_double_secondary`: 3
  - `pdf_barline_outside_staff_region`: 5
  - `pdf_barline_too_short`: 6
  - `pdf_candidate_outside_bar`: 1
  - `pdf_candidate_outside_system`: 1
  - `pdf_fret_digits_not_merged_gap_too_large`: 1
  - `pdf_fret_optical_bounds_confidence_below_threshold`: 1
  - `pdf_fret_refinement_not_enough_for_build_ir`: 1
  - `pdf_grouping_confidence_below_threshold`: 2
  - `pdf_grouping_not_safe_for_build_ir`: 2
  - `pdf_layout_details`: 1
  - `pdf_layout_detection_requires_manual_review`: 2
  - `pdf_missing_pdf_grouping_blocks_build_ir`: 2
  - `pdf_partial_grouping_with_playable_candidates`: 2
  - `pdf_timing_mapping_not_implemented`: 1
  - `pdf_tuning_standard_detected`: 1
  - `tab-extraction-incomplete`: 1
- **Artifact Paths (Private-Safe)**:
  - `gp_package`: `private_input_custom_lesson_5/smoke.gp`
  - `score_ir_json`: `private_input_custom_lesson_5/score.ir.json`
  - `warnings_json`: `private_input_custom_lesson_5/warnings.json`

### `private_input_custom_lesson_6`
- **ScoreIR Note Count**: `115`
- **GPIF Note Count**: `115`
- **Playable Fret Candidate Count**: `115`
- **Matched Fret Candidate Count**: `115`
- **Unmatched Fret Candidate Count**: `0`
- **Non-Playable Technique/Text Candidate Count**: `13`
- **Warning-code Counts**:
  - `partial_pdf_grouping`: 1
  - `pdf-tab-system-not-detected`: 3
  - `pdf_bar_boxes_constructed`: 5
  - `pdf_barline_does_not_cross_staff`: 3
  - `pdf_barline_double_secondary`: 4
  - `pdf_barline_outside_staff_region`: 3
  - `pdf_barline_too_short`: 5
  - `pdf_drawn_geometry_present_but_staff_unresolved`: 4
  - `pdf_drawn_staff_lines_unresolved`: 2
  - `pdf_fret_digits_not_merged_gap_too_large`: 1
  - `pdf_fret_optical_bounds_confidence_below_threshold`: 1
  - `pdf_fret_refinement_not_enough_for_build_ir`: 1
  - `pdf_grouping_confidence_below_threshold`: 2
  - `pdf_grouping_not_safe_for_build_ir`: 2
  - `pdf_layout_details`: 1
  - `pdf_layout_detection_requires_manual_review`: 2
  - `pdf_missing_pdf_grouping_blocks_build_ir`: 2
  - `pdf_partial_grouping_with_playable_candidates`: 2
  - `pdf_tab_staff_lines_fragmented`: 4
  - `pdf_text_geometry_present_but_no_safe_system`: 4
  - `pdf_timing_mapping_not_implemented`: 1
  - `pdf_tuning_standard_detected`: 1
  - `tab-extraction-incomplete`: 1
- **Artifact Paths (Private-Safe)**:
  - `gp_package`: `private_input_custom_lesson_6/smoke.gp`
  - `score_ir_json`: `private_input_custom_lesson_6/score.ir.json`
  - `warnings_json`: `private_input_custom_lesson_6/warnings.json`

### `private_input_custom_lesson_7`
- **ScoreIR Note Count**: `624`
- **GPIF Note Count**: `624`
- **Playable Fret Candidate Count**: `624`
- **Matched Fret Candidate Count**: `624`
- **Unmatched Fret Candidate Count**: `0`
- **Non-Playable Technique/Text Candidate Count**: `13`
- **Warning-code Counts**:
  - `partial_pdf_grouping`: 1
  - `pdf_bar_boxes_constructed`: 25
  - `pdf_barline_does_not_cross_staff`: 26
  - `pdf_barline_double_secondary`: 22
  - `pdf_barline_outside_staff_region`: 26
  - `pdf_barline_too_short`: 26
  - `pdf_fret_digits_not_merged_gap_too_large`: 1
  - `pdf_fret_optical_bounds_confidence_below_threshold`: 1
  - `pdf_fret_refinement_not_enough_for_build_ir`: 1
  - `pdf_grouping_confidence_below_threshold`: 2
  - `pdf_grouping_not_safe_for_build_ir`: 2
  - `pdf_layout_details`: 1
  - `pdf_layout_detection_requires_manual_review`: 2
  - `pdf_missing_pdf_grouping_blocks_build_ir`: 2
  - `pdf_partial_grouping_with_playable_candidates`: 2
  - `pdf_timing_mapping_not_implemented`: 1
  - `pdf_tuning_standard_detected`: 1
  - `tab-extraction-incomplete`: 1
- **Artifact Paths (Private-Safe)**:
  - `gp_package`: `private_input_custom_lesson_7/smoke.gp`
  - `score_ir_json`: `private_input_custom_lesson_7/score.ir.json`
  - `warnings_json`: `private_input_custom_lesson_7/warnings.json`

### `private_input_custom_melodic_soloing`
- **ScoreIR Note Count**: `0`
- **GPIF Note Count**: `0`
- **Playable Fret Candidate Count**: `59`
- **Matched Fret Candidate Count**: `0`
- **Unmatched Fret Candidate Count**: `59`
- **Non-Playable Technique/Text Candidate Count**: `51`
- **Warning-code Counts**:
  - `partial_pdf_grouping`: 1
  - `pdf_bar_box_construction_not_enough_for_build_ir`: 3
  - `pdf_bar_box_too_narrow`: 3
  - `pdf_barline_ambiguous`: 3
  - `pdf_barline_crosses_insufficient_string_gaps`: 3
  - `pdf_barline_does_not_cross_staff`: 3
  - `pdf_barline_double_secondary`: 1
  - `pdf_barline_too_short`: 3
  - `pdf_fret_bbox_too_tall`: 1
  - `pdf_fret_digits_not_merged_gap_too_large`: 1
  - `pdf_fret_optical_bounds_confidence_below_threshold`: 1
  - `pdf_fret_refinement_not_enough_for_build_ir`: 1
  - `pdf_grouping_confidence_below_threshold`: 2
  - `pdf_grouping_not_safe_for_build_ir`: 2
  - `pdf_large_tab_staff_spacing_detected`: 1
  - `pdf_layout_details`: 1
  - `pdf_layout_detection_requires_manual_review`: 2
  - `pdf_missing_pdf_grouping_blocks_build_ir`: 2
  - `pdf_partial_grouping_with_playable_candidates`: 2
  - `pdf_tab_staff_spacing_supported_dynamic`: 1
  - `pdf_timing_mapping_not_implemented`: 1
  - `pdf_tuning_standard_detected`: 1
  - `tab-extraction-incomplete`: 1
- **Artifact Paths (Private-Safe)**:
  - `gp_package`: `private_input_custom_melodic_soloing/smoke.gp`
  - `score_ir_json`: `private_input_custom_melodic_soloing/score.ir.json`
  - `warnings_json`: `private_input_custom_melodic_soloing/warnings.json`

---

## 4. Public Test Verification

We added 8 comprehensive unit tests under `tests/test_bar_alignment_quality_gate.py` verifying all parser-level and quality-level positive/negative cases:
1. `test_parser_ignores_automation_bar_tags`: Asserts that automation Bar tags do not inflate musical track bar count.
2. `test_raw_plus_4_automation_overcount_no_suspect`: Asserts that +4 automation overcounts do not trigger `gp_output_bar_alignment_suspect`.
3. `test_raw_plus_4_mismatch_without_automation_is_suspect`: Asserts raw track bar mismatches are strictly flagged as suspect.
4. `test_explicit_template_prelude_track_bars_accounted`: Verifies expected template bars are correctly subtracted and accounted for.
5. `test_claimed_template_bars_with_notes_remain_suspect`: Asserts template prelude bars with notes trigger suspect status.
6. `test_fewer_musical_gpif_bars_than_scoreir_remains_suspect`: Asserts fewer musical bars than ScoreIR are flagged as suspect.
7. `test_technique_loss_reached_only_after_alignment_passes`: Confirms un-serialized technique markers classify as technique loss expected once alignment passes.
8. `test_low_serialized_note_coverage_beats_bar_success`: Enforces note coverage priority over bar success.

**All 438 public unit and integration tests passed perfectly.**

---

## 5. Private-Safety Audit

- **Verification Command:** `git ls-files fixtures/private work`
- **Output:** `fixtures/private/.gitkeep`
- **Result:** **No private files or OMR assets were committed.** The private-safety invariant is strictly maintained.

---

## 6. Recommended Next Branch

`feature/melodic-soloing-barline-refinement-v0.1`
To resolve OMR barline drift and layout alignment mapping, which is the current blocker for the melodic soloing score's empty GP packages.
