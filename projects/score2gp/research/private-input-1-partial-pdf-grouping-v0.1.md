# ScoreToGP Research Report: Investigate private_input_1 Partial PDF Grouping Blocker (v0.1)

- **Repository**: `score2gp-agentops` and `score2gp`
- **Product Branch**: `main` (Commit: `7fb22eadcaf73d12928abfc7e2921da1348e5b9e`)
- **Agentops Branch**: `research/private-input-1-partial-pdf-grouping-v0.1` (Commit: `1cb2b226d2a6d000fdd7f0ed02e999a0712d1474`)

---

## Verdict

**First PDF grouping loss stage identified.**

The blocker is caused by overly strict candidate refinement checks on valid fret numbers. Specifically, narrow digit bounding boxes (width < 4.0pt) trigger a confidence deduction that falls below the 0.70 threshold (yielding `pdf_fret_optical_bounds_confidence_below_threshold`), and sequential distinct notes on the same string trigger digit-merging alerts (`pdf_fret_digits_not_merged_gap_too_large`). These warnings are treated as unsafe, blocking full PDF grouping and preventing `build_ir` from completing unless `allow_skip_unboxed` is enabled.

---

## Evidence

- **Product Branch**: `main`
- **Product Head SHA**: `7fb22eadcaf73d12928abfc7e2921da1348e5b9e`
- **Agentops Branch**: `research/private-input-1-partial-pdf-grouping-v0.1`
- **Agentops Head SHA**: `1cb2b226d2a6d000fdd7f0ed02e999a0712d1474`
- **Commands Run**:
  ```bash
  # WSL commands in product repo:
  PYTHONPATH=. .venv/bin/python3 -m pytest
  PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py
  PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
  git status --short
  git ls-files fixtures/private work
  ```
- **Public Test Result**: `459 passed` in 9.06s.
- **Private Safety Invariant**: `git ls-files fixtures/private work` outputs exactly `fixtures/private/.gitkeep`.
- **Private Audit Result**: `private_input_1` fails in default mode with status `fail` and quality category `gp_output_empty_or_near_empty` due to `partial_pdf_grouping`. When run via `private_e2e_smoke.py` (which passes `allow_skip_unboxed=True`), it completes successfully, producing `smoke.gp` with 160 events (137 matched candidates, 16 unmatched candidates).
- **Working Tree Status**: Clean.

---

## Stage-Loss Table

| Stage | Observed Count/Status | Expected Relationship | Warning/Category Signal | Evidence Path under `work/` | Interpretation | Recommended Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PDF page extraction** | 2 pages | 2 pages | none | `private_input_1/extracted.tabraw.json` | Text extraction succeeded completely. | None |
| **text/fret candidate extraction** | 398 candidates | 398 candidates | `tab-extraction-incomplete` | `private_input_1/extracted.tabraw.json` | Candidates extracted successfully. | None |
| **horizontal staff-line detection** | 53 lines (5 TAB staves on Page 1, 3 TAB + 1 incomplete staff on Page 2) | 54 lines (9 systems * 6 strings) | `pdf_layout_details` | `private_input_1/extracted.tabraw.json` | 8 complete 6-line staves and 1 incomplete 5-line staff detected. Notation staves missed (4.25pt < 6.0pt threshold). | None |
| **TAB system grouping** | 9 systems | 9 systems | `pdf_layout_details` | `private_input_1/extracted.tabraw.json` | Grouping succeeded. | None |
| **notation/TAB pairing** | 0 pairs | 0 pairs | none | `private_input_1/extracted.tabraw.json` | Notation staves not detected due to compact spacing (`4.25pt` vs `6.0pt` limit). | Lower notation staff spacing detection threshold to `4.0pt`. |
| **barline detection** | 28 barlines | 28 barlines | `info_pdf_barline_too_short`, `pdf_barline_double_secondary` | `private_input_1/extracted.tabraw.json` | Barlines successfully resolved. | None |
| **bar-box construction** | 16 bar boxes constructed | 16 bar boxes | `pdf_bar_boxes_constructed` | `private_input_1/extracted.tabraw.json` | Successfully matches the 16 MusicXML measures. | None |
| **candidate-to-system assignment** | 337 assigned, 61 unassigned | 398 assigned | `pdf_candidates_unassigned_to_system` | `private_input_1/extracted.tabraw.json` | Non-playable text and demoted noise digits are unassigned. 153/153 valid frets are assigned. | None (noise digits are safely demoted). |
| **candidate-to-bar assignment** | 337 assigned, 61 unassigned | 398 assigned | `pdf_candidates_unassigned_to_bar` | `private_input_1/extracted.tabraw.json` | All valid 153 fret candidates are assigned to bars. | None |
| **candidate-to-string/fret assignment** | 177 assigned, 221 unassigned | 398 assigned | `pdf_candidates_unassigned_to_string` | `private_input_1/extracted.tabraw.json` | All valid 153 fret candidates successfully assigned to strings. | None |
| **MusicXML/PDF alignment handoff** | Blocked under default run | Monotonic mapping | `pdf_fret_refinement_not_enough_for_build_ir` | `private_input_1/extracted.tabraw.json` | Refinement warnings on valid frets block build_ir. | Refine character width and digit merging tolerances. |
| **ScoreIR construction gate** | Blocked under default run | Valid IR | `pdf_grouping_not_safe_for_build_ir` | `private_input_1/build_error.json` | Safety gate triggers and prevents building IR. | Refine safety gate codes list to tolerate font width warnings. |

