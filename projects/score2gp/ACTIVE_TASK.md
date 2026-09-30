# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-03 — Text labels: carry printed text onto the beat it annotates

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-03-text-labels`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Carry printed text such as 'Example 1 - [0:13]' onto the beat it annotates, as GPIF `FreeText`. The reference Lesson-3.gp has 12 labels; the output has none. RES-REQ-0005 found 1,318 text candidates dropped silently from PDF-only builds (gap G16).

## Allowed paths

- `src/score2gp/pdf.py`
- `src/score2gp/pdf_*.py`
- `src/score2gp/notation_omr/**`
- `src/score2gp/recognition/**`
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
- `docs/architecture.md`
- `tests/test_omit_03_*.py`
- `tests/fixtures/pdf/omit_03/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
