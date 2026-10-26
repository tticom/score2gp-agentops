# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-04-FU2 — Arpeggio direction: comment the upward-arrow-to-Down mapping and verify Up on a real reference when one exists

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-04-fu2-arpeggio-direction-mapping`

**Pull Request**: 515

**Owner Role**: implementation

## Objective

Arpeggio direction: comment the upward-arrow-to-Down mapping and verify Up on a real reference when one exists. Source: authority item OMIT-04-FU2. Non-blocking follow-ups from tticomgov-code's approving review 5378371016 of tticom/score2gp#475 (OMIT-04) at 3c5536d: _marks in src/score2gp/pdf_arpeggios.py labels an upward arrow 'down' (the GPIF value) with no code comment explaining it, and only the Down value occurs in the real references, so Up is verified only on a synthetic fixture. Document the mapping where it is made and verify Up against a real reference when one has an up arpeggio.

## Allowed paths

- `src/score2gp/**`
- `tests/**`
- `docs/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
