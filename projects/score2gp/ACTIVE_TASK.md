# Active Task

**Task**: CR-05A: PDF-Tab Barline Style Classification Seam
**Status**: RESOLVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp-agentops
**PR Branch**: `agy/cr05a-pdf-tab-barline-style-classification-v2`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0027-cr05a-pdf-tab-barline-style-classification.md`

## Context

Task `CR-05` (Structural Layout and Titles Architecture) completed and merged via governance PR #480 (`e4830ae94321fa2e3f30ad28b7d056a83e1778f5`). The project now promotes task `CR-05A` from `APPROVED_TASK_QUEUE.md` under the Visual Output Correctness Series to implement bounded barline style classification on the PDF-tab conversion seam.

## Goal

Classify PDF-tab barline candidate details into explicit, typed barline styles (`regular`, `double`, `final`, `ambiguous`, `unclassified_stroke`) while preserving 100% backward-compatible float `valid_barlines` arrays, `_TabSystem.barlines`, and system layout bounds.

## Allowed Files

- `src/score2gp/pdf_geometry.py`
- `src/score2gp/pdf.py`
- `src/score2gp/report.py`
- `tests/test_cr05_barline_style_classification.py`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- No title classification or title ownership code changes in CR-05A.
- No system layout break refactoring in CR-05A.
- No changes to product `build_ir.py` conversion logic in CR-05A.

## Acceptance

Extend `_LineSegment` metadata, populate typed `barline_style` in candidate details, pass `test_cr05_barline_style_classification.py` and `scripts/agent_verify.py`, update `ACTIVE_TASK.md`, and publish one product pull request on branch `agy/cr05a-pdf-tab-barline-style-classification-v2` in `tticom/score2gp` for independent Codex review.
