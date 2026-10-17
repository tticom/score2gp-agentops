# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: HOPO-01 — Hammer-on/pull-off pairing requires the marker to lie between the two notes

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/hopo-01-betweenness`

**Pull Request**: 499

**Owner Role**: implementation

## Objective

The within-bar HOPO pairing ranks note pairs by midpoint distance without requiring the marker to lie between them, so a genuine cross-bar HOPO whose marker is keyed to the destination bar attaches silently to that bar's first pair (review thread N1 on product #467, `src/score2gp/build_ir.py` around the intra-bar loop). Require betweenness, add the backward cross-bar counterpart, and refuse with a located reason when ambiguous.

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
