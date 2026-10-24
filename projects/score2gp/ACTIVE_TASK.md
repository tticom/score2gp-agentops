# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-04-FU5 — G-Am-C-Lick.pdf: write the refused bars as printed, or refuse them with a located reason; find every printed percussive strike

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-04-fu5-g-am-c-lick-refused-bars`

**Pull Request**: 511

**Owner Role**: implementation

## Objective

OMIT-04-FU1 left G-Am-C-Lick.pdf at 4 of 9 bars written. The maintainer reports most of the score is missing and not all percussive strikes were found. Find each root cause for the five refused bars (bars 2 and 6: 2 notation heads against 1 TAB candidate; bar 8: unread rest or multi-head X form beside a note) and write the bar from the PDF's printed notation and TAB, or refuse it with a located reason; no reference .gp exists and none may be invented.

## Allowed paths

- `tests/**`
- `src/score2gp/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
