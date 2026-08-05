# Active Task

**Task**: CR-07C: Span-Based Embellishment Attachments for Palm Mute & Let Ring
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr07c-span-based-embellishment-attachments`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0035-cr07c-span-based-embellishment-attachments.md`

## Context

Developer slice `CR-07B` completed and merged via PR #407 (`198adc09b836d998945a946c9e8ecc7e6829e644`). The project now promotes Developer slice `CR-07C` to attach span-based embellishments (palm muting "P.M." and let ring "let ring") across note/chord ranges using onset-to-end-event ID ranges in ScoreIR and GPIF.

## Goal

Implement span-based embellishment attachment logic (`PalmMuteTechnique`, `LetRingTechnique`) in `src/score2gp/tabraw.py` and `src/score2gp/build_ir.py`. Attach text/drawing span candidates to ScoreIR note ranges using explicit event ID spans rather than global text scopes.

## Allowed Files

- `src/score2gp/tabraw.py`
- `src/score2gp/build_ir.py`
- `tests/test_cr07_embellishment_attachments.py`

## Non-goals

- Audio/OMR pitch resolution changes and non-span embellishments are deferred to subsequent tasks.

## Acceptance

Pass validation commands (`pytest tests/test_cr07_embellishment_attachments.py` and `python scripts/agent_verify.py`). Publish one Developer pull request on branch `agy/cr07c-span-based-embellishment-attachments` in `tticom/score2gp` for independent Codex review.
