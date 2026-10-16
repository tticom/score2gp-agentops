# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OUT-01 — Contain fabricated GP6/GP8 output: --target accepts only evidence-backed targets

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/out-01-contain-fabricated-targets`

**Pull Request**: 493

**Owner Role**: implementation

## Objective

`version_adapter.py` can emit a file presented as GP6 or GP8 that is not one (invented tags, a ZIP called GP6, an unknown target silently becoming GP7). A commercial product must not ship mislabelled files. Make `--target` accept only the evidence-backed target (the current GPIF-ZIP output) and refuse the others with a located error.

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
