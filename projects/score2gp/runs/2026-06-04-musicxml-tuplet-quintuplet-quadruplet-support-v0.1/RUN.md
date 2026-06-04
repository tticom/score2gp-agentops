# Run Record: MusicXML Quadruplet and Quintuplet Preflight Support v0.1

Durable record of the MusicXML timing preflight support implementation for quadruplets (4:3) and quintuplets (5:3), public unit and integration test suite, and E2E validation against the private benchmark ladder.

## Metadata
- **Run ID**: `2026-06-04-musicxml-tuplet-quintuplet-quadruplet-support-v0.1`
- **Product Repository**: `tticom/score2gp`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Branch**: `feature/musicxml-tuplet-quintuplet-quadruplet-support-v0.1`
- **Product Head SHA**: `191e8204af0145e1a5c2e9e8770483aed592ef1f`
- **Agentops Branch**: `agent/musicxml-tuplet-quintuplet-quadruplet-support-v0.1`

---

## 1. Architectural Strategy & Implementation

This run addresses the `musicxml_tuplet_unsupported` fatal timing preflight issues for `private_input_1` (Derek Trucks BB King). It implements narrow support for parsing quadruplets (`4:3`) and quintuplets (`5:3`) on compound meters.

### Key Changes in `src/score2gp/musicxml.py`

1. **Supported Tuplet Predicate**:
   - Added a helper `_is_supported_tuplet` that allows exactly:
     - triplets: `actual_notes == 3 and normal_notes == 2`
     - quadruplets: `actual_notes == 4 and normal_notes == 3`
     - quintuplets: `actual_notes == 5 and normal_notes == 3`
   - All other tuplet ratios remain unsupported.
2. **Unsupported Tuplet Flagging**:
   - Changed the assignment of `tuplet_unsupported` to rely on the helper predicate:
     ```python
     tuplet_unsupported = tuplet is not None and not _is_supported_tuplet(tuplet)
     ```

---

## 2. Public Test Results

All 457 public tests passed cleanly:

```text
============================= 457 passed in 11.07s =============================
```

### Key Additions in Test Suites
- **`tests/test_musicxml.py`**: Added `test_musicxml_tuplets_support` which creates a synthetic 12/8 measure containing:
  - Triplet `3:2` (verified supported)
  - Quadruplet `4:3` (verified supported)
  - Quintuplet `5:3` (verified supported)
  - Septuplet `7:4` (verified unsupported, triggers timing error)

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
| `private_input_1` | `fail` | `musicxml_timing_risk` (preflight) | 0 | 0 | 0 | - | - |

### Observations & E2E Findings:
- **`private_input_1` tuplet unsupported errors dropped from 67 to 0**.
- **Lessons 3–7 and Melodic Soloing match counts remain perfectly stable**.
- **Remaining Fatal Timing Blocker for `private_input_1`**:
  - `musicxml_unbalanced_backup_forward` (15 occurrences), causing timeline cursor offset misalignment (e.g. at Measure 1, where divisions leave the cursor at 45 instead of 48).

---

## 4. Verification & Testing

### Executed Validation Command Block & Outcomes

```bash
# 1. Run unit and integration tests
PYTHONPATH=. .venv/bin/python3 -m pytest

# 2. Run private pipeline and quality audit
PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py
PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py

# 3. Check workspace whitespace/diff check
git diff --check

# 4. Verify git tracked private files
git ls-files fixtures/private work
```

### Outcomes & Evidence:
1. **Full Public Test Suite**: `457 passed` (all unit and integration tests).
2. **Quality Audit**: Verified stability of Lessons 3–7, Melodic Soloing, and confirmed drop of tuplet unsupported errors on `private_input_1`.
3. **Git Whitespace Check**: `git diff --check` completed successfully with no trailing whitespace or format errors.
4. **Private-Safety Invariant Audit**: `git ls-files fixtures/private work` outputs exactly:
   ```text
   fixtures/private/.gitkeep
   ```
