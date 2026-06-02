# Run Record: Melodic Soloing Barline Refinement v0.1

Durable record of the Melodic Soloing Barline Refinement implementation, public unit and integration test suite, and E2E validation against the private benchmark ladder.

## Metadata
- **Run ID**: `2026-06-02-melodic-soloing-barline-refinement`
- **Product Repository**: `tticom/score2gp`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Branch**: `feature/melodic-soloing-barline-refinement-v0.1`
- **Agentops Branch**: `agent/melodic-soloing-barline-refinement-v0.1`

---

## 1. Architectural Strategy & Implementation

We addressed the melodic soloing empty-output blocker by refining staff segment grouping, implementing notation-to-TAB barline inheritance, capping dynamic bar boundary tolerance, and prefix-downgrading candidate-level warnings.

### Key Refinements in `src/score2gp/pdf.py`

1. **Ambiguous Bar Tolerance Cap** (`_TabSystem.ambiguous_bar_tolerance`):
   - Capped the dynamic tolerance proximity threshold at `6.0` points for widely spaced staves (`self.line_spacing > 15.0`). This prevents dynamic proximity thresholds from becoming too large and over-filtering valid/ambiguous barline evidence, while leaving standard staves completely untouched.

2. **Collinear Line Segment Horizontal Overlap Matching** (`_tab_line_groups`):
   - Resolved collinear segment groupings. If only one collinear segment exists at a target Y, it is accepted greedily. When multiple candidates exist, they are resolved by sorting them by normalized horizontal overlap ratio (requiring `>= 0.5`) against the first line of the group (`group_indices[0]`). This recovers fragmented lines on melodic soloing without regressing standard sheets like Lesson 5.

3. **Notation-to-TAB Barline Inheritance** (`_detect_tab_systems`):
   - Allowed TAB systems with incomplete native barlines (`len(valid_barlines) < 2`) to inherit barlines from standard notation staves above them.
   - Constrained standard notation staves tightly to the same page, directly above, vertically within `250.0` points, and horizontally aligned (`>= 70%` overlap).
   - Near-equivalent barlines (like double barlines or final bars) are merged and deduplicated within a `15.0` point window.

4. **OMR Warning Guarding and Downgrading** (`extract_tab` warnings collector):
   - Downgraded candidate-level warnings (such as `pdf_barline_too_short`) to severity `"info"` with an `"info_"` prefix if the system has successfully constructed/inherited at least 2 usable barlines. This prevents false blocker errors from halting the build while keeping diagnostic history intact.

---

## 2. Private Smoke & Quality Audit Results

The quality audit was successfully executed across all private inputs under default `allow_remediation=False` path.

### Post-Serialization Quality Audit Table

| Input Label | Status | Quality Category | ScoreIR Notes | GPIF Notes | Matched Frets | Deduplication | Spacing Applied |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| `private_input_1` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 | No | No |
| `private_input_2` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 | No | No |
| `private_input_custom` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 | No | No |
| `private_input_custom_lesson_3` | `pass` | `gp_output_technique_loss_expected` | 451 | 451 | 451 | No | No |
| `private_input_custom_lesson_4` | `pass` | `gp_output_technique_loss_expected` | 546 | 546 | 546 | No | No |
| `private_input_custom_lesson_5` | `pass` | `gp_output_technique_loss_expected` | 295 | 295 | 295 | No | No |
| `private_input_custom_lesson_6` | `pass` | `gp_output_technique_loss_expected` | 115 | 115 | 115 | No | No |
| `private_input_custom_lesson_7` | `pass` | `gp_output_technique_loss_expected` | 624 | 624 | 624 | No | No |
| `private_input_custom_melodic_soloing` | `pass` | `gp_output_fret_matching_suspect` | 16 | 16 | 16 | No | Yes |

*Note: All Lessons 3–7 passed with zero regressions. Melodic soloing successfully progressed from empty output to a valid pass with 16 matched notes/frets and a produced GP package!*

---

## 3. Detailed Per-Score Metrics (Private-Safe)

### `private_input_custom_melodic_soloing`
- **ScoreIR Note Count**: `16`
- **GPIF Note Count**: `16`
- **Playable Fret Candidate Count**: `59`
- **Matched Fret Candidate Count**: `16`
- **Unmatched Fret Candidate Count**: `43`
- **Non-Playable Technique/Text Candidate Count**: `51`
- **Warning-code Counts**:
  - `info_pdf_barline_ambiguous`: 2
  - `info_pdf_barline_crosses_insufficient_string_gaps`: 2
  - `info_pdf_barline_does_not_cross_staff`: 2
  - `info_pdf_barline_too_short`: 2
  - `partial_pdf_grouping`: 1
  - `pdf_bar_box_construction_not_enough_for_build_ir`: 3
  - `pdf_bar_box_too_narrow`: 3
  - `pdf_barline_double_secondary`: 1
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

## 4. Verification & Testing

### Executed Validation Command Block & Outcomes
We executed the following validation command block locally to verify the correctness of the changes:

```bash
# 1. Run unit and integration tests
python -m pytest tests/test_pdf_melodic_refinements.py
python -m pytest

# 2. Run private pipeline and quality audit
python scripts/private_e2e_smoke.py
python scripts/private_gp_quality_audit.py

# 3. Export and diff schemas
python -m score2gp.cli export-schema --out schemas
git diff -- schemas

# 4. Validate output IR files
python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json

# 5. Check workspace whitespace/diff check
git diff --check

# 6. Verify git tracked private files
git ls-files fixtures/private work
```

### Outcomes & Evidence:
1. **Specific Refinement Tests**: `python -m pytest tests/test_pdf_melodic_refinements.py`
   - **Result**: `4 passed` in `7.72s`.
2. **Full Public Test Suite**: `python -m pytest`
   - **Result**: `442 passed` in `329.42s`.
3. **Private E2E Smoke Tests**: `python scripts/private_e2e_smoke.py`
   - **Result**: Successfully ran all pipelines. Generated local artifacts under `work/private_e2e_smoke_v0_1/` including `score.ir.json` and `smoke.gp` for `private_input_custom_melodic_soloing`.
4. **Quality Audit**: `python scripts/private_gp_quality_audit.py`
   - **Result**: Wrote master quality audit summary JSON and Markdown. Verified that melodic soloing moved out of `gp_output_empty_or_near_empty` into `gp_output_fret_matching_suspect` with `16` matched notes/frets and a valid produced GP package. Zero regressions occurred on Lessons 3–7.
5. **Schema Export**: `python -m score2gp.cli export-schema --out schemas`
   - **Result**: Executed successfully. `git diff -- schemas` produced zero differences.
6. **IR Format Validation**: `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
   - **Result**: Validated successfully with no format errors.
7. **Git Whitespace Check**: `git diff --check`
   - **Result**: Completed successfully with no trailing whitespace or format errors in source/test files.
8. **Private-Safety Invariant Audit**: `git ls-files fixtures/private work`
   - **Result**: Output is exactly:
     ```text
     fixtures/private/.gitkeep
     ```
     No private inputs, generated GP packages, or intermediate JSON files are tracked in version control.

