# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-01 — Classify the thin flat band symbols that leave bars refused as note_duration_event_unread

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-01-classify-thin-flat-band-symbols`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Classify the thin flat band symbols that leave bars refused as note_duration_event_unread. Source: authority item REFUSE-01. Measured 2026-10-27 on the latest survey: across 9 partly refused PDFs, 799 symbols were unclassified (symbol_unclassified) and 751 of them share one shape (constant-thickness band, about 3.9 by 0.7 staff spaces, drawn). Measure first what they are on real approved sources, then classify or explicitly refuse them with a located reason. Goal: fewer refused bars with no false success. Acceptance must use real approved sources, not synthetic ones.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
