# Active Task

**Task**: PDFTAB-DUR-07: Regression Audit & System Hardening
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer / Pipeline Integrator
**Repository**: tticom/score2gp
**PR Branch**: `agy/pdftab-duration-regression-audit`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0024-pdf-tab-duration-regression-audit.md`

## Context

Following the merge of PR #395 (`326fc4baa6d339f7eb73d72d4f6caf0379dcf9df`), Slice 3 (Assembler Integration & Oracle Verification) is fully merged in `score2gp`. This task implements Slice 4 (Regression Audit & System Hardening) as defined in Section 7 of `docs/design/pdf-tab-duration-candidate-extraction.md`.

## Goal

Perform comprehensive regression audit across the full corpus harness, verifying unstemmed tab staves, standard notation, and IR validation.
Add regression test suite in `tests/test_pdf_tab_duration_regression_audit.py` to ensure end-to-end conversion consistency and zero leakage.
Verify that `export-schema`, `artifact_audit.py`, `validate-ir`, and `agent_verify.py` pass cleanly with zero warnings or uncommitted diffs.

## Allowed Files

- `tests/test_pdf_tab_duration_regression_audit.py` (in `score2gp`)

## Non-goals

No edits to unrelated parsers, private inputs, reference GP leakage, automatic merge, or branch deletion.

## Acceptance

Regression audit tests in `tests/test_pdf_tab_duration_regression_audit.py` pass 100%. All public fixture conversions, schema exports, IR validations, and artifact audits pass cleanly. `agent_verify.py` passes with overall status `PASS`, product PR is opened, and handback comment is published.
