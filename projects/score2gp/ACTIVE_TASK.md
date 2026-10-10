# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: PDF-GROUP-03 — Songbook transcriptions refused at bar-box construction

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/pdf-group-03-song-bar-boxes`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Find why nine with-score sources refuse at layout gating with pdf_bar_box_construction_not_enough_for_build_ir (Back In Black, Black Dog, Brown Sugar, Castles Made of Sand, Crossroads, Ex 2 Hands Up, Heartbreaker, Hey Joe, Pride and Joy), where the barline detector discards most candidate strokes as too short, not crossing the staff, outside the system and similar. Investigate first (read the PDF-GROUP-01 close-out); build bar boxes only by a staff-relative rule that keeps true barlines and rejects stems and other vertical strokes, otherwise stop with the measured finding. Ex 2 Hands Up has a reference .gp and is the measurable target. Evidence: the 2026-10-08 fixture survey and diagnosis.

## Allowed paths

- `src/score2gp/pdf.py`
- `src/score2gp/pdf_geometry.py`
- `src/score2gp/pdf_staff_detection.py`
- `src/score2gp/pdf_tab_system_partition.py`
- `src/score2gp/pdf_tab_bar_assembler.py`
- `tests/test_dur_02_oracle.py`
- `tests/test_pdf*.py`
- `tests/test_pdf_group_03_*.py`
- `tests/fixtures/pdf/pdf_group_03/**`
- `docs/design/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
