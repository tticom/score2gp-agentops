# Active Task

**Task**: Task 94 — Dual-Modality Visual TAB Digit OMR (CRP-06)
**Status**: PROMOTED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/crp-06-dual-modality-tab-recognition`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0049-source-modality-tab-recognition.md`

## Context

Task 93 (CRP-05) evaluated sidecar OMR options on `src/score2gp/notation_omr/timeline.py` using `Lesson-6.pdf` 4/4 triplets as the mandatory discriminator and selected Outcome A (internal topology-first timing adapter).
Task 94 (CRP-06) is the sixth stage of the Conversion Recovery Programme. It implements visual TAB digit recognition for LilyPond/Sibelius vector bezier paths and embedded text candidates (`0-24`) in `src/score2gp/pdf.py`, preventing adjacent fret digit over-merging (> 24) while distinguishing fret numbers from string labels or fingering digits.

## Goal

Implement `tests/test_tab_digit_recognition.py` and refine TAB candidate text merging in `src/score2gp/pdf.py` to prevent adjacent single-digit frets (e.g. `7` and `10`) from merging into impossible guitar frets (> 24) and classify fret candidates accurately.

## Allowed Files

- `src/score2gp/pdf.py`
- `tests/test_tab_digit_recognition.py`

## Non-goals

- Do not hardcode fret limits without bounds checking against valid guitar fretboard ranges (0-24).
- Do not pass reference `.gp` files to the TAB candidate extractor.
- Do not introduce fixture-specific coordinate bounds or hash checks.

## Acceptance

- `pytest tests/test_tab_digit_recognition.py` passes cleanly and verifies fret candidate classification bounds (0-24).
- `python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf` extracts separate fret candidates for adjacent digits.
- `python3 scripts/agent_verify.py` passes with zero regression.
