# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: LAYOUT-01 — Reproduce the source's bars-per-row layout: write the track SystemsLayout from the PDF systems

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/layout-01-source-row-layout`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Write each track's SystemsLayout (bars per row) from the systems read in the source PDF, so Guitar Pro breaks rows where the source does. Promoted from the backlog item added by #731; its measurement: Measured by governance on 2026-09-29 at product main 2e8c00b (worktree at d7eef3f) on this Windows host. The references encode line breaks per track as <SystemsLayout> (bars per row); the writer emits a fixed 3 per row. For Lessons 3-7 the systems found by read_note_durations equal the reference SystemsLayout exactly (23, 29, 14, 34 and 25 rows), and every reference DoubleBar ends a row (0 exceptions), while some rows end without one. Write SystemsLayout (and SystemsDefautLayout) from the source systems, or fall back to a documented default with a located diagnostic when systems are unknown; extend the independent comparator to compare it; assert equality for Lessons 3-7. Maintainer request 2026-09-29: reproduce the original format.

## Allowed paths

- `src/score2gp/pdf.py`
- `src/score2gp/pdf_*.py`
- `src/score2gp/notation_omr/**`
- `src/score2gp/ir.py`
- `src/score2gp/tabraw.py`
- `src/score2gp/build_ir.py`
- `src/score2gp/gpif.py`
- `src/score2gp/gp_package.py`
- `src/score2gp/version_adapter.py`
- `src/score2gp/cli.py`
- `schemas/**`
- `tests/test_dur_02_oracle.py`
- `docs/design/**`
- `tests/test_layout_01_*.py`
- `tests/fixtures/pdf/layout_01/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
