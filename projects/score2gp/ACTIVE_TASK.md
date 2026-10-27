# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-03-FU4 — pdf_text_labels: split attach_pdf_text_labels, name the thresholds, move the late import to module level

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-03-fu4-split-attach-pdf-text-labels`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

pdf_text_labels: split attach_pdf_text_labels, name the thresholds, move the late import to module level. Source: authority item OMIT-03-FU4. Non-blocking follow-up 4 from tticomgov-code's approving re-review 5365611424 of tticom/score2gp#473 (OMIT-03) at 51f8f05. Suspected smell only: attach_pdf_text_labels is one function of about 90 lines with nested branches and inline thresholds (5 spaces, 2 pt margin, 1 pt boundary, 7/15/16 pt sizes), cli.py imports pdf_text_labels inside convert_command, and a test imports the private _classify. Split into classify, locate-bar and choose-beat steps, name the thresholds, and keep the written GP byte-identical.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
