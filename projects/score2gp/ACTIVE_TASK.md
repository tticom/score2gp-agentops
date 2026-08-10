# Active Task

**Task**: Task 96 — Recognition Adapter Seam (CRP-08)
**Status**: MERGED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/crp-08-recognition-adapter-seam`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0051-recognition-adapter-seam.md`

## Context

Task 95 (CRP-07) implemented document topology data structures and barline classification invariants in `src/score2gp/notation_omr/staff_geometry.py`.
Task 96 (CRP-08) is the eighth stage of the Conversion Recovery Programme. It implements typed candidate adapters and evidence records (`CandidateAdapter`, `EvidenceRecord`, `SourceModality`) in `src/score2gp/notation_omr/evidence.py` that retain source coordinates, modality, confidence, absence, ambiguity, and conflict behind a single interface without assigning downstream musical semantics.

## Goal

Implement `tests/test_recognition_adapters.py` and refine `src/score2gp/notation_omr/evidence.py` to wrap text, vector, and raster candidates in typed evidence adapters with source coordinate retention, modality tracking, and ambiguity flag handling.

## Allowed Files

- `src/score2gp/notation_omr/evidence.py`
- `tests/test_recognition_adapters.py`

## Non-goals

- Do not assign downstream musical timing or duration semantics inside the evidence adapters.
- Do not pass reference `.gp` files to the evidence adapters.
- Do not introduce fixture-specific coordinate bounds or hash checks.

## Acceptance

- `pytest tests/test_recognition_adapters.py` passes cleanly and verifies candidate adapter wrapping, modality retention, and source coordinate preservation.
- `python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf` preserves typed candidate evidence.
- `python3 scripts/agent_verify.py` passes with zero regression.
