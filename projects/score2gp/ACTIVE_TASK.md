# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: DUR-03-FU1 — TAB staff recovery: guard the old_line_rows >= 5 clause on approved real sources

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/dur-03-fu1-old-line-rows-guard`

**Pull Request**: 513

**Owner Role**: implementation

## Objective

TAB staff recovery: guard the old_line_rows >= 5 clause on approved real sources. Source: authority item DUR-03-FU1. Non-blocking follow-up 1 from tticomgov-code's approving review 5376313575 of tticom/score2gp#474 (DUR-03) at 5e52dee. Eight real TAB systems depend on the old_line_rows >= 5 clause in the recovery rule in src/score2gp/pdf.py. No public fixture or mutant exercises it: removing the clause passes all seven public DUR-03 tests, and only the private Lesson 5 bar count guards it. Guard the clause with a test over the approved private corpus (counts and labels only) and show the named mutants failing it; a mutant no approved real source reaches is reported as not killed, with counts. A committed synthetic fixture may supplement only as non-domain test infrastructure and carries no acceptance weight.

## Allowed paths

- `src/score2gp/**`
- `tests/**`
- `fixtures/public/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
