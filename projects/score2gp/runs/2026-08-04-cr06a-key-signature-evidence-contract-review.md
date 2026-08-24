# Formal Review Record — CR-06A Key Signature Evidence Contract & Fallback Removal

- **Target Repository**: `tticom/score2gp`
- **Target PR**: #403
- **Head SHA**: `ce00f73f75b47e4599d28da720cdd8fe8c8ef237`
- **Branch**: `agy/cr06a-key-signature-evidence-contract`
- **Reviewer Role**: Sceptical Reviewer (Hard-Review Protocol)
- **Verdict**: **`APPROVED`**

---

## 1. Summary of Changes

Developer slice **CR-06A** implements key signature evidence contracts and removes unevidenced default assumptions:
1. **Removed Default `C Major` Fallback**: Replaced hardcoded `key_sig = "C Major"` default in [`src/score2gp/notation_omr/pitch.py`](file:///home/tticom-codex/work/score2gp-workspace/score2gp/src/score2gp/notation_omr/pitch.py) with explicit `key_signature_status` tracking (`EVIDENCED`, `UNKNOWN`, `AMBIGUOUS`).
2. **Zero Alterations for Unevidenced Staves**: Unevidenced staves set `key_signature_status = "UNKNOWN"` and `resolved_key_signature = None`, applying 0 key signature alterations.
3. **CLI Report Formatting**: Updated [`src/score2gp/cli.py`](file:///home/tticom-codex/work/score2gp-workspace/score2gp/src/score2gp/cli.py) `_format_diagnostics_report` to format unevidenced or `UNKNOWN` key signatures as `Key Signature: Unknown` instead of `C Major`.
4. **Unit Test Suite**: Added 4 unit tests in [`tests/test_cr06_key_signature_semantics.py`](file:///home/tticom-codex/work/score2gp-workspace/score2gp/tests/test_cr06_key_signature_semantics.py) covering unevidenced staves, explicit valid key signatures, ambiguous key signatures, and CLI report formatting.

---

## 2. Adversarial Probes & Evidence Ledger

| Claim | Inspected File / Code | Executed Probe / Counterexample | Observed Output & Oracle | Classification |
| :--- | :--- | :--- | :--- | :--- |
| **Unevidenced Staves Report `UNKNOWN`** | `pitch.py#L201-L203` | Candidate processed with `explicit_key_signature=None`. | `key_signature_status == "UNKNOWN"`, `resolved_key_signature is None`, 0 alterations applied. | **VERIFIED** |
| **Evidenced Key Signatures Apply Alterations** | `pitch.py#L205-L208` | `explicit_key_signature="F Major"` passed for B4 staff candidate. | Pitch altered from B4 (71) to Bb4 (70), `key_signature_status == "EVIDENCED"`. | **VERIFIED** |
| **Ambiguous Key Signatures Handle Safely** | `pitch.py#L209-L210` | Nonexistent key `"Invalid Nonexistent Key"` passed. | `key_signature_status == "AMBIGUOUS"`, `resolved_key_signature is None`, 0 alterations. | **VERIFIED** |
| **CLI Formatting** | `cli.py#L234-L249` | Tested data dicts with `UNKNOWN`, `AMBIGUOUS`, `EVIDENCED`, and empty status. | Formats as `"Key Signature: Unknown"`, `"Key Signature: Ambiguous"`, `"Key Signature: D Major"`. | **VERIFIED** |

---

## 3. Disconfirmation & Sabotage Verification

- **Sabotage Test**: Sabotaged `map_clef_resolved_staff_pitch` to default `key_signature_status` back to `"C Major"`. `test_cr06_key_signature_unevidenced_returns_unknown` immediately failed with `AssertionError`.
- **Verification Commands Executed**:
  - `.venv/bin/python -m pytest tests/test_cr06_key_signature_semantics.py` (4 passed)
  - `.venv/bin/python scripts/agent_verify.py` (1078 passed, 1 skipped)

---

## 4. Verdict & Next Task Authorization

- **Verdict**: **`APPROVED`**
- **Suggested Next Step**: Merge PR #403 in `tticom/score2gp`, then promote next backlog slice **CR-06B** in `score2gp-agentops`.