---

## Warning Summary

The warning counts at candidate and page levels (anonymized and grouped by category, counts only):

### Page-level warnings (from `warnings.json`)
- `pdf_grouping_not_safe_for_build_ir`: 2
- `pdf_missing_pdf_grouping_blocks_build_ir`: 2
- `pdf_layout_detection_requires_manual_review`: 2
- `pdf_partial_grouping_with_playable_candidates`: 2
- `pdf_grouping_confidence_below_threshold`: 2
- `partial_pdf_grouping`: 1
- `pdf_fret_digit_symbol_overlap_ambiguous`: 1
- `pdf_fret_digits_not_merged_gap_too_large`: 1
- `pdf_fret_optical_bounds_confidence_below_threshold`: 1
- `pdf_fret_refinement_not_enough_for_build_ir`: 1
- `pdf_bar_boxes_constructed`: 9
- `info_pdf_barline_too_short`: 1
- `pdf_barline_double_secondary`: 1
- `pdf_layout_details`: 1
- `tab-extraction-incomplete`: 1

### Candidate-level warnings (from `extracted.tabraw.json`)
- `pdf_non_playable_text_not_string_assigned`: 236
- `pdf_string_assignment_nearest_line`: 177
- `pdf_fret_refinement_not_enough_for_build_ir`: 161
- `pdf_fret_optical_bounds_confidence_below_threshold`: 87
- `pdf_fret_single_digit_extracted`: 82
- `pdf_fret_multidigit_extracted`: 73
- `pdf_multidigit_fret_string_assigned`: 73
- `pdf_fret_digits_not_merged_gap_too_large`: 61
- `pdf_fret_chord_text_digit_excluded`: 40
- `pdf_fret_technique_marker_excluded`: 38
- `pdf_fret_digits_merged`: 24
- `pdf_fret_split_text_span_merged`: 24
- `pdf_fret_digit_symbol_overlap_ambiguous`: 13
- `pdf_fret_page_or_legend_number_excluded`: 9
- `pdf_playable_candidate_requires_string_assignment`: 9
- `pdf_string_assignment_missing`: 9
- `pdf_candidates_unassigned_to_string`: 9
- `pdf_candidates_unassigned_to_system`: 6
- `pdf_tuning_label_outside_system`: 2
- `pdf_tuning_label_unassociated`: 2
- `pdf_tuning_text_preserved_non_playable`: 2
- `pdf_tuning_not_used_for_string_assignment`: 2
- `pdf_tuning_not_used_for_fret_inference`: 2
- `pdf_pitch_layout_evidence_detected`: 2
- `pdf_string_assignment_outside_staff`: 2
- `pdf_candidate_outside_system`: 1
- `pdf_candidate_outside_bar`: 1

