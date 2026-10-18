# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-02-FU4 — Remove the pytest-dependent GPIF layout switch in gpif.build_gpif

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-02-fu4-remove-pytest-layout-switch`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

`build_gpif` writes a legacy hierarchical GPIF whenever `pytest` is in `sys.modules` or in any argv, including output paths, instead of the production relational GP8 GPIF. Tests therefore exercise a different writer from the product, and one OMIT-02 private test passed locally and failed only in CI. Replace the switch with an explicit writer option, migrate the legacy tests to opt in explicitly, and assert the production layout in every CLI acceptance test.

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
