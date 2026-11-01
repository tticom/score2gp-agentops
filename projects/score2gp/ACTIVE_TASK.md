# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: TABRHY-01 — Read the rhythm printed under staffless TAB (stems, beams, flags, dots, ties, rests, triplets, whole-note chords)

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/tabrhy-01-read-rhythm-printed-under-staffless-tab`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Read the rhythm that staffless TAB prints under the strings. Six of the seven no-score PDFs are refused (4 with pdf_only_tab_no_notation_bars, 2 with pdf_only_tab_grouping_unsafe; one converts). The supervisor viewed one of each refusal code: they are Guitar-Pro-style TAB with printed rhythm below the strings, so the durations are READ from it (strategy 2 below), never counted or guessed. The maintainer judged both: both should convert, and for the grouping_unsafe one "the tab grouping safety or resolution needs to be increased until the tab is safely determinable". The maintainer's judgements on the two named fixtures are in the private-fixtures file `fixtures/no-score/MAINTAINER-JUDGEMENTS-2026-11-01.md` (it reaches you as `fixtures/private/MAINTAINER-JUDGEMENTS-2026-11-01.md`); read it first. It is private: never copy its content into the repository, the PR or the handback.

## Reading order (maintainer, 2026-11-01: "it should not guessed until no other reading strategy produces a plausible rhythm")

Try these in order, per bar; the first that gives a plausible rhythm wins. A rhythm is plausible only if the bar's durations total exactly the printed meter's capacity (the rational meter utility) and nothing printed contradicts it.

1. **Printed notation staff**, where one exists: note types win (the existing reader).
2. **Rhythm marks printed under the TAB** (staffless TAB, as Guitar-Pro-style exports print it): stems, beams, flags, augmentation dots, tie arcs, rest glyphs, tuplet brackets with their numbers, and circled stemless chords.
3. **Printed beat-count text** under or over the TAB, where there is any.
4. **Last resort, a labelled guess:** infer the rhythm from the TAB itself (equal column spacing, count of columns). Every such duration is labelled GUESS in the report and in the GP file and is never counted as a read result. This is the separate authority item TABONLY-01 and is not part of this task.

If no strategy gives a plausible rhythm, the bar is refused with a located reason, as now.

## Musician knowledge (general; recorded from the maintainer and standard notation practice)

- A chord is the digits stacked on different strings at one horizontal position.
- In TAB-only notation a circle around stemless fret digits marks a whole note (one chord filling a bar in 4/4). The supervisor believes this; the author must show from a real PDF what the circle means before relying on it.
- A stem with no beam and no flag is a quarter note (when the beat unit is a quarter); one beam or one flag is an eighth; two are a sixteenth; a dot adds half the note's value; a bracket with a number groups a tuplet.
- A tie or slur arc between two notes of the same pitch holds the first for the length of both; a note that ends a tie carries on into the next beat.
- A rest glyph is a rest of its printed type.
- Where the printed notes in a bar total less than the meter and nothing else is printed for the remainder, the maintainer reads the remainder as a rest ("a missing rest"). Treat this as an implied rest: write it as a rest, but label it IMPLIED in the report, count it separately from printed rests and never use it to make a bar that otherwise disagrees (too many notes, or a contradicting mark) pass.
- Bends, slides, hammer-ons, pull-offs, vibrato, palm-mute spans, repeat signs and chord names are separate features and are not rhythm.

The same reading order and knowledge are recorded in projects/score2gp/knowledge/tab-rhythm-reading-strategy.md of the governance repository.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
