# Active Task

**Task**: CR-06: Key-Signature Semantics Architecture
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr06-key-signature-semantics-architecture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0030-cr06-key-signature-semantics-architecture.md`

## Context

Task `MXS-10` (Assisted Sidecar Ingestion Manifest) completed and merged via product PR #412 (`b49e37a17c66f442a809e5d2dd6e5f0e733e89fb`). The project now promotes task `CR-06` to architect key-signature semantics.

## Goal

Determine a generic, testable architecture in `tticom/score2gp` for key-signature evidence detection on notation staves.
The architecture must distinguish explicit sharp/flat key-signature glyph evidence from the absence of key-signature evidence. It must never emit C-major / A-minor (0 accidentals) as a "recognized key signature" when evidence is absent or ambiguous, and must never manufacture accidentals or alter pitch assignments from unknown key signature evidence.

## Allowed Files

- `src/score2gp/pdf.py`
- `src/score2gp/pdf_staff_geometry.py`
- `src/score2gp/whole_note_recogniser.py`
- `src/score2gp/gpif.py`
- `src/score2gp/cli.py`
- `docs/design/cr06-key-signature-semantics-architecture.md`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- Product source code implementation is not authorized. Do not modify product source code in `score2gp`.

## Acceptance

Write `docs/design/cr06-key-signature-semantics-architecture.md` in `tticom/score2gp`. Choose exactly one outcome (`CONTINUE`, `RESEARCH_NEXT`, or `STOP`). Stop after publishing one product architecture PR in `tticom/score2gp` for independent Codex review.
