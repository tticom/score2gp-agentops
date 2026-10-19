# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-04-FU3 — Can't Find My Way Home: attach the five arpeggios refused for lack of written events, or close with evidence

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-04-fu3-cfw-arpeggios`

**Pull Request**: 503

**Owner Role**: implementation

## Objective

Five arpeggio marks in Can't Find My Way Home (bars 2, 6, 7, 18 and 19) were refused with `pdf_arpeggio_beat_unavailable` because those bars had no written events. CFW-04, CFW-05 and later work may have changed that. Re-measure; where a bar is now written, attach the arpeggio with the direction the page shows; where it is not, keep the located refusal.

## Allowed paths

- `src/score2gp/**`
- `tests/**`
- `docs/**`
- `schemas/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
