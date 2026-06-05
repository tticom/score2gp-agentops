# Run Record: Fret Candidate Width & Digit-Merge Heuristics v0.1

Durable record of the fret candidate width refinement, digit-merge heuristic tightening, and safety checks on `private_input_1` and other private benchmark scores.

## Metadata
- **Run ID**: `2026-06-05-fret-refinement-tolerances-v0.1`
- **Product Repository**: `tticom/score2gp`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Branch**: `feature/private-input-1-fret-refinement-tolerances-v0.1`
- **Product Head SHA**: `7fb22eadcaf73d12928abfc7e2921da1348e5b9e`

---

## 1. Architectural Strategy & Implementation

This run refines fret candidate classification and digit-merge checks to resolve visual overlap/grouping blockers while preserving strict-mode accuracy.

### Key Implementation Details:
1. **Pipeline Verification**:
   - Confirmed that `system`, `string`, and `bar_index` assignments are already resolved and available when `_candidate_confidence` is called at line 1898 of `inspect_pdf`.
   - Utilized these assigned parameters inside the new helper `_is_plausible_narrow_fret_digit(...)` to make precise confidence decisions.
2. **Narrow Digit Safety Bound**:
   - Maintained `2.8pt` as the lower safety bound (`MIN_NARROW_FONT_FRET_DIGIT_WIDTH`).
   - In `_candidate_confidence`, widths `< 2.8pt` are always penalized. Widths between `2.8pt` and `4.0pt` only avoid the penalty if they are evaluated as plausible narrow digits (i.e. `_is_plausible_narrow_fret_digit` returns `True`).
3. **Technique Ligature vs Brackets**:
   - Refined `_split_technique_mixed_words` to apply the `4.0pt` width limit only when a real technique symbol (such as `h`, `p`, `s`, `v`, `b`, `r`, `~`, `/`, `\`) is present in the split word. Bracketed/parenthesized numbers (like `(8)`) are not technique ligatures, so they bypass this strict limit (threshold set to `2.0pt`), resolving false blockers on valid narrow bracketed digits.
4. **Tightened Repeated Digit Merging**:
   - Updated `_should_warn_unmerged_fret_digits` for repeated equal digits (e.g. `1` and `1`, `2` and `2`) to enforce a tight geometry limit `min(max_width * 1.0, 6.0)`.
   - Gaps larger than the character width suggest distinct sequential notes, representing "separate-note spacing evidence" and thus bypassing the unmerged warning.

---

## 2. Public Test Results

All 463 public tests passed cleanly:
```text
============================= 463 passed in 9.26s ==============================
```

### Updates to Test Suite (`tests/test_pdf.py`):
- Added `test_is_plausible_narrow_fret_digit` to verify the new helper logic.
- Updated `test_should_warn_unmerged_fret_digits` to verify that repeated digits like `1` + `1` with a tight gap warn appropriately, but repeated digits with wider spacing (e.g., `8` and `8` with gap `5.5` or `1` and `1` with gap `5.5` and width `2.0`) do not warn.
- Updated `test_narrow_font_valid_digit_confidence` to verify that `2.8pt` is the lower safety bound (confidence remains high for `2.84pt` but gets penalized for `2.76pt`).
- Added `test_narrow_font_noisy_digit_confidence` to verify that noise is correctly penalized.

---

## 3. Private Smoke & Quality Audit Results

### E2E Quality Audit Table
- **Strict Conversion Status**: Pass
- **Remediation/Diagnostic Status**: Pass (all resolved under default flow without `allow_skip_unboxed=True`)
- **Generated File Existence**: Yes
- **Semantic Round-Trip Status**: Valid
- **Exact Blocker Category**: None

| Input Label | Status | Quality Category | Notes | Matched |
| :--- | :---: | :--- | :---: | :---: |
| `private_input_1` | `pass` | `gp_output_technique_loss_expected` | 137 | 137 |
| `private_input_custom_lesson_3` | `pass` | `gp_output_technique_loss_expected` | 459 | 459 |
| `private_input_custom_lesson_4` | `pass` | `gp_output_technique_loss_expected` | 546 | 546 |
| `private_input_custom_lesson_5` | `pass` | `gp_output_technique_loss_expected` | 295 | 295 |
| `private_input_custom_lesson_6` | `pass` | `gp_output_technique_loss_expected` | 235 | 235 |
| `private_input_custom_lesson_7` | `pass` | `gp_output_technique_loss_expected` | 624 | 624 |
| `private_input_custom_melodic_soloing` | `pass` | `gp_output_technique_loss_expected` | 82 | 82 |

### Observations:
- **`private_input_1` compiles successfully under default settings** (no `allow_skip_unboxed=True` required).
- All lessons (Lessons 3–7) and Melodic Soloing match counts remain perfectly stable and correct.

---

## 4. Verification & Testing

### Verification Commands Run:
```bash
PYTHONPATH=. .venv/bin/pytest
PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py
python -m score2gp.cli export-schema --out schemas
python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
git diff --check
git ls-files fixtures/private work
```

### Outcomes & Evidence:
1. **Public test suite**: 463 passed.
2. **Private-Safety Invariant**: `git ls-files fixtures/private work` outputs exactly:
   ```text
   fixtures/private/.gitkeep
   ```
3. **Next Required Evidence**: PR Review and merging.
