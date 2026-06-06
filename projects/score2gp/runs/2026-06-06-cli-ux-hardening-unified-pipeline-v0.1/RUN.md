# ScoreToGP Run Record - CLI UX Hardening and Unified Convert Pipeline v0.1

## Repo and Branches
- **Repository**: tticom/score2gp / tticom/score2gp-agentops
- **Product Branch**: `feature/cli-ux-hardening-unified-pipeline-v0.1` (merged via Product PR #172)
- **Agentops Branch**: `run/cli-ux-hardening-unified-pipeline-v0.1`
- **Product PR**: #172
- **Product Head SHA**: `72a52a37e3037860f1f0dbe747fd21b06cca96c0`
- **Product Merge Commit**: `df3b328540af2bff2ff9e39e433fe44d2211b582`

## Prompt Chain
- Prompt manifest: [prompt-manifest.json](prompt-manifest.json)
- Operative prompt: [prompts/001-cli-ux-hardening-unified-pipeline-v0.1.md](prompts/001-cli-ux-hardening-unified-pipeline-v0.1.md)
- Prompt files:
  - [prompts/001-cli-ux-hardening-unified-pipeline-v0.1.md](prompts/001-cli-ux-hardening-unified-pipeline-v0.1.md)

## Files Changed

### Product Repository (`score2gp`):
- `src/score2gp/cli.py` (MODIFY)
- `tests/test_cli_convert.py` (MODIFY)
- `tests/test_orchestration.py` (MODIFY)

### Agentops Repository (`score2gp-agentops`):
- `projects/score2gp/runs/2026-06-06-cli-ux-hardening-unified-pipeline-v0.1/RUN.md` (NEW)
- `projects/score2gp/runs/2026-06-06-cli-ux-hardening-unified-pipeline-v0.1/prompt-manifest.json` (NEW)
- `projects/score2gp/runs/2026-06-06-cli-ux-hardening-unified-pipeline-v0.1/prompts/001-cli-ux-hardening-unified-pipeline-v0.1.md` (NEW)

## Input Availability
- **Inputs**: All standard private PDFs under `fixtures/private/` (e.g. `Lesson-3.pdf`, `Melodic Soloing Masterclass.pdf`, etc.)

## Output Directory Path
- **Outputs Directory**: `work/private_e2e_smoke_v0_1` and `work/private_gp_quality_audit_v0_1`

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `pass` (All staves, measures, beats, and notes compile cleanly for playable inputs)
- **Remediation / Diagnostic Status**: `pass` (All E2E checks run correctly; 478 passed tests)
- **Generated File Existence**: `yes` (`ScoreIR` and `.gp` written for compatible inputs, refusal files written for unsupported inputs)
- **Semantic Round-Trip Status**: `verified` (Successful compilation paths continue to match note counts and generate valid GP files)

## Key Implementation Summary
- **Unified Pipeline Orchestration**: Hardened `score2gp convert` into a unified user-facing pipeline.
- **Explicit CLI Options**: Added explicit options: `--pdf`, `--musicxml`, `--template`, `--out`, `--work-dir`, `--json-report`, and `--strict` / `--no-strict`.
- **Pipeline Stage Preservation**: Preserved pipeline ordering (PDF inspection/extraction -> MusicXML preflight/gating -> ScoreIR build -> GP package write/validation).
- **Structured Exit Codes**: Added structured exit-code mapping:
  - `0`: Success.
  - `1`: Missing input/path/dependency failure.
  - `2`: PDF layout/grouping refusal.
  - `3`: MusicXML timing/polyphony refusal.
  - `4`: ASCII/MusicXML alignment compatibility refusal.
  - `5`: GP writing/validation failure.
- **Priority Exit Code Gating**: Patched exit-code priority so `pdf_input_class_ascii_tab_requires_alignment` maps to exit code 4, not 2.
- **Output Safety and Stale File Protection**: Writes GP output to a temp file under `--work-dir`, validates it, and moves to `--out` only on success. Protects pre-existing output files on failure.
- **Strictness Exit Gating**: Ensures `--no-strict` still exits non-zero if no valid GP package is produced.
- **Tightened Report Contract**: Writes private-safe JSON report containing: `status`, `stage`, `exit_code`, `error_type`, `refusal_code`, `recommended_action`, `output_path`, `output_written`, `work_dir`, `diagnostics_paths`, `strict`, and summary counts.

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

## Exact Verification Commands Run

### 1. Public Test Suite:
```bash
PYTHONPATH=. .venv/bin/pytest
```
* **Result**: **100% PASS** (478/478 items passed cleanly).

### 2. Private E2E Smoke Tests:
```bash
PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py
```
* **Result**: **PASS** (all checks matched/gated successfully).

### 3. Private GP Quality Audit:
```bash
PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
```
* **Result**: **PASS** (153/153 matched on private_input_1, stable Lessons 3–7, stable Melodic Soloing at 82/82).

### 4. Private-Safety Audit:
```bash
git ls-files fixtures/private work
```
* **Result**: Outputs exactly:
  ```text
  fixtures/private/.gitkeep
  ```
  Strict private-safety invariant is fully preserved.

## Next Required Evidence
Run a fresh post-CLI release-readiness audit from product main to confirm the documented CLI contract, product docs, smoke tests, private quality audit, exit-code behaviour, and private-safety invariant all remain aligned.
