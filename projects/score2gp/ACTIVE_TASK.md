# Active Task

**Task**: Task 91 — Page-Continuous Measure Indexing & Offsets (CRP-03)
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/crp-03-page-continuous-measure-indexing`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0046-m6-prevent-digit-over-merging.md`

## Context

Task 90 (CRP-02) topologically locked notation and TAB staves system-by-system in `src/score2gp/pdf.py`.
Task 91 (CRP-03) is the third stage of the Conversion Recovery Programme. It passes `running_bar_index` across multi-page boundaries in `_extract_pdf_text_candidates` to prevent measure index reset on Page 2 and calculates cumulative page height coordinate offsets.

## Goal

Enable sequential measure tracking across page boundaries and compute cumulative page height coordinate offsets in `src/score2gp/pdf.py` to prevent page-boundary index conflicts and coordinate collisions.

## Allowed Files

- `src/score2gp/pdf.py`
- `tests/test_pdf.py`

## Non-goals

- Do not modify higher-level timeline, measure assembly, or IR compilation modules.
- Do not re-introduce 300pt outer tolerance or duration scaling hacks.
- Do not calibrate rules to target fixture coordinates or file hashes.

## Acceptance

- `pytest tests/test_pdf.py` passes cleanly.
- `python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf` outputs sequentially incrementing measure indices across multi-page boundaries.
- `python3 scripts/agent_verify.py` passes with zero regression.


