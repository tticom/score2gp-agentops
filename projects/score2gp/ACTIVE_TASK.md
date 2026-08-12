# Active Task

**Task**: Task 100 — Unified ScoreIR / GPIF Compiler Refactor & Binary Assembly Seam (CRP-12)
**Status**: PROMOTED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/crp-12-scoreir-gpif-compiler-refactor`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0055-scoreir-gpif-compiler-refactor.md`

## Context

Task 99 (CRP-11) implemented biomechanical position optimization and fret token ownership in `src/score2gp/notation_omr/position_optimizer.py`.
Task 100 (CRP-12) is the twelfth stage of the Conversion Recovery Programme. It refactors the ScoreIR and GPIF compilation pipeline to compile locked timelines, tuplet durations, and fretboard position assignments into valid `.gp` binary outputs.

## Goal

Implement `tests/test_scoreir_gpif_compiler_refactor.py` and refine `src/score2gp/scoreir_compiler.py` and `src/score2gp/gpif_builder.py` to compile OMR evidence into valid ScoreIR and GPIF structures.

## Allowed Files

- `src/score2gp/scoreir_compiler.py`
- `src/score2gp/gpif_builder.py`
- `tests/test_scoreir_gpif_compiler_refactor.py`

## Non-goals

- Do not introduce synthetic measures or unevidenced note events.
- Do not pass reference `.gp` files to the compiler.
- Do not bypass timing or capacity validation during compilation.

## Acceptance

- `pytest tests/test_scoreir_gpif_compiler_refactor.py` passes cleanly and verifies ScoreIR/GPIF compilation and binary assembly invariants.
- `python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-6.pdf` produces valid `.gp` output binaries.
- `python3 scripts/agent_verify.py` passes with zero regression.
