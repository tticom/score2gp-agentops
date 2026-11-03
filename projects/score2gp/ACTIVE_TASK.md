# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: REFUSE-07 — Reduce the unread-duration refusals left in the newly routed sources

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/refuse-07-hey-joe-pride-and-joy-refused-bars`

**Pull Request**: 541

**Owner Role**: implementation

## Objective

After GROUP-01, Hey Joe and Pride and Joy write only part of their bars: the rest are refused with note_duration_event_unread (12 bars) and bar_total_mismatch / mixed_percussive_tie_ownership_unread. Measure the refusal reasons on those two sources and the whole set, and read the largest class that is unambiguously musical from note type plus grouping. Leads, not facts: re-measure.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
