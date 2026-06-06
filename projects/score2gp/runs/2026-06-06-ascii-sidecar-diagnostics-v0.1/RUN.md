# ScoreToGP Run Record - ASCII Sidecar Diagnostics Improvement v0.1

## Repo and Branches
- **Repository**: tticom/score2gp / tticom/score2gp-agentops
- **Product Branch**: `feature/ascii-sidecar-diagnostics-v0.1` (merged via Product PR #175)
- **Agentops Branch**: `run/ascii-sidecar-diagnostics-v0.1`
- **Product PR**: #175 (https://github.com/tticom/score2gp/pull/175)
- **Product Head SHA**: `cc8c7ba3a62a5f14fd2f3dfc91ee99ba751177e6` (Initial commit: `281a23e57125d3f8ea4ce822583ab3730a8e8d0a`)
- **Product Merge Commit**: `5dbc57d81a942cf7b02db709f1816e885d518ce3`
- **Merged Timestamp**: `2026-06-06T18:50:04Z`

## Prompt Chain
- Prompt manifest: [prompt-manifest.json](prompt-manifest.json)
- Operative prompt: [prompts/001-ascii-sidecar-diagnostics-v0.1.md](prompts/001-ascii-sidecar-diagnostics-v0.1.md)

## Files Changed

### Product Repository (`score2gp`):
- `src/score2gp/build_ir.py` (MODIFY)
- `tests/test_cli_convert.py` (MODIFY)

### Agentops Repository (`score2gp-agentops`):
- `projects/score2gp/runs/2026-06-06-ascii-sidecar-diagnostics-v0.1/RUN.md` (NEW)
- `projects/score2gp/runs/2026-06-06-ascii-sidecar-diagnostics-v0.1/prompt-manifest.json` (NEW)
- `projects/score2gp/runs/2026-06-06-ascii-sidecar-diagnostics-v0.1/prompts/001-ascii-sidecar-diagnostics-v0.1.md` (NEW)

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `pass` (All staves, measures, beats, and notes compile cleanly for playable inputs)
- **Remediation / Diagnostic Status**: `pass` (All E2E checks run correctly; 487 passed tests)
- **Generated File Existence**: `yes` (Expected gate refusal behaviors matched)
- **Semantic Round-Trip Status**: `verified` (Successful compilation paths continue to compile without regressions)

## Key Implementation Summary
- **Remediation Key Mismatch Fix**: Populates both the HTML-diagnostics-consumed `expected_next_remediation` key and the CLI-consumed `remediation_hint` key during ASCII alignment gate refusals.
- **Specific Action Surface**: Surfaced the specific remediation hint (`re-align the source PDF and MusicXML files to update the stale hashes`) in both CLI stderr and the JSON report.
- **Scope Restriction**: The final PR intentionally does not expose full expected or actual hashes in user-facing remediation text to keep the diagnostics clean and focused.

## Non-Goals Kept
- No ASCII conversion implementation
- No rhythm inference
- No OCR
- No sidecar schema changes
- No private/generated artifacts committed
- No exposure of full expected/actual source hashes in user-facing remediation

## Test Coverage
The following unit tests are added/updated to cover diagnostics key mismatch and scope restriction:
- `test_cli_convert_hash_refusal_contains_specific_remediation_hint` (asserts exit code is 4, stderr contains the specific remediation hint, and the JSON report contains the same hint in `recommended_action`)
- `test_cli_convert_hash_refusal_does_not_print_full_hashes_in_remediation` (asserts exit code is 4, stderr and `recommended_action` contain the specific remediation hint, and neither stderr nor `recommended_action` leaks full fake expected or actual hash strings)

## Exact Verification Commands Run

### 1. Focused CLI Convert Test Suite:
```bash
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_convert.py
```
* **Result**: **PASS** (13/13 items passed cleanly).

### 2. Focused Gate Test Suite:
```bash
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_ascii_scoreir_gate.py
```
* **Result**: **PASS** (25/25 items passed cleanly).

### 3. Public Test Suite:
```bash
PYTHONPATH=. .venv/bin/pytest
```
* **Result**: **100% PASS** (487/487 items passed cleanly).

### 4. Private-Safety Audit:
```bash
git ls-files fixtures/private work
```
* **Result**: Outputs exactly:
  ```text
  fixtures/private/.gitkeep
  ```
  Strict private-safety invariant is fully preserved.

### 5. Git Diff Check:
```bash
git diff --check
```
* **Result**: Clean.
