# Active Task

**Task**: Task 102 — Port and Harmonize Barline Detection & Geometry Cleanup (CRP-01)
**Status**: MERGED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/crp-01-barline-detection-harmonization`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0044-m6-port-and-harmonize-barline-detection.md`

## Context

Task 101 completed the architecture review and migration mapping. CRP-01 is the first unblocked implementation task on the migration map.

## Goal

Port valid barline detection thresholds from PR 418 into `src/score2gp/pdf.py`, revert the `outer_tolerance = 300.0` geometry snapping hack, and enforce staff-relative barline height bounds without mutating higher-level layout models.

## Allowed Files

- `src/score2gp/pdf.py`
- `src/score2gp/pdf_staff_notation_diagnostics.py`
- `tests/test_pdf_geometry_candidate_extractor.py`
- `tests/test_pdf.py`

## Non-goals

- Do not implement page-continuous measure indexing (handled in CRP-03).
- Do not lock 5-line notation barlines to 6-line TAB barlines (handled in CRP-02).

## Acceptance

- `pytest tests/test_pdf_geometry_candidate_extractor.py` and `pytest tests/test_pdf.py` pass cleanly.
- `python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf` increases extracted notation bar boxes on `Lesson-5.pdf` from 31 (on main) to 41 across 12 systems without triggering 300pt snapping hacks.
- Held-out real-source probe on `fixtures/private/Lesson-6.pdf` increases extracted notation bar boxes from 13 (on main) to 40 across 10 systems without snapping hacks.
- `python3 scripts/agent_verify.py` passes with zero regression.
