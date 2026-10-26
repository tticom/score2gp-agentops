# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-04-FU4 — attach_pdf_arpeggios: split the long, deeply nested function

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-04-fu4-split-attach-pdf-arpeggios`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

attach_pdf_arpeggios: split the long, deeply nested function. Source: authority item OMIT-04-FU4. Non-blocking style follow-up from tticomgov-code's approving review 5378371016 of tticom/score2gp#475 (OMIT-04): attach_pdf_arpeggios in src/score2gp/pdf_arpeggios.py is one long, deeply nested function. Split it into candidate selection, chord location and beat choice, and name the thresholds, keeping the written GP byte-identical.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
