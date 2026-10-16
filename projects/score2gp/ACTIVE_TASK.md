# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: CFW-05 — Can't Find My Way Home: write bar 6 now that dead-note heads are read

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/cfw-05-dead-note-bar-6`

**Pull Request**: 491

**Owner Role**: implementation

## Objective

Bar 6 of Can't Find My Way Home was refused because the dead-note head was unread. UNREAD-02 (product #489) now reads the cross head and writes percussive strikes. Measure what bar 6 does today; write it correctly if the pairing is unambiguous, otherwise keep it refused with a located reason.

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
