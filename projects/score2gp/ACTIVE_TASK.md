# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: GROUP-02 — Accept repeat-sign start barlines as system barlines where the evidence is unambiguous

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/group-02-repeat-sign-start-barlines`

**Pull Request**: 540

**Owner Role**: implementation

## Objective

GROUP-01 (merged) left 5_Grateful_Dead_Intros refused at grouping (missing_pdf_barlines): 5 systems, one with a single barline because a repeat-sign start barline is classed as floating. It is readable music. Measure the remaining grouping refusals on the current runtime, then let repeat-sign (thick-thin or dotted) start and end barlines count as system barlines only where the drawn evidence makes it unambiguous. Do not loosen or bypass a safety check; a barline the evidence cannot settle stays refused with a located reason.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
