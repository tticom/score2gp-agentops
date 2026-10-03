# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: SCALE-01 — Make the staff and barline detection constants relative to the staff space (Melodic Soloing Masterclass reads no notation bars)

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/scale-01-scale-relative-constants`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Replace the absolute-point limits in staff and symbol detection (find_staves step cap, extract_page_symbols rectangle thickness, and any others found by measurement) by limits derived from the measured staff space, so large-scale pages find their staves and barlines, and write the bars that then pair unambiguously with their TAB digits. Normal pages must be byte-identical; anything ambiguous stays refused with a located reason.

## Allowed paths

- `src/score2gp/notation_omr/**`
- `src/score2gp/pdf_*.py`
- `docs/design/**`
- `tests/test_dur_02_oracle.py`
- `tests/test_note_duration*.py`
- `tests/test_npg03b_floating.py`
- `tests/test_pdf*.py`
- `tests/test_scale_01_*.py`
- `tests/fixtures/pdf/scale_01/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
