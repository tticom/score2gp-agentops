# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: UNREAD-02 — Dead-note X heads become TAB X events, with a candidate and routing contract

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/unread-02-dead-note-x-events`

**Pull Request**: 488

**Owner Role**: implementation

## Objective

UNREAD-01 (stopped at its scope gate, then limited to located refusals by the maintainer on 2026-10-10) leaves standard dead-note X heads as located dead_note_x_head refusals. G-Am-C-Lick has four cross-shaped heads (1.16 x 1.0 staff spaces) whose stems carry secondary beams that no recognised head owns, so the bars holding them stay refused. Writing them faithfully needs a TAB X candidate kind and routing: build_ir.py:1772 keeps only numeric-fret candidates (plus the legacy rest token), line 1801 passes only those to the assembler, and tabraw.py:107 parses only digits. The IR (NoteEvent.is_dead) and GPIF (dead-note technique) already carry a dead note. Add the candidate and routing contract so an X on a string is read from the TAB, associated with its duration like a digit and written as a dead note, without changing what any numeric-fret file produces. Maintainer: 'widen the scope to fit in 1 as a or part of the next task' (2026-10-10).

## Allowed paths

- `src/score2gp/build_ir.py`
- `src/score2gp/tabraw.py`
- `src/score2gp/pdf.py`
- `src/score2gp/pdf_tab_bar_assembler.py`
- `src/score2gp/pdf_tab_event_factory.py`
- `src/score2gp/pdf_tab_duration_associator.py`
- `src/score2gp/pdf_tab_duration_types.py`
- `src/score2gp/notation_omr/**`
- `tests/test_dur_02_oracle.py`
- `tests/test_unread_02_*.py`
- `tests/fixtures/pdf/unread_02/**`
- `src/score2gp/ir.py`
- `src/score2gp/gpif.py`
- `schemas/scoreir.v0.1.schema.json`
- `src/score2gp/black_key_spelling.py`
- `src/score2gp/gp_package.py`
- `tests/test_unread_01_dead_heads.py`
- `tests/test_unread_01_mutants.py`
- `tests/test_unread_01_font_glyphs.py`
- `docs/design/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
