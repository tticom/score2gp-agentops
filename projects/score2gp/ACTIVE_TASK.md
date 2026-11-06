# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: TABGUESS-01 — Design and score the spacing model for TAB that prints no rhythm

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/tabguess-01-design-and-score-the-spacing-model`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

The 53 bars refused as note_duration_event_unread / tab_column_without_rhythm_mark and most of the 29 bars refused as bar_without_notation_or_tab_item are TAB that prints no rhythm at all (no stems, beams, flags, notation staff or beat counts), so reading strategies 1 to 3 in knowledge/tab-rhythm-reading-strategy.md produce nothing. The maintainer decided on 2026-10-27 (option B) that a labelled guess is the last strategy, and on 2026-11-01 that rhythm 'should not guessed until no other reading strategy produces a plausible rhythm'. This task designs that last strategy and SCORES it; it does not write guessed bars into any output. The central difficulty is that nothing in these sources can show a guess is right, so score the model on sources where the rhythm is printed and read (strategies 1 and 2 give the truth) by hiding the printed rhythm, then apply it to the no-rhythm sources only as a labelled report.

## Allowed paths

- `src/score2gp/**`
- `tests/**`
- `docs/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
