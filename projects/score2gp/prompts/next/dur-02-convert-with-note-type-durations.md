# DUR-02 — Convert with note-type durations; delete the count rule

- **Repository:** `tticom/score2gp`
- **Depends on:** DUR-01
- **Requirement:** REQ-0001
- **Branch:** `feat/dur-02-convert-with-note-type-durations`

## Goal

The PDF conversion route takes every duration from DUR-01's note-type reader, and takes positions (string and fret) from the TAB. Maintainer, 2026-09-26: rhythm comes only from note types and their grouping, and counts are irrelevant.

At product `3af1925`, `determine_pdf_tab_event_duration` takes a recognised rest or `visual_morphology` evidence first, and falls back to a guess when it is missing. This task deletes every one of those guesses, rather than bypassing them:
- the count-based fallback (`select_pdf_tab_grid_spacing_and_duration_name`);
- the 960-tick quarter `equal_spacing_fallback` emitted by `pdf_tab_duration_associator.py` for unstemmed events without visual candidates (declared in `pdf_tab_duration_types.py`, listed in `tabraw.py`);
- the editable-draft quarter-note default;
- the remainder rest padding (`decompose_pdf_tab_measure_remainder_to_rests`).

Existing `visual_morphology` evidence is kept only if it meets DUR-01's standard: derived from identified symbols, with the symbols cited. Otherwise DUR-01's records replace it.

It is the first time the product can produce a Guitar Pro file from a real source with real rhythm. The maintainer will then open that file in Guitar Pro.

## Acceptance

1. The four fallbacks above are deleted from `src/`: no producer emits `equal_spacing_fallback`, and the source type no longer admits it. If that changes the TabRaw payload shape, bump its contract version. No code path assigns one duration to a group of notes, or derives a duration from an event count, note spacing, a default or a bar total. No other gate is weakened.
2. The conversion route takes each event's duration from DUR-01's records, and each event's positions from the TAB. Events in the notation and the TAB are matched by column, with the match recorded.
3. A bar with an unread event, a notation/TAB mismatch, or a total that disagrees with the time signature is not written with invented values. It is refused with a located reason code in the diagnostics.
4. Converting `Lesson-3.pdf` produces a GP file, and the independent oracle comparator against `Lesson-3.gp` reports, for every bar the product writes:
   - equal durations, including dots, tuplets and ties;
   - equal rests;
   - equal string and fret positions.

   Report coverage (bars written out of bars in the source) and every difference, by bar and event index.
5. The same comparison runs for Lessons 4-7, and coverage and differences are reported.
6. Tests that asserted count-derived durations or padded rests are converted to assertions of note-type durations or refusals, and none is deleted without a replacement. Restoring the count rule makes the tests fail.
7. `python -m pytest`, `export-schema`, `validate-ir`, `scripts/artifact_audit.py` and `git diff --check` all pass.

## Constraints

- No duration guess, and no gate loosened.
- The MusicXML-timed route stays correct.
- Commit no private musical content. The generated GP files for the maintainer stay under `work/`, and their paths are given in the handback.
