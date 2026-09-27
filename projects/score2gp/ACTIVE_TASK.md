# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: DUR-02 — Convert with note-type durations; delete the count rule

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/dur-02-convert-with-note-type-durations`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

The PDF conversion route takes every duration from DUR-01's note-type reader and positions from the TAB; the count-based fallback, the equal_spacing_fallback quarter, the editable-draft quarter default and the remainder rest padding are deleted; the first real-source GP (Lesson 3) with real rhythm is produced for the maintainer to test in Guitar Pro.

## Allowed paths

- `src/score2gp/pdf_tab_measure_timing.py`
- `src/score2gp/pdf_tab_bar_assembler.py`
- `src/score2gp/pdf_tab_event_factory.py`
- `src/score2gp/build_ir.py`
- `src/score2gp/cli.py`
- `src/score2gp/ir.py`
- `src/score2gp/notation_omr/**`
- `src/score2gp/note_duration*.py`
- `tests/test_cli_convert.py`
- `tests/test_pdf_only_tab*.py`
- `tests/test_pdf_tab_*.py`
- `tests/test_dur_02_*.py`
- `docs/design/pdf-tab-duration-candidate-extraction.md`
- `docs/musicxml-tabraw-build-ir.md`
- `docs/architecture.md`
- `schemas/**`
- `src/score2gp/pdf_tab_duration_associator.py`
- `src/score2gp/pdf_tab_duration_types.py`
- `src/score2gp/tabraw.py`
- `src/score2gp/pdf.py`
- `src/score2gp/pdf_geometry_candidate_extraction.py`
- `tests/test_pdf_tab_duration_associator.py`
- `tests/test_tabraw_duration_metadata.py`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
