# Active Task

**Task**: Task 90 — Topologically Locked System Barlines (CRP-02)
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/crp-02-topologically-locked-system-barlines`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0045-m6-implement-page-coordinate-offsets.md`

## Context

Task 89 (CRP-01) ported valid barline detection thresholds (20pt internal bar width and staff-relative min height) into `src/score2gp/pdf.py`.
Task 90 (CRP-02) is the second stage of the Conversion Recovery Programme. It locks notation staff and TAB staff barlines system-by-system before event extraction, closing the remaining 2-bar gap (41 -> 43 bars on `Lesson-5.pdf`) and ensuring system barlines do not bleed across system or page boundaries.

## Goal

Topologically lock 5-line notation barlines to 6-line TAB barlines system-by-system in `src/score2gp/pdf.py` before event extraction, establishing precise system boundary alignment.

## Allowed Files

- `src/score2gp/pdf.py`
- `tests/test_pdf_geometry_candidate_extractor.py`
- `tests/test_pdf.py`

## Non-goals

- Do not modify higher-level timeline, measure assembly, or IR compilation modules.
- Do not re-introduce 300pt outer tolerance or duration scaling hacks.
- Do not calibrate rules to target fixture coordinates or file hashes.

## Acceptance

- `pytest tests/test_pdf_geometry_candidate_extractor.py` and `pytest tests/test_pdf.py` pass cleanly.
- `python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf` extracts all 43 notation barlines across 12 systems on `Lesson-5.pdf` without triggering 300pt snapping hacks.
- `python3 scripts/agent_verify.py` passes with zero regression.

