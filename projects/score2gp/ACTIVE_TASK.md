# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-04-FU1 — Read a whole real Guitar Pro file that has noteless non-rest beats, or refuse them with a located reason

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-04-fu1-read-real-gp-noteless-beats`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Read a whole real Guitar Pro file that has noteless non-rest beats, or refuse them with a located reason. Source: backlog OMIT-04-FU1. Found by the author of tticom/score2gp#475 (OMIT-04) and confirmed as pre-existing by tticomgov-code's approving review 5378371016: extract_score_ir_from_gp refuses the whole real Lesson-3.gp with a noteless-beat error, also at the base with the arpeggios stripped. validate_roundtrip, compare_gp and scripts/oracle.py therefore cannot round-trip a real Guitar Pro file end to end, only the public fixtures. Read beats that carry no note and are not rests (for example a beat that holds only a symbol), or refuse them with a located reason, and add a read test on a real reference.

## Allowed paths

- `src/score2gp/**`
- `tests/**`
- `docs/**`
- `scripts/oracle.py`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
