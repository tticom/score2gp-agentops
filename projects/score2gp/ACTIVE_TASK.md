# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-04-FU1 — Convert G-Am-C-Lick.pdf correctly, or refuse each unreadable bar with a located reason (retargeted from Lesson-3.gp reading)

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-04-fu1-g-am-c-lick-pdf`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Retargeted on the maintainer's direction (2026-10-21): 'change the fixture used for this development item. Focus the development on G-Am-C-Lick.pdf although currently there is no equivalent gp file.' The original premise (Lesson-3.gp is refused for noteless non-rest beats) was disproved by the author's preflight on 2026-10-20: at main a2d232d the file reads (66 bars, 465 events) and its two noteless beats are already decoded as rests, as an existing regression test requires. G-Am-C-Lick.pdf converts PARTIAL (4 bars written, 5 shortfalls: note_duration_event_unread x3, notehead_digit_count_mismatch x2). Find each root cause and write the bar correctly or refuse it with a located reason. No reference .gp exists and none may be invented: the PDF's printed notation and TAB are the oracle.

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
