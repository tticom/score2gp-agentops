# ScoreToGP Run Record - MusicXML Grace Note Support v0.1

## Repo and Branches
- **Repository**: score2gp / score2gp-agentops
- **Product Branch**: `feature/grace-note-support-v0.1` (merged via Product PR #170)
- **Agentops Branch**: `run/musicxml-grace-note-support-v0.1`
- **Product PR**: #170
- **Product Head SHA**: `9d654a869296a8e6770b94a8276323728668467d`
- **Product Merge Commit**: `3c1941d5c8166ef3443367102ce6b25f1bd8dfef`

## Prompt Chain
- Prompt manifest: [prompt-manifest.json](prompt-manifest.json)
- Operative prompt: [prompts/001-musicxml-grace-note-support-v0.1.md](prompts/001-musicxml-grace-note-support-v0.1.md)
- Prompt files:
  - [prompts/001-musicxml-grace-note-support-v0.1.md](prompts/001-musicxml-grace-note-support-v0.1.md)

## Files Changed

### Product Repository (`score2gp`):
- `src/score2gp/build_ir.py`
- `src/score2gp/gpif.py`
- `src/score2gp/musicxml.py`
- `tests/test_musicxml.py`

### Agentops Repository (`score2gp-agentops`):
- `projects/score2gp/runs/2026-06-05-musicxml-grace-note-support-v0.1/RUN.md`

## Input Availability
- **Inputs**: All standard private PDFs under `fixtures/private/` (e.g. `Lesson-3.pdf`, `Melodic Soloing Masterclass.pdf`, etc.)

## Output Directory Path
- **Outputs Directory**: `work/private_e2e_smoke_v0_1` and `work/private_gp_quality_audit_v0_1`

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `pass` (All staves, measures, beats, and notes compile cleanly for playable inputs)
- **Remediation / Diagnostic Status**: `pass` (All E2E checks run correctly; 467 passed tests)
- **Generated File Existence**: `yes` (`ScoreIR` and `.gp` written for compatible inputs, refusal files written for unsupported inputs)
- **Semantic Round-Trip Status**: `verified` (Successful compilation paths continue to match note counts and generate valid GP files)

## Key Implementation Summary
- Parsed MusicXML grace notes and slash attribute.
- Deduplicated notation/TAB grace notes.
- Compiled grace notes as zero-duration pre-host events.
- Added GraceTiming / GraceTechnique metadata.
- Included grace notes in diagnostic/onset grouping.
- Sorted GPIF voice events so grace notes serialize before host events.

## Private-Safe E2E Smoke Metrics

| Input Label | Status | Quality Category | Notes | Matched | First Blocker / Refusal Code |
| :--- | :---: | :--- | :---: | :---: | :--- |
| `private_input_1` | `pass` | `gp_output_technique_loss_expected` | 153 | 153 | `none` |
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
* **Result**: **100% PASS** (467/467 items passed cleanly).

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
- Run a fresh post-grace-note active-blocker audit from product main to determine the next highest-value project task now that private_input_1 has reached full candidate coverage.
