# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: CFW-04 — Read grace notes, small stemless heads and wave glyphs, so more of Can't Find My Way Home is written

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/cfw-04-grace-small-heads`

**Pull Request**: 476

**Owner Role**: implementation

## Objective

Read grace notes (small flagged heads), stemless small heads and non-note wave glyphs from the source, write the grace the way the reference does (GraceNotes OnBeat) and write the bars they unblock. The diagnosis expects Can't Find My Way Home to go from 9 to 18 of 21 bars written with none paired wrongly; whatever cannot be read unambiguously (tied chords, a dead-note head) stays refused with a located reason.

## Allowed paths

- `src/score2gp/notation_omr/**`
- `src/score2gp/pdf_*.py`
- `src/score2gp/ir.py`
- `src/score2gp/build_ir.py`
- `src/score2gp/gpif.py`
- `src/score2gp/gp_package.py`
- `schemas/**`
- `docs/design/**`
- `tests/test_dur_02_oracle.py`
- `tests/test_note_duration*.py`
- `tests/test_pdf*.py`
- `tests/test_cfw_04_*.py`
- `tests/test_omit_04_private.py`
- `tests/fixtures/pdf/cfw_04/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
