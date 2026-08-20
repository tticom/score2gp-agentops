# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: NPG-03B — Floating Barline Geometry Isolation

**Status**: PENDING

**Repository**: tticom/score2gp

**PR Branch**: `feat/npg-03b-floating-barline`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Implement floating barline geometry isolation as defined in the NPG-00R ADR.

## Allowed paths

- `src/score2gp/pdf_geometry.py`
- `src/score2gp/pdf_tab_bar_assembler.py`

## Validation commands

- `.venv/bin/python -m pytest tests/test_pdf_geometry.py tests/test_pdf_tab_bar_assembler.py`
