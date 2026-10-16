# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: DUR-02-FU5 — Can't Find My Way Home: fix or locate the technique differences in written bars (HOPO origin/destination, slide)

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/dur-02-fu5-cfw-technique-differences`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

In the written bars of Can't Find My Way Home the independent comparator reported 4 HOPO origin, 4 HOPO destination and 1 slide difference against the reference `.gp` (2026-09-28 at OMIT-01 round 3, since then DUR-03, UNREAD-01/02 and others have landed). Re-measure, diagnose each remaining difference against the source and reference, fix the cause or locate it, and add a regression per distinct cause.

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
