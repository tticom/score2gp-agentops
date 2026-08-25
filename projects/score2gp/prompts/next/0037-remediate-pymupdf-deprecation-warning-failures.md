# 0037 - Remediate PyMuPDF Deprecation Warning Failures

## Objective

Remediate PyMuPDF deprecation warning failures on CI. Newer versions of `PyMuPDF` (v1.24.3+) print a deprecation warning to stdout when importing the legacy `fitz` module name directly:
`warning: The fitz API is deprecated and will be removed in future. Use import pymupdf instead.`

This warning pollutes stdout of subprocess command executions (e.g. CLI subcommands with `--json`), causing JSON parsing errors (such as `json.decoder.JSONDecodeError`) in 38 integration and CLI tests. Update the import statements in product files to use the modern `import pymupdf as fitz` syntax to suppress the warning without affecting existing code references.

## Authorized Product Files

- `src/score2gp/pdf_raster_staff_diagnostics.py`
- `src/score2gp/notation_omr/pipeline.py`
- `src/score2gp/pdf.py`

No other product files in `src/` may be edited in this task.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/next/0037-remediate-pymupdf-deprecation-warning-failures.md`, `PLANNING_DATA.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/fix-pymupdf-deprecation-warning` in `tticom/score2gp`.
6. Run `python scripts/agent_verify.py` in `score2gp` before making code modifications.

## Implementation Scope & Seam Contract

1. **Modify imports in authorized files**:
   - In `src/score2gp/pdf_raster_staff_diagnostics.py`, replace `import fitz` with `import pymupdf as fitz`.
   - In `src/score2gp/notation_omr/pipeline.py`, replace `import fitz` with `import pymupdf as fitz`.
   - In `src/score2gp/pdf.py`, replace all instances of `import fitz` with `import pymupdf as fitz`.

2. **Suppress stdout warning**:
   - Ensure the deprecation warning is no longer printed to stdout when executing CLI commands.

## Validation Commands

1. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_note_candidate_recognition_cli.py`
2. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_note_candidate_recognition_report.py`
3. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_raster_diagnostics_gate_report.py`
4. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_semantic_cli_reporting.py`
5. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_whole_note_recognition_cli.py`
6. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_whole_note_recognition_report.py`
7. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python scripts/agent_verify.py`

## Non-goals

- Do not change any actual pdf parsing, coordinate extraction, or diagnostics logic.
- Do not introduce external dependencies or change standard python import pathways.