---

## Comparison Table

Compare `private_input_1` against known passing custom fixtures (counts only):

| Fixture Label | Systems | Bar Boxes | Playable Candidates | Assigned Candidates | Matched Notes | Quality Category | Dominant Warnings |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `private_input_1` | 9 | 16 | 153 | 153 | 137 | `gp_output_empty_or_near_empty` (fails gate) | `pdf_fret_refinement_not_enough_for_build_ir`, `pdf_fret_digits_not_merged_gap_too_large` |
| `Lesson 3` | 7 | 23 | 461 | 459 | 459 | `gp_output_technique_loss_expected` | `info_pdf_barline_too_short`, `pdf_bar_boxes_constructed` |
| `Lesson 4` | 7 | 29 | 549 | 546 | 546 | `gp_output_technique_loss_expected` | `info_pdf_barline_too_short`, `pdf_bar_boxes_constructed` |
| `Lesson 5` | 5 | 11 | 297 | 295 | 295 | `gp_output_technique_loss_expected` | `info_pdf_barline_too_short`, `pdf_bar_boxes_constructed` |
| `Lesson 6` | 3 | 10 | 238 | 235 | 235 | `gp_output_technique_loss_expected` | `pdf_barline_double_secondary`, `info_pdf_barline_too_short` |
| `Lesson 7` | 6 | 25 | 624 | 624 | 624 | `gp_output_technique_loss_expected` | `pdf_barline_double_secondary`, `info_pdf_barline_too_short` |
| `Melodic Soloing` | 3 | 3 | 82 | 82 | 82 | `gp_output_technique_loss_expected` | `info_pdf_barline_does_not_cross_staff`, `pdf_barline_double_secondary` |

---

## Architecture Recommendation

### Recommended Smallest Developer Task

We recommend a narrow tolerance refinement task in the PDF extraction engine to prevent character width and digit merging heuristics from triggering blocking grouping failures on valid, narrow fret characters.

- **Branch Name**: `feature/private-input-1-fret-refinement-tolerances-v0.1`
- **Likely Affected Files/Modules**:
  - [src/score2gp/pdf.py](file:///\\wsl.localhost\Ubuntu-24.04\home\tticom\work\score2gp-workspace\score2gp\src\score2gp\pdf.py) (specifically `_candidate_confidence` and digits-merging logic in `_extract_pdf_text_candidates`).
- **Goal**:
  - Prevent fret candidates from dropping below 0.70 confidence (which triggers `pdf_fret_optical_bounds_confidence_below_threshold`) solely due to digit characters being narrow.
  - Avoid generating blocking warnings (`pdf_fret_digits_not_merged_gap_too_large`) for sequential distinct notes on the same string that are separated by more than a multi-digit number gap.
- **Non-goals**:
  - Do not disable safety warnings entirely.
  - Do not modify system-level layout classification or barlines.
- **Implementation Approach**:
  - In `_candidate_confidence` (line 4303), lower the width threshold from `4.0` points to `2.8` points to accommodate narrow fonts.
  - In the digits-merging loop (line 1676), restrict the `pdf_fret_digits_not_merged_gap_too_large` warning so it is only appended if there is true digit overlap or if the gap is highly ambiguous, or allow separate sequential notes to exist without triggering blocking refinement warnings.
- **Tests Required**:
  - Add a synthetic public unit test in `tests/test_pdf.py` mimicking a narrow fret digit candidate (e.g. width=3.5pt) and asserting that its confidence remains above 0.70 and that no blocking warnings are appended.
- **Validation Commands**:
  ```bash
  PYTHONPATH=. .venv/bin/python3 -m pytest
  PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
  ```
- **Acceptance Criteria**:
  - Public tests continue to pass (459 items).
  - `private_input_1` passes the post-serialization GP quality audit under default parameters without requiring `allow_skip_unboxed=True`.
- **Stop Conditions**:
  - Stop if any public unit test fails or if a change reduces notes matched in Lessons 3-7 or Melodic Soloing.
- **Reporting Format**:
  - Same as final report.
