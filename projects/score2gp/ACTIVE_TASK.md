# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: BARTOTAL-01 — Bars whose tick total differs from the declared time signature must be refused, not written

**Status**: RESOLVED

**Repository**: tticom/score2gp

**PR Branch**: `feat/bartotal-01-refuse-wrong-total-bars`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

A bar whose summed tick total differs from the declared time signature is refused with a located code and warning, never written as a success (E_Chord_Lick_Chord bars 2, 4, 10 and 12 are written with 4080 or 3960 ticks under 4/4). Investigate first why the check does not fire and whether 4/4 is right for that file; never invent a value; do not change exit-code semantics for files with refused bars unless the investigation shows false success (report it, do not change silently).

## Allowed paths

- `src/score2gp/notation_omr/note_duration.py`
- `src/score2gp/pdf.py`
- `src/score2gp/pdf_*.py`
- `tests/test_note_duration*.py`
- `tests/test_pdf*.py`
- `tests/test_bartotal_01_*.py`
- `tests/fixtures/pdf/bartotal_01/**`
- `docs/design/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
