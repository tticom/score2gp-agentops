# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: MEM-01-FU2 — gp_package.py: stamp GP-imported ScoreIR and ScoreBooklet with SCHEMA_VERSION

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/mem-01-fu2-gp-package-schema-version`

**Pull Request**: 518

**Owner Role**: implementation

## Objective

gp_package.py: stamp GP-imported ScoreIR and ScoreBooklet with SCHEMA_VERSION. Source: authority item MEM-01-FU2. Non-blocking follow-up 2 from tticomgov-code's approving review of tticom/score2gp#472 (MEM-01) at caf71f3. src/score2gp/gp_package.py builds GP-imported ScoreIR/ScoreBooklet at three sites with schema_version="0.1.0" while ir.SCHEMA_VERSION is now 0.1.1. Valid, because those objects carry no TabRaw provenance, but inconsistent. Use the constant and add a test; the small memory saving (about 2-4% peak working set) is covered by MEM-02 and MEM-03, not by this item.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
