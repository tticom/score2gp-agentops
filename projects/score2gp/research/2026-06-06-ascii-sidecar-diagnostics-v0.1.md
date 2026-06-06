# ASCII Sidecar Diagnostics Improvement Investigation v0.1

## Verified State
- **Product PR #174**: Merged at commit `385de47d630a88c9557377b5b26e120d51de20e5` in `tticom/score2gp`.
- **Governance PR #47**: Merged at commit `6a4a8c84938c762ec233b55fc915e02bff1fec13` in `tticom/score2gp-agentops`.
- **Active Files Inspected**:
  - `src/score2gp/ascii_alignment.py`
  - `src/score2gp/build_ir.py`
  - `src/score2gp/cli.py`
  - `tests/test_ascii_scoreir_gate.py`
  - `tests/test_cli_convert.py`

## Current Diagnostic Behavior
- **Missing / Mismatched Sidecar Hash**: Raises `BuildIrInputRiskError` with category `ascii_alignment_stale_sidecar_hash`.
- **Malformed Sidecar Hash**: Correctly raises `BuildIrInputRiskError` and classifies the status as `"malformed"`.
- **Diagnostics Payload**: Populates `details` with `hash_diagnostics` dict specifying `pdf_hash_status` and `musicxml_hash_status` values (`missing`, `mismatch`, `malformed`, `missing_active_file`).
- **Remediation Mapping**: `_ascii_gate_remediation()` defines a specific hint string for each refusal reason code under `"expected_next_remediation"`.

## Current Diagnostic Surfaces
- **Exception Details**: Stored inside the error details and serialized in the intermediate diagnostics JSON.
- **CLI Exit Code**: Maps to `4`.
- **CLI Stderr**: Prints `refusal_code` and `recommended_action`.
- **JSON Report**: Includes `refusal_code` and `recommended_action`.
- **HTML Report**: Correctly renders status, verdict, and the suggested remediation text from `expected_next_remediation`.

## Gaps
1. **Key Mismatch in CLI/JSON Report**: The CLI catch-block in `cli.py` extracts the user-facing remediation hint via `exc.details.get("remediation_hint")`. However, `_apply_ascii_gate_refusal_details` in `build_ir.py` populates the key `"expected_next_remediation"`. Consequently, both the CLI stderr printout and the `--json-report` fall back to the generic string `"Check the intermediate diagnostics report for details."` instead of displaying the actual remediation message.
2. **Detailed Diagnostics Hidden on Stderr**: The CLI stderr output does not specify which hash failed or the failure type (missing vs mismatched) unless the user opens the intermediate diagnostics JSON.

## Privacy Assessment
The current diagnostics do not leak absolute paths, private labels, or private score names. Only relative/generic error labels are exposed in user-facing reports.

## Recommendation
Verdict: **Implement diagnostics improvement now**. Addressing the key mismatch is a low-risk, high-value improvement that ensures specific, actionable hints are immediately visible to users.

## Proposed Smallest Implementation Increment
- **Branch**: `feature/ascii-sidecar-diagnostics-v0.1`
- **Likely Files to Change**:
  - `src/score2gp/build_ir.py`
  - `tests/test_cli_convert.py`
- **Test Names to Add/Update**:
  - `test_cli_convert_hash_refusal_contains_specific_remediation_hint`
  - `test_cli_convert_hash_refusal_displays_correct_active_hash`
- **Acceptance Criteria**:
  - `remediation_hint` is populated in the exception details for all ASCII gate refusals.
  - If a hash mismatch or missing hash error occurs, the actual computed (correct) hash of the active file is included in the diagnostics details (under `pdf_actual_hash` and/or `musicxml_actual_hash`) and printed as part of the recommended action on CLI stderr.
  - The CLI convert command outputs the specific hint and correct active hash on stderr.
  - The `--json-report` output contains the correct hint and active hash status.
  - All public and private tests continue to pass.
- **Stop Conditions**: Stop if the task requires changing the sidecar schema version or altering non-ASCII conversion paths.

## Developer Prompt
```text
Title: Fix ASCII sidecar gate remediation hint key mismatch and print correct active hashes

Context:
In build_ir.py, ASCII ScoreIR gate refusals populate the details dictionary with expected_next_remediation. However, cli.py attempts to read remediation_hint. This mismatch causes the convert CLI output and --json-report to default to a generic fallback. Furthermore, when a sidecar hash mismatch occurs, the user does not see the correct active hash on stderr to fix the sidecar.

Goal:
Unify the remediation keys and expose the correct active hashes on mismatch.

Requirements:
1. In src/score2gp/build_ir.py, inside _apply_ascii_gate_refusal_details, add "remediation_hint": _ascii_gate_remediation(primary) to the details update payload.
2. In src/score2gp/build_ir.py, inside _ascii_scoreir_gate, if a mismatch or missing hash is found in the sidecar, include the correct active file's computed SHA-256 hash in details as "pdf_actual_hash" and/or "musicxml_actual_hash".
3. Dynamically append the correct active hash(es) to the remediation hint or CLI stderr message so that the user receives an actionable prompt containing the exact correct hash (e.g. "Expected PDF hash <hash> in sidecar, but active file hash is <actual_hash>").
4. In tests/test_cli_convert.py, add a test test_cli_convert_hash_refusal_displays_correct_active_hash using tmp_path that triggers a stale hash refusal and asserts:
   - exit_code is 4
   - recommended_action in the JSON report matches the expected remediation hint and contains the correct active hash
   - recommended_action printed to CLI stderr contains the correct active hash
5. Run all tests and verify they pass.

Non-goals:
- Do not implement ASCII conversion or rhythm inference.
- Do not implement OCR.
- Do not commit private/generated artifacts.
```

## Non-Goals
No ASCII conversion, rhythm inference, or OCR is part of this increment.

