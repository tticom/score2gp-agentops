# RHY-00 — Refuse output whose rhythm was not read from the notation

- **Repository:** `tticom/score2gp`
- **Requirement:** REQ-0001 (usable GP output), REQ-0005 (explained shortfalls); maintainer direction 2026-09-26
- **Branch:** `feat/rhy-00-refuse-unread-rhythm`

## Why

Maintainer direction, 2026-09-26: "It is the note type and the grouping of those notes that determine rhythm. Guessing that 8 notes mean they're all 8th notes will lead to disaster. Stop that right now and understand the note types."

A note's duration is written in its **note type**, and **grouping** relates the notes to each other:

- the notehead: hollow (whole or half) or filled (quarter or shorter);
- the stem;
- flags, or the beams that replace them (one for an eighth, two for a sixteenth, three for a thirty-second);
- augmentation dots;
- rest symbols;
- tuplet brackets or numbers (for example 3 in the time of 2);
- ties.

Beams group notes within a beat. The bar's total must then match the time signature. That total is a check on what was read, never a source of durations.

At product `3af1925`, the PDF-only route reads none of this:

- `select_pdf_tab_grid_spacing_and_duration_name` (`src/score2gp/pdf_tab_measure_timing.py`) gives **every** event in a bar the same duration, chosen from the number of events: up to 8 become eighths, up to 16 sixteenths, up to 32 thirty-seconds, and more become sixty-fourths.
- `--editable-draft` makes every event a quarter note.
- `decompose_pdf_tab_measure_remainder_to_rests` then fills whatever is left of the bar with invented rests.
- `src/score2gp/pdf_tab_bar_assembler.py` calls all of this from `build_ir.py`.
- The result is reported as `success`. This is gap G7, plus G8 for the rests, in the RES-REQ-0005 research.

## Goal

No GP output may contain a duration or rest that was not read from note types and grouping.

- Until rhythm evidence exists (REC-10, which builds on TOP-02), the `--pdf-only-tab` and `--editable-draft` routes must **refuse** before writing any GP file.
- The refusal carries a stable, located reason code.
- The MusicXML-timed route, where durations come from the MusicXML note types, is unchanged.

## Acceptance

1. The count-based duration choice, the editable-draft quarter-note default and the remainder rest padding are removed from every code path that can produce output. No function in `src/` derives a duration from an event count, from note spacing or from a fixed default.
2. `convert --pdf-only-tab` and `convert --editable-draft` refuse on a public PDF fixture and on the real `Lesson-5.pdf`:
   - they exit non-zero with refusal code `pdf_rhythm_not_read` (stage `measure-assembly`);
   - the refusal gives the page, system and bar where rhythm was needed;
   - the message says rhythm must come from note types and grouping;
   - no new GP file is written.
3. MusicXML-timed conversions and their tests are unchanged and pass.
4. Every test that asserted a count-derived duration or a padded rest is converted into a refusal assertion, and none is deleted without a replacement. A mutation check that restores the old duration choice makes the refusal tests fail.
5. The product docs that describe the heuristic (`docs/design/pdf-tab-duration-candidate-extraction.md`, `docs/musicxml-tabraw-build-ir.md`) say it was removed and why, and name the refusal code.
6. The mandatory product checks pass: `python -m pytest`, `export-schema` with no schema diff, `validate-ir`, `scripts/artifact_audit.py`, `git diff --check`.

## Constraints

- Tighten, never loosen: no gate is widened, and no alternative guess replaces the removed one. That means no spacing-based, beat-grid or "most common value" durations.
- Commit no private musical content, note or fret data, or coordinates.
- Leave stale output from earlier runs to NATIVE-01. Here, a refusing run must simply not write or overwrite a GP file.
