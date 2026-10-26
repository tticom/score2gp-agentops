# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-03-FU3 — Labels: measure the 51 corpus lines between five and seven staff spaces above the staff and give the rotated tab-clef glyph its own reason code

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-03-fu3-label-band-source-role`

**Pull Request**: 516

**Owner Role**: implementation

## Objective

Labels: measure the 51 corpus lines between five and seven staff spaces above the staff and give the rotated tab-clef glyph its own reason code. Source: authority item OMIT-03-FU3. Non-blocking follow-up 3 from tticomgov-code's approving re-review 5365611424 of tticom/score2gp#473 (OMIT-03) at 51f8f05. The label band is a fixed five staff spaces above the top staff line. One real Lesson 4 reference label sits 6.4 spaces above and is refused, and 51 corpus lines between five and seven spaces still need a measured source-role rule before the band can widen without admitting a wrong read. In Lesson 4 pdf_text_outside_annotation_band also holds the rotated tab clef glyph, so the missing label is identifiable only by its located bbox: give that glyph its own reason code.

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
