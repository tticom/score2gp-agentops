# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: DUR-04 — Settle the remaining bars whose durations do not total the meter

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/dur-04-remaining-bar-total-mismatches`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

After REFUSE-05 and TABRHY-01 the whole-set ranking holds bar_total_mismatch at 6 bars (reader gap) and tie_head_ownership_unconfirmed at 1. The total is the check, never the evidence. Leads, not facts: re-measure, say per bar whether a printed symbol (dot, rest, tuplet, tie) is unread, and view the page.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
