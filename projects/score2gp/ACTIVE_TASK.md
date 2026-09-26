# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: DUR-01 — Read note durations from note types

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/dur-01-note-durations-from-note-types`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Every note and rest carries its own duration, read from its note type (notehead, stem, flag glyphs or beam lines, dots, rest glyphs) and grouping (beams, tuplets, ties): a symbol-cited duration record per event on the notation staff, unread with a located reason when ambiguous, never guessed, validated per event against Lesson-3.gp through the independent oracle.

## Allowed paths

- `src/score2gp/notation_omr/**`
- `src/score2gp/recognition/**`
- `src/score2gp/note_duration*.py`
- `src/score2gp/pdf.py`
- `src/score2gp/cli.py`
- `tests/test_dur_01_*.py`
- `tests/test_notation_omr*.py`
- `tests/fixtures/pdf/dur_01/**`
- `scripts/dur_01_*.py`
- `docs/design/note-duration-recognition.md`
- `docs/architecture.md`
- `schemas/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
