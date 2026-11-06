# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: PERCX-01 — Read X percussive strikes in TAB that has no notation staff

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/percx-01-read-x-strikes-in-tab-only-systems`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

NOROUTE-01 found that a one-page TAB-only source (five systems, printed 4/4, chord names, no stems, beams or flags) stops with percussive_strike_without_owning_note: 0 notation bars, 82 TAB digits unplaced and 6 X strikes (system 4, bar 6). The maintainer decided the terminology and storage of X heads (percussive strikes) in UNREAD-02 (see the percussive-strike memory). Without a notation staff an X strike has no owning note, so the route refuses before any bar. The source prints no rhythm marks, so its durations are TABGUESS-01 territory; this task is only about letting a strike without an owning note be read and carried, so that the layer below rhythm is complete. Leads, not facts: re-measure.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
