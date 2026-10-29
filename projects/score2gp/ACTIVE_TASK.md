# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: TRIP-01 — Check and fix recognition of mixed quarter, eighth and quarter-note-triplet durations

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/trip-01-mixed-quarter-eighth-triplet-durations`

**Pull Request**: 529

**Owner Role**: implementation

## Objective

Investigate whether duration recognition handles mixed quarter notes, eighth notes and quarter-note triplets (1/4-note triplets, as the maintainer wrote; eighth-note triplets are checked as well if the score prints them), using Mixing Lead & Rhythm pt1.pdf (the PDF, which is not corrupted). Maintainer 2026-10-29: 'The note counts are consistent, but maybe highlighting a flaw in the codes note duration recognition as there are mixed 1/4, 1/8 and 1/4 note triplets in the score. So if we can't recognise that we've found a system flaw.' Its reference .gp is unreadable (high-entropy score member), so the printed notation is the only check and results are labelled not independently verified.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
