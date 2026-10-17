# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: SLIDE-01 — Slides: write the slide type the source shows, and report slide marks that were not extracted

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/slide-01-slide-types-and-unextracted-marks`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Every slide is written as one fixed type regardless of the source mark (shift, legato, in, out), and a curved slide mark with no extracted candidate (Lesson 5 bars 16 and 17) produces no slide and no warning. Read the type from the source where it is readable, otherwise record why not, and make every unextracted slide mark a located diagnostic: no silent omission.

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
