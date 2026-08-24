# Run Record: Post-Serialization GP Output Quality Audit

Durable record of the post-serialization quality audit, public classification test suite, and E2E validation against the private benchmark ladder.

## Metadata
- **Run ID**: `2026-06-01-post-serialization-gp-output-quality-audit`
- **Product Repository**: `tticom/score2gp`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Branch**: `research/post-serialization-gp-output-quality-audit-v0.1`
- **Agentops Branch**: `agent/post-serialization-gp-output-quality-audit-v0.1`

---

## 1. Architectural Strategy & Quality Audit

We implemented a new post-serialization quality audit engine to systematically verify generated Guitar Pro packages and ScoreIR outputs. This ensures that we do not claim success purely based on "file existence" and instead rigorously evaluate musical notes coverage and alignment.

### Quality Audit Script (`private_gp_quality_audit.py`)
1. **Pipeline Metrics Aggregator**:
   - Parses generated `score.ir.json` to extract structural bar, event, and note counts.
   - Extracts anonymized warning code counts from `warnings.json`.
   - Parses OMR candidate count data from `summary.json`.
   - Directly loads the generated `.gp` zip package using `inspect_gp` to read the compiled relational GPIF measures and notes counts, and parses `<Beat>` elements to count beats.
2. **Quality Classifications**:
   - `gp_output_empty_or_near_empty`: Generated GP packages with zero notes or missing structural notes.
   - `gp_output_bar_alignment_suspect`: Shifts, skipped bars, or mismatches flagged by OMR alignment warnings or a strict bar-count mismatch between GPIF and ScoreIR (`gpif_measure_count != scoreir_bar_count`).
   - `gp_output_fret_matching_suspect`: Low fret match rates (< 40%) against playable candidates.
   - `gp_output_note_coverage_low`: Note match rates between 40% and 70%, or low serialized GP notes vs ScoreIR notes / candidates (< 70%).
   - `gp_output_technique_loss_expected`: High note coverage (70%+) and plausible bar alignment, but containing un-serialized technique text candidates.
   - `gp_output_quality_pass_basic`: Non-empty, highly matching, and fully aligned without outstanding limitations.

---

## 2. Quality Audit Summary

The quality audit was executed successfully across all private scores under default `allow_remediation=False` path. 

### Post-Serialization Quality Audit Table

| Input Label | Status | Quality Category | ScoreIR Notes | GPIF Notes | Matched Frets | Deduplication Applied | Spacing Applied |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| `private_input_1` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 | No | No |
| `private_input_2` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 | No | No |
| `private_input_custom` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 | No | No |
| `private_input_custom_lesson_3` | `pass` | `gp_output_bar_alignment_suspect` | 451 | 451 | 451 | No | No |
| `private_input_custom_lesson_4` | `pass` | `gp_output_bar_alignment_suspect` | 546 | 546 | 546 | No | No |
| `private_input_custom_lesson_5` | `pass` | `gp_output_bar_alignment_suspect` | 295 | 295 | 295 | No | No |
| `private_input_custom_lesson_6` | `pass` | `gp_output_bar_alignment_suspect` | 115 | 115 | 115 | No | No |
| `private_input_custom_lesson_7` | `pass` | `gp_output_bar_alignment_suspect` | 624 | 624 | 624 | No | No |
| `private_input_custom_melodic_soloing` | `pass` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 | No | Yes |

*Output Directory Summary Path:* `work/private_gp_quality_audit_v0_1/summary.json`

### Crucial Findings
1. **Custom Lessons (Lessons 3 to 7)**:
   - **Classification:** `gp_output_bar_alignment_suspect`
   - **Diagnosis:** The strict bar-count check successfully flags the custom lesson scores due to the exactly 4 cover-page booklet bars added by the booklet template, which causes a mismatch against primary score movement bars.
   - **Next Blocker:** **Bar alignment quality gate / booklet cover-page bar alignment**. Reconciling and aligning movement/booklet cover page bars is the next blocker.
2. **Melodic Soloing Score (`private_input_custom_melodic_soloing`)**:
   - **Classification:** `gp_output_empty_or_near_empty`
   - **Quality:** Note count is 0. 59 fret candidates are 100% unmatched.
   - **Next Blocker:** **Note matching & barline construction**.

---

## 3. Public Test Verification

We added 6 new unit tests in `tests/test_gp_quality_audit.py` to cover all quality classification logic:
1. `test_classify_gp_quality_basic_pass`: Verifies highly populated, non-empty, and aligned scores without technique candidates pass basic validation.
2. `test_classify_gp_quality_empty_or_near_empty`: Confirms that GP outputs with zero notes are flagged.
3. `test_classify_gp_quality_fret_matching_suspect`: Asserts that a low fret match rate (< 40%) is flagged as suspect.
4. `test_classify_gp_quality_technique_loss_expected`: Confirms that scores with excellent note coverage but un-serialized technique candidates are flagged as technique-loss-expected.
5. `test_classify_gp_quality_serialized_coverage_low` (NEW): Asserts that high ScoreIR notes but low GPIF notes (< 70%) is classified as `gp_output_note_coverage_low`.
6. `test_classify_gp_quality_measure_mismatch` (NEW): Asserts that a GPIF/ScoreIR measure count mismatch is classified as `gp_output_bar_alignment_suspect`.

**All 430 public unit and integration tests in the repository pass perfectly.**

---

## 4. Private-Safety Audit

- **Verification Command:** `git ls-files fixtures/private work`
- **Output:** `fixtures/private/.gitkeep`
- **Result:** **No private files, private PDFs, or work outputs were committed.** The private-safety invariant is strictly maintained.

---

## 5. Recommended Next Branch

`feature/bar-alignment-quality-gate-v0.1`
Given that the strict checks flag the custom lessons as `gp_output_bar_alignment_suspect` due to the cover-page booklet bar setup, the recommended next branch is `feature/bar-alignment-quality-gate-v0.1` to build a clean alignment gate and movement-aware booklet compiler to resolve cover-page mismatches.
