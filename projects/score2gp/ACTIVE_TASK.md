# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: TIEOWN-01 — Read which head of a chord owns a tie

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/tieown-01-per-head-tie-ownership`

**Pull Request**: 552

**Owner Role**: implementation

## Objective

REFUSE-12 deliberately excludes tie.start when it ties one head of a chord to the note before it, because copying would invent ties on other heads. The rest of the class is per-head tie ownership: a chord that is both a tie stop on one head and a tie start (a tied chain), a 6-head chord with 4 digits whose two heads are tie stops from a previous 2-head chord, the mixed_percussive_tie_ownership_unread bars (3), and the tie_stop_without_written_predecessor bars that cascade from them (10 at the last measurement). Leads, not facts: re-measure. Settle ownership from the tie arc's end points against each head's own position, never from counts.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
