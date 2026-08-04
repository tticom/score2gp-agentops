# Active Task

**Task**: CR-05A: PDF-Tab Barline Style Classification Seam
**Status**: PROMOTED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr05a-pdf-tab-barline-style-classification`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0027-cr05a-pdf-tab-barline-style-classification.md`

## Context

Architecture task `CR-05` completed and merged via PR #397 (`5268844e1c5596b3c3db1e5c821e93064a7417c1`). The project now promotes Developer slice `CR-05A` to implement typed barline style classification (`"regular"`, `"double"`, `"final"`, `"ambiguous"`, `"unclassified_stroke"`) on the PDF-tab conversion seam while preserving 100% backward compatibility.

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

## Acceptance

Pass validation commands (`pytest tests/test_cr05_barline_style_classification.py` and `python scripts/agent_verify.py`). Publish one Developer pull request on branch `agy/cr05a-pdf-tab-barline-style-classification` in `tticom/score2gp` for independent Codex review.
