# Run Record: Melodic Soloing Fragmented TAB Staff-Line Grouping Pass v0.1

Durable record of the melodic soloing fragmented TAB staff-line grouping implementation and validation.

## Metadata
- **Run ID**: `2026-06-03-melodic-soloing-fragmented-line-grouping-v0.1`
- **Product Repository**: `tticom/score2gp`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Branch**: `feature/melodic-soloing-fragmented-line-grouping-v0.1`
- **Product PR**: #163
- **Product Head SHA**: `9bdcf04ab84a991f68c74fe78076f7434e41e6e3`
- **Product Merge Commit**: `1ce31296b5589a7c8ebd45a350ab4aab4f5640c6`
- **Agentops Branch**: `agent/melodic-soloing-fragmented-line-grouping-v0.1`

---

## 1. Strategy & Implementation

We resolved the missing middle system in `private_input_custom_melodic_soloing` by implementing a conservative wide-gap horizontal staff-line merging strategy in `src/score2gp/pdf.py`:
1. **Gap Classification**: Gaps between collinear segments are categorized into close-gap (<= 120.0 points) and wide-gap (> 120.0 and <= 360.0 points) regimes.
2. **Close-Gap Regime (<= 120.0)**: Preserves the exact original behavior, allowing merges for gaps <= 5.0 points or when at least one continuous neighbor spans the gap, or matching split neighbors exist.
3. **Wide-Gap Regime (120.0 to 360.0)**: Gated by `FRAGMENTED_STAFF_LINE_NEIGHBOR_MAX_GAP = 360.0`. Merging is permitted only when **at least two** neighboring parallel segments span the gap continuously, vertical distance is restricted to the plausible TAB staff band (`2.0 <= abs(other_y - seg_y) <= 45.0`), and the left/right segments themselves are excluded from neighbor evidence.

---

## 2. Public Test Results

All 454 public tests passed cleanly:

```text
============================= 454 passed in 9.33s =============================
```

### Key Additions in Test Suites
- **`tests/test_pdf.py`**: Added coverage for:
  - Positive wide-gap merge with two spanning neighbors.
  - Negative wide-gap no-merge with only one spanning neighbor.
  - Negative wide-gap no-merge when neighbors are too far vertically.
  - Regression close-gap merge with one neighbor.

---

## 3. Private Smoke & Quality Audit Results

The quality audit was successfully executed across all private inputs:

### Post-Serialization Quality Audit Table

| Input Label | Status | Quality Category | ScoreIR Notes | GPIF Notes | Matched Frets |
| :--- | :---: | :--- | :---: | :---: | :---: |
| `private_input_1` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 |
| `private_input_2` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 |
| `private_input_custom` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 |
| `private_input_custom_lesson_3` | `pass` | `gp_output_technique_loss_expected` | 459 | 459 | 459 |
| `private_input_custom_lesson_4` | `pass` | `gp_output_technique_loss_expected` | 546 | 546 | 546 |
| `private_input_custom_lesson_5` | `pass` | `gp_output_technique_loss_expected` | 295 | 295 | 295 |
| `private_input_custom_lesson_6` | `pass` | `gp_output_technique_loss_expected` | 235 | 235 | 235 |
| `private_input_custom_lesson_7` | `pass` | `gp_output_technique_loss_expected` | 624 | 624 | 624 |
| `private_input_custom_melodic_soloing` | `pass` | `gp_output_note_coverage_low` | 50 | 50 | 50 |

### Observations & Reviewer Deltas Verification:
- **`private_input_custom_melodic_soloing` matched-note count improved from 41 to 50!** Inferred system count increased from 2 to 3, proving the highly fragmented middle system was successfully recovered and grouped by merging its horizontal staff line segments.
  - *Known Limitation*: Melodic soloing matched notes improved to 50 but is still below expected full coverage. A follow-up active-blocker audit is needed to identify whether the remaining note loss is caused by timing/bar assignment, candidate extraction, MusicXML alignment, or another grouping limitation.
- **Lesson 3 matched count increased from 451 to 459**:
  - *Reviewer Conclusion*: This delta represents a **legitimate recovery** of staff lines that were fragmented by fret digits on system boundaries. By merging them under the neighbor constraint, these candidates are correctly assigned to string lines, with no warnings or category regressions.
- **Lesson 6 matched count increased from 115 to 235**:
  - *Reviewer Conclusion*: This delta represents a **legitimate recovery** of highly fragmented horizontal lines. System-detection warnings like `pdf-tab-system-not-detected` disappeared completely, and constructed bar boxes doubled from 5 to 10. These notes are correctly aligned and assigned to TAB staves with no false-positive geometry merging.
- **Lessons 4, 5, and 7 remained stable** at 546, 295, and 624 matched notes respectively.
- **Quality Categories**: All Lessons 3–7 remain as `pass` status under category `gp_output_technique_loss_expected`. Warning categories showed no new fatal grouping, ambiguous grouping, or false-positive system/bar assignment.
- **ScoreIR and GPIF note counts**: Remained perfectly equal across all files (Lesson 3: 459/459, Lesson 6: 235/235, Melodic Soloing: 50/50).

---

## 4. Verification & Testing

### Executed Validation Command Block & Outcomes

```bash
# 1. Run new PDF merging unit tests
wsl -d Ubuntu-24.04 -e sh -c "cd /home/tticom/work/score2gp-workspace/score2gp && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_pdf.py"

# 2. Run full public test suite
wsl -d Ubuntu-24.04 -e sh -c "cd /home/tticom/work/score2gp-workspace/score2gp && PYTHONPATH=. .venv/bin/python3 -m pytest"

# 3. Run private pipeline and quality audit
wsl -d Ubuntu-24.04 -e sh -c "cd /home/tticom/work/score2gp-workspace/score2gp && PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py && PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py"

# 4. Check workspace whitespace/diff check
wsl -d Ubuntu-24.04 -e sh -c "cd /home/tticom/work/score2gp-workspace/score2gp && git diff --check"

# 5. Verify git tracked private files
wsl -d Ubuntu-24.04 -e sh -c "cd /home/tticom/work/score2gp-workspace/score2gp && git ls-files fixtures/private work"
```

### Outcomes & Evidence:
1. **Targeted Tests**: `142 passed` (including 4 new tests).
2. **Full Public Test Suite**: `454 passed`.
3. **Quality Audit**: Melodic soloing matched notes improved to 50. Lessons 3 & 6 matched counts improved to 459 and 235.
4. **Git Whitespace & Schema Check**: Completed successfully (clean).
5. **Private-Safety Invariant Audit**: `git ls-files fixtures/private work` outputs exactly:
   ```text
   fixtures/private/.gitkeep
   ```
