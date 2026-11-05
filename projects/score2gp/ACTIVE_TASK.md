# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-16 — Read the accidental and curved forms beside and over or under noteheads

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-16-read-accidental-and-curved-forms`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

After REFUSE-14, the largest group of refused bars with printed notes is unsupported_overlapping_form (9 bars) plus 8 more bars counted under notehead_digit_count_mismatch that carry the same unread accidental_beside_notehead / over_or_under_notehead curved forms (5 sources). These are accidentals other than naturals and curves that are neither ties nor slurs. Leads, not facts: re-measure. Extend the score model only where a glyph's meaning is fixed by notation (sharp, flat, double sharp, courtesy accidental, slide or articulation curve); keep the pitch honest because the TAB digit is the authority for string and fret.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
