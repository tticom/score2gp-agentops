# ScoreToGP Run Record - Layout Class and Missing Sidecar Safety Gates

## Repo and Branches
- **Repository**: score2gp / score2gp-agentops
- **Product Branch**: `feature/layout-class-and-sidecar-refinement-v0.1` (merged via Product PR #169)
- **Agentops Branch**: `run/layout-class-and-missing-sidecar-safety-gates-v0.1`
- **Product PR**: #169
- **Product Head SHA**: `addfc162ffa82ff2f9547d2b27d42cf38a4cd5b2`
- **Product Merge Commit**: `b9f54a40ffa963e83e91a2fd22070ec9eeff6d75`

## Prompt Chain
- Prompt manifest: [prompt-manifest.json](prompt-manifest.json)
- Operative prompt: [prompts/001-layout-class-and-sidecar-refusal-gates.md](prompts/001-layout-class-and-sidecar-refusal-gates.md)
- Prompt files:
  - [prompts/001-layout-class-and-sidecar-refusal-gates.md](prompts/001-layout-class-and-sidecar-refusal-gates.md)

## Files Changed

### Product Repository (`score2gp`):
- `src/score2gp/build_ir.py`
- `src/score2gp/pdf.py`
- `src/score2gp/private_diagnostics.py`
- `src/score2gp/report.py`
- `src/score2gp/tabraw.py`
- `tests/test_ascii_alignment.py`
- `tests/test_ascii_scoreir_gate.py`
- `tests/test_pdf.py`
- `tests/test_private_smoke.py`

### Agentops Repository (`score2gp-agentops`):
- `projects/score2gp/runs/2026-06-05-layout-class-and-missing-sidecar-safety-gates-v0.1/RUN.md`

## Input Availability
- **Inputs**: All standard private PDFs under `fixtures/private/` (e.g. `Lesson-3.pdf`, `Melodic Soloing Masterclass.pdf`, etc.)

## Output Directory Path
- **Outputs Directory**: `work/private_e2e_smoke_v0_1` and `work/private_gp_quality_audit_v0_1`

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `pass` (All staves, measures, beats, and notes compile cleanly for playable inputs; correct refusal codes are reported for unsupported inputs)
- **Remediation / Diagnostic Status**: `pass` (All E2E checks run correctly; 466 passed tests)
- **Generated File Existence**: `yes` (`ScoreIR` and `.gp` written for compatible inputs, refusal files written for unsupported inputs)
- **Semantic Round-Trip Status**: `verified` (Successful compilation paths continue to match note counts and generate valid GP files)

## Blocker and Diagnostics Resolved
- **Diagnostic warnings / refusal codes implemented**:
  - `pdf_input_class_ascii_tab_requires_alignment` (refuses ASCII tab without sidecar)
  - `pdf_input_class_missing_musicxml_sidecar` (refuses missing MusicXML sidecar)
  - `pdf_input_class_drawn_tab_requires_barlines` (refuses drawn TAB without barlines)
  - `pdf_input_class_scanned_pdf_unsupported` (refuses scanned/raster PDF)
  - `pdf_input_class_no_extractable_tab_geometry` (refuses scanned PDF with no vector geometry)

## Private-Safe E2E Smoke Metrics

| Input Label | Status | Quality Category | Notes | Matched | First Blocker / Refusal Code |
| :--- | :---: | :--- | :---: | :---: | :--- |
| `private_input_1` | `pass` | `gp_output_technique_loss_expected` | 137 | 137 | `none` |
| `private_input_2` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | `pdf_input_class_ascii_tab_requires_alignment` |
| `private_input_custom` (Rock Ballads) | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | `pdf_input_class_missing_musicxml_sidecar` |
| `private_input_custom` (Chord Melody) | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | `pdf_input_class_missing_musicxml_sidecar` |
| `private_input_custom` (Practice Lick) | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | `pdf_input_class_missing_musicxml_sidecar` |
| `private_input_custom` (Legato Licks) | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | `pdf_input_class_missing_musicxml_sidecar` |
| `private_input_custom_lesson_3` | `pass` | `gp_output_technique_loss_expected` | 459 | 459 | `none` |
| `private_input_custom_lesson_4` | `pass` | `gp_output_technique_loss_expected` | 546 | 546 | `none` |
| `private_input_custom_lesson_5` | `pass` | `gp_output_technique_loss_expected` | 295 | 295 | `none` |
| `private_input_custom_lesson_6` | `pass` | `gp_output_technique_loss_expected` | 235 | 235 | `none` |
| `private_input_custom_lesson_7` | `pass` | `gp_output_technique_loss_expected` | 624 | 624 | `none` |
| `private_input_custom_melodic_soloing` | `pass` | `gp_output_technique_loss_expected` | 82 | 82 | `none` |

## Exact Verification Commands Run

### 1. Public Test Suite:
```bash
PYTHONPATH=. .venv/bin/python3 -m pytest
```
* **Result**: **100% PASS** (466/466 items passed cleanly in 12.24s under WSL environment).

### 2. Private-Safety Audit:
```bash
git ls-files fixtures/private work
```
* **Result**: Outputs exactly:
  ```text
  fixtures/private/.gitkeep
  ```
  Strict private-safety invariant is fully preserved.

## Next Required Evidence
- None for this task. The gating/safety infrastructure is fully implemented, verified, and merged.
