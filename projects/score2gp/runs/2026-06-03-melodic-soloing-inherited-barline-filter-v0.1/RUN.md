# Run Record: Melodic Soloing Defensive Inherited-Barline Closeness Filter v0.1

Durable record of the melodic soloing defensive inherited-barline closeness filter implementation, public unit and integration test suite, and E2E validation against the private benchmark ladder.

## Metadata
- **Run ID**: `2026-06-03-melodic-soloing-inherited-barline-filter-v0.1`
- **Product Repository**: `tticom/score2gp`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Branch**: `feature/melodic-soloing-inherited-barline-filter-v0.1`
- **Product PR**: #164 (https://github.com/tticom/score2gp/pull/164)
- **Agentops Branch**: `agent/melodic-soloing-inherited-barline-filter-v0.1`

---

## 1. Architectural Strategy & Implementation

We implemented a batch/anchored notation-to-TAB inherited barline closeness filter to reject false internal measure splits (e.g. tuplet bracket hooks or note stems on notation staves) while preserving standard Lessons 3–7 and double-barline merging.

### Key Refinements in `src/score2gp/pdf.py`

1. **Closeness Threshold** (`MIN_INHERITED_INTERNAL_BAR_WIDTH`):
   - Added constant `MIN_INHERITED_INTERNAL_BAR_WIDTH = 130.0` points. 
   - Audited Lessons 3–7 measure widths and verified that all measures < 130.0 points are created by explicit barlines (`inh=False`), so 130.0 is non-regressive.

2. **Batch/Anchored Filtering**:
   - Refactored `_detect_tab_systems` notation-to-TAB inheritance. Enforces a range `(15.0, 130.0)` for closeness rejection.
   - Any inherited candidate from `partner_valid` is rejected as `pdf_barline_inherited_too_close` if it lies within this range of an explicit TAB anchor or another candidate.
   - Enforcing the lower bound `15.0` ensures legitimate close double barlines (spaced `<= 15.0` points apart) bypass the filter and merge correctly instead of being rejected.

3. **Diagnostics & Copying**:
   - Added `pdf_barline_inherited_too_close` warning taxonomy code and message.
   - Updated details log generator to construct copies `dict(det)` before updating, avoiding in-place mutation of the source list.

---

## 2. Public Test Results

All 455 public tests passed cleanly:

```text
============================= 455 passed in 13.59s =============================
```

### Key Additions in Test Suites
- **`tests/test_pdf.py`**: Added `test_notation_to_tab_barline_inheritance_filter` verifying:
  - Inherited internal barline rejection under 130.0.
  - Inherited internal barline acceptance >= 130.0.
  - Close pair batch-rejection without order dependency (bracket-hook pattern).
  - Explicit TAB barlines non-regression.
  - Normal notation-to-TAB inheritance works on standard systems.

---

## 3. Private Smoke & Quality Audit Results

The quality audit was successfully executed across all private inputs:

### Post-Serialization Quality Audit Table

| Input Label | Status | Quality Category | ScoreIR Notes | GPIF Notes | Matched Frets | Deduplication | Spacing Applied |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| `private_input_1` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 | No | No |
| `private_input_2` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 | No | No |
| `private_input_custom` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 | No | No |
| `private_input_custom_lesson_3` | `pass` | `gp_output_technique_loss_expected` | 459 | 459 | 459 | No | No |
| `private_input_custom_lesson_4` | `pass` | `gp_output_technique_loss_expected` | 546 | 546 | 546 | No | No |
| `private_input_custom_lesson_5` | `pass` | `gp_output_technique_loss_expected` | 295 | 295 | 295 | No | No |
| `private_input_custom_lesson_6` | `pass` | `gp_output_technique_loss_expected` | 235 | 235 | 235 | No | No |
| `private_input_custom_lesson_7` | `pass` | `gp_output_technique_loss_expected` | 624 | 624 | 624 | No | No |
| `private_input_custom_melodic_soloing` | `pass` | `gp_output_note_coverage_low` | 50 | 50 | 50 | No | Yes |

### Observations & Alignment Diagnosis:
- **Lessons 3–7 remained stable and unaffected** compared to main after PR #163.
- **`private_input_custom_melodic_soloing` remained at 50 matched notes**. Note counts in ScoreIR and GPIF are equal.
- This confirms that false inherited barlines were not the active note-loss blocker, but the patch correctly adds correctness checks preventing tuplet hooks from generating false measures.
- **Next Active Blocker**: Classified as **timing/onset alignment**. The log outputs `pdf_timing_mapping_not_implemented` for page 1 of melodic soloing. This blocks visual/horizontal onset mapping, forcing fallback timing alignment and leaving 32 notes unmatched.

---

## 4. Verification & Testing

### Executed Validation Command Block & Outcomes

```bash
# 1. Run unit and integration tests
python -m pytest

# 2. Run private pipeline and quality audit
python scripts/private_e2e_smoke.py
python scripts/private_gp_quality_audit.py

# 3. Check workspace whitespace/diff check
git diff --check

# 4. Verify git tracked private files
git ls-files fixtures/private work
```

### Outcomes & Evidence:
1. **Full Public Test Suite**: `455 passed`.
2. **Quality Audit**: Verified stability of Lessons 3–7 and Melodic Soloing notes.
3. **Git Whitespace Check**: `git diff --check` completed successfully with no trailing whitespace or format errors.
4. **Private-Safety Invariant Audit**: `git ls-files fixtures/private work` outputs exactly:
   ```text
   fixtures/private/.gitkeep
   ```
