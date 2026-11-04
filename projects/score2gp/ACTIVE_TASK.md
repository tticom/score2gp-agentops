# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-11 — Read the largest remaining reader-gap refusal class after REFUSE-10

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-11-largest-remaining-refusal-class`

**Pull Request**: 545

**Owner Role**: implementation

## Objective

REFUSE-07 to REFUSE-10 each read one measured class of refused bars. Re-run the whole-set measurement on the current runtime (after REFUSE-08, -09 and -10) and rank every remaining refusal code by bar count over all approved PDFs. Take the single largest class that is a reader gap and whose symbols are unambiguously musical, and read it only where the drawn notation settles it. Leads, not facts: do not trust older rankings.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
