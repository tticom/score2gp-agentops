# Active Task

**Task**: CR-07B: Proximity & String-Identity Note Attachment for Visual Vibrato and Slide Evidence
**Status**: PROMOTED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr07b-vibrato-and-slide-note-attachment`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0034-cr07b-vibrato-and-slide-note-attachment.md`

## Context

Developer slice `CR-07A` completed and merged via PR #406 (`bc079a708994778edfeb1e05dd1f58587f59952a`). The project now promotes Developer slice `CR-07B` to attach extracted `VisualVibratoEvidence` and `VisualSlideEvidence` candidates to ScoreIR note techniques (`VibratoTechnique`, `SlideTechnique`) and GPIF representations using horizontal proximity and string identity invariants.

## Goal

Implement visual vibrato and slide attachment logic in `src/score2gp/tabraw.py` and `src/score2gp/build_ir.py`. Connect visual vibrato candidates to target notes/chords and visual slide candidates to target notes sharing the same string identity (or adjacent coordinates for position shifts).

## Allowed Files

- `src/score2gp/tabraw.py`
- `src/score2gp/build_ir.py`
- `tests/test_cr07_embellishment_attachments.py`

## Non-goals

- Span-based embellishments (palm muting, let ring) and audio/OMR pitch resolution changes are deferred to subsequent tasks.

## Acceptance

Pass validation commands (`pytest tests/test_cr07_embellishment_attachments.py` and `python scripts/agent_verify.py`). Publish one Developer pull request on branch `agy/cr07b-vibrato-and-slide-note-attachment` in `tticom/score2gp` for independent Codex review.
