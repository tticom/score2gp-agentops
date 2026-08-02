# Active Task

**Task**: CR-05A: PDF-Tab Barline Style Classification Seam
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr05a-pdf-tab-barline-style-classification`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0027-cr05a-pdf-tab-barline-style-classification.md`

## Context

PR #397 (`agy/cr05-structural-layout-and-titles-architecture`) on `tticom/score2gp` was merged into product `main`, establishing the decoupled layout and titles data models and authorizing Developer implementation slice `CR-05A` on the PDF-tab conversion seam.

## Goal

Classify PDF-tab barline candidate details into explicit, typed barline styles (`"regular"`, `"double"`, `"final"`, `"ambiguous"`, `"unclassified_stroke"`) while preserving 100% backward-compatible float `valid_barlines` arrays, `_TabSystem.barlines`, and system layout bounds.

## Allowed Files

- `src/score2gp/pdf_geometry.py`
- `src/score2gp/pdf.py`
- `src/score2gp/report.py`
- `tests/test_cr05_barline_style_classification.py`

## Non-goals

- No title classification or title ownership code changes in `CR-05A`.
- No system layout break refactoring in `CR-05A`.
- No changes to product `build_ir.py` conversion logic in `CR-05A`.
- Final-barline (thick-thin) classification is deferred until vector stroke-width oracle evidence is added.
- No editing of `docs/design/cr05-structural-layout-and-titles-architecture.md` during this Developer slice.

## Acceptance

Pass validation suite (`pytest tests/test_pdf.py::test_double_barline_ambiguity_resolution`, `pytest tests/test_cr05_barline_style_classification.py`, and `python scripts/agent_verify.py`). Publish one Developer pull request on branch `agy/cr05a-pdf-tab-barline-style-classification` in `tticom/score2gp` for independent Codex review.
