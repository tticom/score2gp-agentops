# DUR-02 — Convert with note-type durations; delete the count rule

- **Repository:** `tticom/score2gp`
- **Depends on:** DUR-01
- **Requirement:** REQ-0001
- **Branch:** `feat/dur-02-convert-with-note-type-durations`

## Goal

The PDF conversion route takes every duration from DUR-01's note-type reader, and takes positions (string and fret) from the TAB. Maintainer, 2026-09-26: rhythm comes only from note types and their grouping, and counts are irrelevant.

This task deletes the following, rather than bypassing them:
- the count-based duration choice (`select_pdf_tab_grid_spacing_and_duration_name`);
- the editable-draft quarter-note default;
- the remainder rest padding (`decompose_pdf_tab_measure_remainder_to_rests`).

It is the first time the product can produce a Guitar Pro file from a real source with real rhythm. The maintainer will then open that file in Guitar Pro.

## Acceptance

1. The three rules above are deleted from `src/`. No code path assigns one duration to a group of notes, or derives a duration from an event count, note spacing, a default or a bar total.
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
