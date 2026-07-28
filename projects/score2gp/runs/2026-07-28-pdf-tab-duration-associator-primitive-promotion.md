# Governance Record: PDFTAB-DUR-04 Task Promotion

**Task**: PDFTAB-DUR-04: PDF-Tab Duration Types & Spatial Associator Primitive
**Status**: AWAITING_EXTERNAL_REVIEW
**Author**: tticom-codex
**Repository**: tticom/score2gp-agentops
**Branch**: `codex/promote-pdf-tab-duration-associator-primitive`

## Summary

Following the merge of architecture PR #392 (`44ab38ca0ad8e0460469360f7ab3e9db29f98aa8`), this governance PR promotes Task PDFTAB-DUR-04, implementing Slice 1 of the durable architecture specification `docs/design/pdf-tab-duration-candidate-extraction.md`.

## Target Scope

- Authorized Repository: `tticom/score2gp`
- Authorized Branch: `agy/pdftab-duration-associator-primitive`
- Allowed Product Files:
  - `src/score2gp/pdf_tab_duration_types.py`
  - `src/score2gp/pdf_tab_duration_associator.py`
  - `tests/test_pdf_tab_duration_associator.py`

## Non-goals

No edits to existing assemblers, TabRaw models, private inputs, reference GP leakage, automatic merge, or premature pipeline integration.
