# ScoreToGP Run Record - ASCII Alignment Sidecar Hash Validation v0.1

## Repo and Branches
- **Repository**: tticom/score2gp / tticom/score2gp-agentops
- **Product Branch**: `feature/ascii-alignment-sidecar-validation-v0.1` (merged via Product PR #174)
- **Agentops Branch**: `run/ascii-alignment-sidecar-validation-v0.1`
- **Product PR**: #174 (https://github.com/tticom/score2gp/pull/174)
- **Product Head SHA**: `2d57923196dcd3c46278c15f184292bd7e8ee447` (Initial commit: `7184318cb9f3b7fac0944143351db69e6d1115a3`)
- **Product Merge Commit**: `385de47d630a88c9557377b5b26e120d51de20e5`
- **Merged Timestamp**: `2026-06-06T16:52:02Z`

## Prompt Chain
- Prompt manifest: [prompt-manifest.json](prompt-manifest.json)
- Operative prompt: [prompts/001-ascii-alignment-sidecar-hash-validation-v0.1.md](prompts/001-ascii-alignment-sidecar-hash-validation-v0.1.md)
- Prompt files:
  - [prompts/001-ascii-alignment-sidecar-hash-validation-v0.1.md](prompts/001-ascii-alignment-sidecar-hash-validation-v0.1.md)

## Files Changed

### Product Repository (`score2gp`):
- `src/score2gp/ascii_alignment.py` (MODIFY)
- `src/score2gp/build_ir.py` (MODIFY)
- `tests/test_ascii_scoreir_gate.py` (MODIFY)

### Agentops Repository (`score2gp-agentops`):
- `projects/score2gp/runs/2026-06-06-ascii-alignment-sidecar-hash-validation-v0.1/RUN.md` (NEW)
- `projects/score2gp/runs/2026-06-06-ascii-alignment-sidecar-hash-validation-v0.1/prompt-manifest.json` (NEW)
- `projects/score2gp/runs/2026-06-06-ascii-alignment-sidecar-hash-validation-v0.1/prompts/001-ascii-alignment-sidecar-hash-validation-v0.1.md` (NEW)

## Input Availability
- **Inputs**: Private benchmark inputs are referenced only by anonymized labels in the private-safe audit summaries. No private PDF, MusicXML, GP package, score title, or generated artifact is committed or named here.

## Output Directory Path
- **Outputs Directory**: `work/private_e2e_smoke_v0_1` and `work/private_gp_quality_audit_v0_1`

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `pass` (All staves, measures, beats, and notes compile cleanly for playable inputs)
- **Remediation / Diagnostic Status**: `pass` (All E2E checks run correctly; 485 passed tests)
- **Generated File Existence**: `yes` (`ScoreIR` and `.gp` written for compatible inputs, refusal files written for unsupported inputs)
- **Semantic Round-Trip Status**: `verified` (Successful compilation paths continue to match note counts and generate valid GP files)

## Key Implementation Summary
- **Mandatory Source Hashes**: Enforces validation of SHA-256 source file hashes for active PDF and MusicXML files at the ASCII ScoreIR gate. Legacy hashless sidecars do not pass.
- **Chunked SHA-256 Computation**: Implemented a deterministic chunked SHA-256 reader helper `compute_sha256(path: Path) -> str` that reads files safely in 64KB blocks.
- **No Silent Repair**: `_alignment_payload` writes hashes only when generating fresh sidecar files. At gate validation time, existing JSON is deserialized directly into Pydantic models without mutating or repairing hashes.
- **Structured Exit Gating**: Refuses stale/missing/malformed hashes with category `ascii_alignment_stale_sidecar_hash`, mapping it to CLI exit code `4`.

## Non-Goals Kept
- No ASCII conversion implementation
- No rhythm inference
- No OCR
- No weakening of existing gates
- No private/generated artifacts committed

## Private-Safe E2E Smoke Metrics

| Input Label | Status | Quality Category | Notes | Matched | First Blocker / Refusal Code |
| :--- | :---: | :--- | :---: | :---: | :--- |
| `private_input_1` | `pass` | `gp_output_technique_loss_expected` | 153 | 153 | `none` |
| `private_input_2` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | `pdf_input_class_ascii_tab_requires_alignment` |
| `private_input_custom` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | `pdf_input_class_missing_musicxml_sidecar` |
| `private_input_custom_lesson_3` | `pass` | `gp_output_technique_loss_expected` | 459 | 459 | `none` |
| `private_input_custom_lesson_4` | `pass` | `gp_output_technique_loss_expected` | 546 | 546 | `none` |
| `private_input_custom_lesson_5` | `pass` | `gp_output_technique_loss_expected` | 295 | 295 | `none` |
| `private_input_custom_lesson_6` | `pass` | `gp_output_technique_loss_expected` | 235 | 235 | `none` |
| `private_input_custom_lesson_7` | `pass` | `gp_output_technique_loss_expected` | 624 | 624 | `none` |
| `private_input_custom_melodic_soloing` | `pass` | `gp_output_technique_loss_expected` | 82 | 82 | `none` |

## Test Coverage
The following unit tests are added or updated to cover hash validation:
- `test_ascii_gate_refuses_missing_pdf_hash` (verifies missing PDF hash raises error)
- `test_ascii_gate_refuses_missing_musicxml_hash` (verifies missing MusicXML hash raises error)
- `test_ascii_gate_refuses_mismatched_pdf_hash` (verifies mismatched PDF hash raises error)
- `test_ascii_gate_refuses_mismatched_musicxml_hash` (verifies mismatched MusicXML hash raises error)
- `test_ascii_gate_accepts_matching_hashes` (verifies valid matching hashes pass cleanly)
- `test_cli_exit_code_maps_stale_ascii_sidecar_to_4` (verifies exit code mapping maps to 4)
- `test_ascii_gate_refuses_malformed_hashes` (verifies explicit `"malformed"` hash length validation status)

## Exact Verification Commands Run

### 1. Focused Gate Test Suite:
```bash
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_ascii_scoreir_gate.py
```
* **Result**: **PASS** (25/25 items passed cleanly).

### 2. Focused CLI Convert Test Suite:
```bash
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_convert.py
```
* **Result**: **PASS** (11/11 items passed cleanly).

### 3. Public Test Suite:
```bash
PYTHONPATH=. .venv/bin/pytest
```
* **Result**: **100% PASS** (485/485 items passed cleanly).
* *Evidence note*: The PR body earlier recorded 484 passed, but the final validation has 485 passed due to post-review additions of `test_ascii_gate_refuses_malformed_hashes`.

### 4. Private E2E Smoke Tests:
```bash
PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py
```
* **Result**: **PASS** (all checks matched/gated successfully).

### 5. Private GP Quality Audit:
```bash
PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
```
* **Result**: **PASS** (stable matching).

### 6. Private-Safety Audit:
```bash
git ls-files fixtures/private work
```
* **Result**: Outputs exactly:
  ```text
  fixtures/private/.gitkeep
  ```
  Strict private-safety invariant is fully preserved.

### 7. Git Diff Check:
```bash
git diff --check
```
* **Result**: Clean.

## Limitations
- Source-file validation requires active PDF and MusicXML source paths to remain present on the local filesystem during build-time evaluation.

## Next Bounded Increment Recommendation
After this run record is merged, the next bounded product increment for the ASCII sidecar workflow will be decided. A likely next decision point is to inspect specifically failing ASCII inputs or improve sidecar diagnostics further. Broad ASCII conversion or OCR changes must not be started without concrete evidence.
