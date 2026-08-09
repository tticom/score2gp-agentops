# Active Task

**Task**: Task 89 — Port and Harmonize Barline Detection & Geometry Cleanup (CRP-01)
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/crp-01-barline-detection-harmonization`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0044-m6-port-and-harmonize-barline-detection.md`

## Context

Task 88 established the governing conversion recovery architecture, real-source testing rules, and 16-task migration map (`CRP-00` to `CRP-15`). Task 89 (`CRP-01`) is the first unblocked downstream implementation task.

## Goal

Port valid barline detection thresholds from PR 418 into `src/score2gp/pdf.py`, revert the `outer_tolerance = 300.0` geometry snapping hack, and enforce staff-relative barline height bounds without mutating higher-level layout models.

## Allowed Files

- `src/score2gp/pdf.py`
- `src/score2gp/pdf_staff_notation_diagnostics.py`
- `tests/test_pdf_geometry_candidate_extractor.py`
- `tests/test_pdf.py`

## Non-goals

- Do not modify higher-level timeline, measure assembly, or IR compilation modules.
- Do not re-introduce 300pt outer tolerance or duration scaling hacks.
- Do not calibrate rules to target fixture coordinates or file hashes.

## Acceptance

- `pytest tests/test_pdf_geometry_candidate_extractor.py` and `pytest tests/test_pdf.py` pass cleanly.
- `python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf` increases extracted notation bar boxes on `Lesson-5.pdf` from 31 to 41 across 12 systems without triggering 300pt snapping hacks (with full 43-measure multi-page grouping completed downstream in CRP-02/03).
- `python3 scripts/agent_verify.py` passes with zero regression.
