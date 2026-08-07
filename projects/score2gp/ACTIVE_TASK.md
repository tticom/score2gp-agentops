# Active Task

**Task**: Remediate PyMuPDF Deprecation Warning Failures
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/fix-pymupdf-deprecation-warning`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0037-remediate-pymupdf-deprecation-warning-failures.md`

## Context

Task `MXS-10` (Assisted Sidecar Ingestion Manifest) completed and merged via product PR #412. However, the server CI is currently failing on 38 tests due to `stdout` pollution by a PyMuPDF `fitz` module deprecation warning. The project now promotes task `0037` to remediate these failures.

## Goal

Update all instances of `import fitz` to `import pymupdf as fitz` in `src/score2gp/` to suppress the deprecation warning on `stdout` and restore CI test health.

## Allowed Files

- `src/score2gp/pdf_raster_staff_diagnostics.py`
- `src/score2gp/notation_omr/pipeline.py`
- `src/score2gp/pdf.py`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- Do not change any actual pdf parsing, coordinate extraction, or diagnostics logic.
- Do not introduce external dependencies or change standard python import pathways.

## Acceptance

Update all `import fitz` statements to `import pymupdf as fitz` in the authorized files, verify that all integration and CLI tests pass locally and on CI, update `ACTIVE_TASK.md`, and publish one product pull request on branch `agy/fix-pymupdf-deprecation-warning` in `tticom/score2gp` for independent Codex review.
