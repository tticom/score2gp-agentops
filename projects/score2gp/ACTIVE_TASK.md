# Active Task

**Task**: CR-07A: Bounded Visual Vibrato and Slide Glyphs Evidence Seam
**Status**: PROMOTED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr07a-bounded-visual-vibrato-and-slide-glyphs-evidence-seam`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0033-cr07a-bounded-visual-vibrato-and-slide-glyphs-evidence-seam.md`

## Context

Architecture task `CR-07` completed and merged via PR #405 (`f2419056a628af063e8a19ee1df47087a5f28971`). The project now promotes Developer slice `CR-07A` to introduce `VisualVibratoEvidence` and `VisualSlideEvidence` candidate extraction models and visual drawing path parsing in `src/score2gp/pdf_geometry.py` and `src/score2gp/pdf.py`.

## Goal

Introduce `VisualVibratoEvidence` and `VisualSlideEvidence` candidate extraction models in `src/score2gp/pdf_geometry.py` and visual drawing path parsing in `src/score2gp/pdf.py` to capture raw embellishment drawing evidence from vector PDF path primitives (`"c"` bezier curves, line segments) before note assignment and pitch resolution.

## Allowed Files

- `src/score2gp/pdf_geometry.py`
- `src/score2gp/pdf.py`
- `tests/test_cr07_embellishment_attachments.py`

## Non-goals

- Downstream compiler/ScoreIR/GPIF embellishment note assignment changes are deferred to subsequent task slices.
- Audio/OMR pitch resolution changes are deferred.

## Acceptance

Pass validation commands (`pytest tests/test_cr07_embellishment_attachments.py` and `python scripts/agent_verify.py`). Publish one Developer pull request on branch `agy/cr07a-bounded-visual-vibrato-and-slide-glyphs-evidence-seam` in `tticom/score2gp` for independent Codex review.
