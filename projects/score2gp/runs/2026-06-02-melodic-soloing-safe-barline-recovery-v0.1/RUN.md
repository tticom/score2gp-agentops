# Run Record: Melodic Soloing Safe Barline Recovery Pass v0.1

Durable record of the melodic soloing safe barline recovery implementation and validation.

## Metadata
- **Run ID**: `2026-06-02-melodic-soloing-safe-barline-recovery-v0.1`
- **Product Repository**: `tticom/score2gp`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Branch**: `feature/melodic-soloing-safe-barline-recovery-v0.1`
- **Product Commit**: `1097c43659e806e3c6a2a8e348cc8ffd6923d473`
- **Agentops Branch**: `agent/melodic-soloing-safe-barline-recovery-v0.1`

---

## 1. Strategy & Implementation

We addressed the melodic soloing note loss due to candidate-to-TAB association loss with the following safe pass:
1. **Double-Barline Tolerance**: Replaced the hardcoded `6.0` check in `filter_tab_barline_candidates` (clustering and ambiguity checks) with a named constant `DOUBLE_BARLINE_CLUSTERING_TOLERANCE = 12.0` and used `<=` comparison.
2. **Strict Inheritance Check**: Gated partner barline inheritance behind `if len(valid_barlines) < 3:`.
3. **No Spurious Rejection Accumulation**: Only accumulated partner rejection reasons and details when internal barlines were actually inherited from the partner (`if inherited_from_partner:`).
4. **Skip Recovery Refinement**: Modified the unboxed recovery skip loop in `build_ir.py` to skip/ignore warnings that have `"severity": "info"`.

---

## 2. Public Test Results

All 450 public tests passed cleanly in the WSL environment:

```text
============================= 450 passed in 13.01s =============================
```

### Key Additions in Test Suites
- **`tests/test_barline_recovery.py`**: Added coverage for:
  - Double barline clustering within 12.0 points.
  - Notation-to-TAB internal barline inheritance.
  - Informational warnings (like `pdf_barline_double_secondary`) not skipping systems during IR build.

---

## 3. Private Smoke & Quality Audit Results

The E2E smoke tests and quality audit were executed across all private inputs:

### Post-Serialization Quality Audit Table

| Input Label | Status | Quality Category | ScoreIR Notes | GPIF Notes | Matched Frets |
| :--- | :---: | :--- | :---: | :---: | :---: |
| `private_input_1` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 |
| `private_input_2` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 |
| `private_input_custom` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 |
| `private_input_custom_lesson_3` | `pass` | `gp_output_technique_loss_expected` | 451 | 451 | 451 |
| `private_input_custom_lesson_4` | `pass` | `gp_output_technique_loss_expected` | 546 | 546 | 546 |
| `private_input_custom_lesson_5` | `pass` | `gp_output_technique_loss_expected` | 295 | 295 | 295 |
| `private_input_custom_lesson_6` | `pass` | `gp_output_technique_loss_expected` | 115 | 115 | 115 |
| `private_input_custom_lesson_7` | `pass` | `gp_output_technique_loss_expected` | 624 | 624 | 624 |
| `private_input_custom_melodic_soloing` | `pass` | `gp_output_note_coverage_low` | 41 | 41 | 41 |

### Observations:
- **`private_input_custom_melodic_soloing` matched-note count improved from 16 to 41!**
- ScoreIR and GPIF note counts remained equal.
- Lessons 3–7 remained stable.
- The middle system remains missing because fragmented horizontal lines require a separate grouping strategy. We stop here and recommend the separate fragmented-line grouping branch.

---

## 4. Verification & Testing

### Executed Validation Command Block & Outcomes

```bash
# 1. Run new barline recovery tests
wsl -d Ubuntu-24.04 -e sh -c "cd /home/tticom/work/score2gp-workspace/score2gp && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_barline_recovery.py"

# 2. Run full public test suite
wsl -d Ubuntu-24.04 -e sh -c "cd /home/tticom/work/score2gp-workspace/score2gp && PYTHONPATH=. .venv/bin/python3 -m pytest"

# 3. Run private pipeline and quality audit
wsl -d Ubuntu-24.04 -e sh -c "cd /home/tticom/work/score2gp-workspace/score2gp && PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py && PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py"

# 4. Check workspace whitespace/diff check
wsl -d Ubuntu-24.04 -e sh -c "cd /home/tticom/work/score2gp-workspace/score2gp && git diff --check && git diff -- schemas"

# 5. Verify git tracked private files
wsl -d Ubuntu-24.04 -e sh -c "cd /home/tticom/work/score2gp-workspace/score2gp && git ls-files fixtures/private work"
```

### Outcomes & Evidence:
1. **Targeted Tests**: `3 passed`.
2. **Full Public Test Suite**: `450 passed`.
3. **Quality Audit**: Melodic soloing matched notes improved from 16 to 41. Lessons 3-7 stable.
4. **Git Whitespace & Schema Check**: Completed successfully (clean).
5. **Private-Safety Invariant Audit**: `git ls-files fixtures/private work` outputs exactly:
   ```text
   fixtures/private/.gitkeep
   ```
