# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: CFW-03 — Can't Find My Way Home: classify and fix the 84 unplaced attachments; keep the legitimate tied-chord refusals

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/cfw-03-unplaced-attachments`

**Pull Request**: 498

**Owner Role**: implementation

## Objective

The run reports 84 `pdf_only_tab_attachment_bar_unplaced` (54 technique-text and 30 chord-symbol candidates with no system), plus 2 bars refused for `notehead_digit_count_mismatch` (bars 3 and 9: the legitimate tied-chord case, two heads with one printed digit). Classify each unplaced attachment by cause, fix those whose system is determinable from the page, and keep the tied-chord bars refused unless a per-head tie reader can be built from evidence.

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
