# Run Record: Melodic Soloing Internal Double-Barline Recovery v0.1

Durable record of the melodic soloing internal double-barline recovery implementation, public unit and integration test suite, and E2E validation against the private benchmark ladder.

## Metadata
- **Run ID**: `2026-06-03-melodic-soloing-internal-double-barline-recovery-v0.1`
- **Product Repository**: `tticom/score2gp`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Branch**: `feature/melodic-soloing-internal-double-barline-recovery-v0.1`
- **Product PR**: #165 (https://github.com/tticom/score2gp/pull/165)
- **Product Head SHA**: `15588c9933bb2064d6ceca7170bc2f29c0970f7a`
- **Product Merge Commit**: `47cf92c52408e8c1f2d08400f7e8a075d14ff266`
- **Related Research PR**: score2gp-agentops #29 (https://github.com/tticom/score2gp-agentops/pull/29)
- **Agentops Branch**: `agent/melodic-soloing-internal-double-barline-recovery-v0.1`

---

## 1. Architectural Strategy & Implementation

This run addresses the candidate-to-bar assignment loss identified in research PR #29, caused by internal double-barlines on TAB staves being rejected under the general `pdf_barline_ambiguous` taxonomy. 

### Key Refinements in `src/score2gp/pdf.py`

1. **Internal Size-2 Double-Barline Recovery**:
   - Internal size-2 TAB double-barline clusters are now conservatively resolved by accepting one representative line as valid and marking the secondary line as `pdf_barline_double_secondary` instead of rejecting both as ambiguous.
   - Larger internal clusters (size >= 3) remain classified as `pdf_barline_ambiguous`.

2. **Recovered Bar Boxes**:
   - Recovered the missing melodic soloing bar boxes from 5 to 8, establishing the necessary horizontal bounding boxes for candidate assignment.
   - Restored full melodic soloing note coverage to 82 matched notes.

---

## 2. Public Test Results

All 456 public tests passed cleanly:

```text
============================= 456 passed in 11.93s =============================
```

### Key Additions in Test Suites
- **`tests/test_pdf.py`**: Added unit tests verifying the internal size-2 double-barline recovery and the classification of secondary lines.

---

## 3. Private Smoke & Quality Audit Results

The quality audit was successfully executed across all private inputs:

### Post-Serialization Quality Audit Table

| Input Label | Status | Quality Category | ScoreIR Notes | GPIF Notes | Matched Frets | Deduplication | Spacing Applied |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| `private_input_custom_lesson_3` | `pass` | `gp_output_technique_loss_expected` | 459 | 459 | 459 | No | No |
| `private_input_custom_lesson_4` | `pass` | `gp_output_technique_loss_expected` | 546 | 546 | 546 | No | No |
| `private_input_custom_lesson_5` | `pass` | `gp_output_technique_loss_expected` | 295 | 295 | 295 | No | No |
| `private_input_custom_lesson_6` | `pass` | `gp_output_technique_loss_expected` | 235 | 235 | 235 | No | No |
| `private_input_custom_lesson_7` | `pass` | `gp_output_technique_loss_expected` | 624 | 624 | 624 | No | No |
| `private_input_custom_melodic_soloing` | `pass` | `gp_output_note_coverage_high` | 82 | 82 | 82 (improved from 56) | No | Yes |

### Observations & Alignment Diagnosis:
- **Lessons 3–7 remained stable and unaffected**.
- **`private_input_custom_melodic_soloing` note coverage improved significantly from 56 to 82**, matching the visual count. 
- **ScoreIR and GPIF note counts are equal** at 82.
- **Melodic soloing bar boxes** increased from **5** before to **8** after.
- **Next Required Action**: Run a fresh post-milestone private-safe baseline audit from product main to classify the next active blocker across all private fixtures, now that melodic soloing has reached full note coverage.

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
1. **Full Public Test Suite**: `456 passed`.
2. **Quality Audit**: Verified stability of Lessons 3–7 and Melodic Soloing note recovery to 82 matched notes.
3. **Git Whitespace Check**: `git diff --check` completed successfully with no trailing whitespace or format errors.
4. **Private-Safety Invariant Audit**: `git ls-files fixtures/private work` outputs exactly:
   ```text
   fixtures/private/.gitkeep
   ```
