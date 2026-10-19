# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-05-FU2 — Remove the 'Compiled Score' placeholder title in scoreir_compiler.py

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-05-fu2-remove-compiled-score-title`

**Pull Request**: 502

**Owner Role**: implementation

## Objective

`src/score2gp/scoreir_compiler.py` invents `title='Compiled Score'` on a route outside OMIT-05's paths. Apply the source-or-refuse rule: read the title from the source, or leave it empty with a located diagnostic. A commercial product must not stamp an invented title on a user's file.

## Allowed paths

- `src/score2gp/**`
- `tests/**`
- `docs/**`
- `schemas/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
