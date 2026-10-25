# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-03-FU1 — OMIT-03 label rules: kill the surviving margin mutants on approved real sources, or record which cannot be reached

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-03-fu1-label-margin-mutants`

**Pull Request**: 514

**Owner Role**: implementation

## Objective

OMIT-03 label rules: kill the surviving margin mutants on approved real sources, or record which cannot be reached. Source: authority item OMIT-03-FU1. Non-blocking follow-up 1 from tticomgov-code's approving re-review 5365611424 of tticom/score2gp#473 (OMIT-03) at 51f8f05. Mutants that relax the bar or system uniqueness check (!= 1 to < 1), the two-point tie margin (to 0.5 pt) and the status == "read" event filter survive both the public and the private tests. Show each mutant failing a test that runs on approved real sources; where no approved real source reaches the margin or overlap, record the mutant as not killed, with counts. Synthetic margin or overlap fixtures may supplement only as non-domain test infrastructure and carry no acceptance weight.

## Allowed paths

- `tests/**`
- `fixtures/public/**`
- `src/score2gp/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
