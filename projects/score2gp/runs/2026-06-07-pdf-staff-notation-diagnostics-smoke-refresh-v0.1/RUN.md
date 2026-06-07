# ScoreToGP Run Record - PDF Notation Diagnostics Smoke Refresh

## Repo and Branches
- **Repository**: `tticom/score2gp` and `tticom/score2gp-agentops`
- **Product Branch**: `main` (PR #185 merged)
- **Agent-ops Branch**: `run/pdf-staff-notation-diagnostics-smoke-refresh-v0.1`
- **Commit Hash**: `5ddd1db7f42958420585a8c817a6344427e07cba`

## Relationship to Past PRs
* **PR #185 (Diagnostics Exceptions)**: Merged into `main`. The exception handling changes ensure that `inspect_pdf` outputs a private-safe warning status (`pdf_notation_geometry_diagnostics_failed`) instead of raising unhandled exceptions or exposing local paths/raw texts. This smoke refresh validates the stability of these changes.

## Prompt Chain
- **Prompt Manifest**: [prompt-manifest.json](prompt-manifest.json)
- **Operative Prompt**: [prompts/001-pdf-staff-notation-diagnostics-smoke-refresh.md](prompts/001-pdf-staff-notation-diagnostics-smoke-refresh.md)

## Plan Evidence
- **Implementation Plan**: [implementation_plan.md](implementation_plan.md)
- **Tasks**: [task.md](task.md)
- **Walkthrough**: [walkthrough.md](walkthrough.md)

## Files Changed

### Agent-ops Repository (`score2gp-agentops`):
* `projects/score2gp/runs/2026-06-07-pdf-staff-notation-diagnostics-smoke-refresh-v0.1/` (New run record directory)

## Smoke Test Inspection Metrics

Below are the aggregated metrics collected across all 12 private PDFs in `fixtures/private/` using the `inspect_pdf` pipeline:

| Label | Kind | Layout Class | Pages | Diags Status | Notation Staves | Line Count | Curve Count | Rect Count | Font Counts |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `private_input_1` | `born-digital` | `vector_tab_with_barlines` | 2 | `success` | 0 | 0 | 0 | 0 | `none` |
| `private_input_custom_rock_ballads` | `scanned-or-raster` | `scanned_no_extractable_text` | 177 | `success` | 0 | 0 | 0 | 0 | `none` |
| `private_input_custom_jazz_classics` | `scanned-or-raster` | `scanned_no_extractable_text` | 105 | `success` | 0 | 0 | 0 | 0 | `none` |
| `private_input_custom_practice_every_day` | `born-digital` | `vector_tab_with_barlines` | 2 | `success` | 0 | 0 | 0 | 0 | `none` |
| `private_input_custom_legato_licks` | `born-digital` | `mixed_unknown_layout` | 1 | `success` | 0 | 0 | 0 | 0 | `none` |
| `private_input_custom_lesson_3` | `born-digital` | `vector_tab_with_barlines` | 4 | `success` | 0 | 0 | 0 | 0 | `none` |
| `private_input_custom_lesson_4` | `born-digital` | `vector_tab_with_barlines` | 5 | `success` | 0 | 0 | 0 | 0 | `none` |
| `private_input_custom_lesson_5` | `born-digital` | `vector_tab_with_barlines` | 3 | `success` | 0 | 0 | 0 | 0 | `none` |
| `private_input_custom_lesson_6` | `born-digital` | `vector_tab_with_barlines` | 6 | `success` | 0 | 0 | 0 | 0 | `none` |
| `private_input_custom_lesson_7` | `born-digital` | `vector_tab_with_barlines` | 5 | `success` | 0 | 0 | 0 | 0 | `none` |
| `private_input_2` | `born-digital` | `born_digital_ascii_tab` | 1 | `success` | 0 | 0 | 0 | 0 | `none` |
| `private_input_custom_melodic_soloing` | `born-digital` | `vector_tab_with_barlines` | 1 | `success` | 0 | 0 | 0 | 0 | `none` |

### Summary Statistics
- **Total Files**: 12
- **Born-digital**: 10
- **Scanned**: 2
- **Total Pages**: 312
- **Diagnostics Success Rate**: 100% (All 12 files returned status `success`)
- **Notation Staves detected**: 0 (Expected as these files contain guitar tablature/layout classes, and standard staff detection correctly found no standard-staff notation groups matching spacing requirements)

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `pass` (Standard PDF inspection status)
- **Remediation / Diagnostic Status**: `pass` (All tests pass cleanly)
- **Generated File Existence**: `yes` (Inspection outputs written locally under `work/`)
- **Semantic Round-Trip Status**: `unaffected` (Core conversion code is unchanged)

## Validation Commands Run
```bash
env PYTHONPATH=src:. .venv/bin/pytest -q
git status
git ls-files fixtures/private work
```

## Private-Safety Audit
* Checked and verified that no private PDF assets, generated `.gp` packages, or inspection JSON reports are committed.
* Local directories `work/` and `scratch/` are correctly git-ignored in both repositories.
