# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: TABONLY-01 — TAB-only sources: infer rhythm from horizontal spacing as a labelled guess instead of refusing

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/tabonly-01-labelled-spacing-guess-for-tab-only-pdfs`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

TAB-only PDFs (the no-score category) are mostly refused: on the 2026-10-30 survey 6 of 7 refused, 4 with pdf_only_tab_no_notation_bars (12 Bar Blues Solo Guitar Jam, 5 MUST KNOW Pentatonic Licks In Em, 7_Grateful_Dead_Melodies, Finger position tips TAB) and 2 with pdf_only_tab_grouping_unsafe (5_Grateful_Dead_Intros, PARANOID - BLACK SABBATH); No Notes converts (9 bars). Maintainer decision 2026-10-27, option B (infer rhythm from horizontal spacing as a labelled guess instead of refusing), and 2026-11-01: 'The no-score refusals are concerning, keep me informed on how that work proceeds. Possibly I can help determine what the system should do with a given no-score fixture and from that you can infer the rule?'. Rhythm without notation is never a read result: every inferred duration is a labelled guess. ASCII and hand-written TAB are separate input classes (IN-02, IN-03).

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
