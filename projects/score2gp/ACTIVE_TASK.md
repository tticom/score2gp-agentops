# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-05-FU1 — Header and footer templates: reproduce Guitar Pro's default rich-text font sizes as project-owned policy

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-05-fu1-header-footer-font-sizes`

**Pull Request**: 506

**Owner Role**: implementation

## Objective

The minimal header/footer template markup drops Guitar Pro's default rich-text font sizes (for example the 35 pt title), a visible difference in Guitar Pro. Reproduce the default sizes as documented project-owned policy constants with provenance (never read from a reference file during conversion), and extend the oracle to compare them.

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
