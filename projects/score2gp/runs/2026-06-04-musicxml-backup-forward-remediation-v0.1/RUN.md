# Run Record: MusicXML Backup/Forward Underfull Remediation v0.1

Durable record of the MusicXML timing preflight remediation implementation for underfull duplicate staff/TAB measures, public unit and integration test suite, and E2E validation against the private benchmark ladder.

## Metadata
- **Run ID**: `2026-06-04-musicxml-backup-forward-remediation-v0.1`
- **Product Repository**: `tticom/score2gp`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Branch**: `feature/musicxml-backup-forward-remediation-v0.1`
- **Product PR**: #167 (https://github.com/tticom/score2gp/pull/167)
- **Product Head SHA**: `93e19d7`
- **Agentops Branch**: `agent/musicxml-backup-forward-remediation-v0.1`

---

## 1. Architectural Strategy & Implementation

This run addresses the false-positive fatal timing blockers on `private_input_1` (Derek Trucks BB King) caused by `musicxml_unbalanced_backup_forward` (15 occurrences). These occur because the OMR writer uses `<backup>` elements to transition between the notation staff (voice 1) and the TAB staff (voice 5). Since both staves end underfull (e.g. 45 divisions instead of expected 48), the final global parsing cursor remains underfull, which was previously flagged as a fatal timing error.

We implement a narrow remediation pass that downgrades `musicxml_unbalanced_backup_forward` and `musicxml_backup_forward_alignment_ambiguous` from `error` to `warning` only under specific, strict safety conditions.

### Exact Downgrade Conditions:
1. `allow_remediation=True` is passed to the parser (so no global relaxation of timing gates occurs).
2. The measure has `voice_cursor_diagnostics`.
3. The measure is underfull-only, not overfull.
4. The same-voice overlap count is exactly 0 (`vcd.same_voice_overlap_count == 0`).
5. The backup element does not rewind before the measure start (`measure.backup_rewinds_before_measure_start` is false).
6. The forward element does not exceed the measure end (`measure.forward_exceeds_measure_end` is false).
7. No fatal overfull issues exist for the measure (`musicxml-overfull-bar` or `musicxml_compound_meter_overfull`).
8. No fatal same-voice overlap or rest/note overlap issues exist for the measure.
9. No `musicxml_invalid_duration_grid` fatal issue exists.
10. Duplicate staff/TAB voice evidence is present via the existing duplication classifier (confirmed voice pair has notes present in the measure).

### Changes in `src/score2gp/musicxml.py`
- Added the safety check helper `_can_remediate_backup_forward_drift(measure, measure_issues, confirmed_pairs)`.
- Integrated this helper inside `analyze_musicxml_timing(...)` immediately after collecting all measure timing issues but before the count for `musicxml_many_timing_risks` is computed.
- Downgrades matching issues to `warning` if all conditions are satisfied.

---

## 2. Public Test Results

All 459 public tests passed cleanly:

```text
============================= 459 passed in 9.85s ==============================
```

### Changes in Test Suite (`tests/test_musicxml_voice_cursor.py`)
Added two new synthetic tests:
1. **`test_vc_underfull_backup_forward_remediation`**:
   - Verifies that `allow_remediation=True` successfully downgrades underfull-only backup/forward drift to warnings.
   - Verifies that `allow_remediation=False` keeps the same drift fatal (as error).
2. **`test_vc_remediation_bounds_and_overlaps`**:
   - Verifies that overfull measures with backup/forward remain fatal.
   - Verifies that same-voice overlaps with backup/forward remain fatal.
   - Verifies that backup rewinding before measure start remains fatal.
   - Verifies that forward exceeding measure end remains fatal.

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
| `private_input_custom_melodic_soloing` | `pass` | `gp_output_technique_loss_expected` | 82 | 82 | 82 | No | Yes |
| `private_input_1` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 | - | - |

### Observations & E2E Findings:
- **`private_input_1` now successfully passes the MusicXML timing preflight gate** (`"musicxml_timing_preflight_status": "safe"`).
- **`musicxml_unbalanced_backup_forward` fatal timing count for `private_input_1` dropped from 15 to 0**.
- **No other MusicXML timing blockers remain** for `private_input_1` (it fails at the subsequent stage `"tabraw-import"` due to PDF text extraction grouping issues `"partial_pdf_grouping"`, which is expected and correct).
- **Lessons 3–7 and Melodic Soloing match counts remain perfectly stable**.

---

## 4. Verification & Testing

### Executed Validation Command Block & Outcomes

```bash
# 1. Run unit and integration tests
PYTHONPATH=. .venv/bin/python3 -m pytest

# 2. Run private pipeline and quality audit
PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py

# 3. Check workspace whitespace/diff check
git diff --check

# 4. Verify git tracked private files
git ls-files fixtures/private work
```

### Outcomes & Evidence:
1. **Full Public Test Suite**: `459 passed` (all unit and integration tests, including new voice cursor remediation tests).
2. **Quality Audit**: Verified stability of Lessons 3–7, Melodic Soloing, and confirmed drop of all fatal backup/forward errors on `private_input_1`.
3. **Git Whitespace Check**: `git diff --check` completed successfully.
4. **Private-Safety Invariant Audit**: `git ls-files fixtures/private work` outputs exactly:
   ```text
   fixtures/private/.gitkeep
   ```
