# DUR-01 — Read note durations from note types

- **Repository:** `tticom/score2gp`
- **Priority:** highest (maintainer, 2026-09-26: "The system fundamentally must understand note duration. This is now the highest priority!")
- **Requirement:** REQ-0001 (usable GP output from real sources)
- **Branch:** `feat/dur-01-note-durations-from-note-types`

## The rule

Every note and rest carries its own duration, and that duration is written in its **note type**. Maintainer, 2026-09-26: "It is the note type and the grouping of those notes that determine rhythm ... counts are irrelevant. One note could be a count of 6, the next 8 could be 32nd notes. Music does not work like that."

**Base value, read from the note itself:**

| Symbols | Value |
|---|---|
| Hollow notehead, no stem | whole |
| Hollow notehead with stem | half |
| Filled notehead with stem, no flag or beam | quarter |
| Plus 1 flag, or 1 beam at the stem | eighth |
| Plus 2 | sixteenth |
| Plus 3 | thirty-second |
| Plus 4 | sixty-fourth |

**Modifiers:**
- Each augmentation dot adds half of the previous value: one dot gives 1.5×, two dots 1.75×.
- A tie joins two written values into one sounding note. Record the tie; do not merge the values.

**Rests** have their own symbol for each value (whole, half, quarter, eighth, sixteenth, thirty-second), and take dots the same way.

**Grouping:**
- A beam group relates notes within a beat. The number of beam lines meeting each stem gives that note's value, so a group can mix values: for example an eighth beamed to two sixteenths, or a partial beam.
- A tuplet bracket or number (for example 3 in the time of 2) scales only the notes it spans.

**The bar total:** it must match the time signature, but only as a **check** on what was read. It is never a source of durations and never a reason to fill gaps.

## Current state (product `3af1925`)

- The conversion route still guesses. `select_pdf_tab_grid_spacing_and_duration_name` gives every event in a bar one duration chosen from the event count, and the remainder is padded with rests. DUR-02 deletes this. DUR-01 must not use it or anything like it.
- `notation_omr/` holds partial evidence: whole, half and quarter notehead candidates, flag and beam candidates, `compose_filled_duration_candidates`, tuplet markers and a timeline preview.
- Its flag reading is itself a count. It picks 1, 2 or 3 flags from the **number of drawing segments** near the stem, with thresholds 25, 45 and 65. It does not identify flag shapes. There are no dots, no eighth or shorter rests, and no working tuplet or tie handling.
- `generate-sidecar` crashes on all seven real sources (RES-REQ-0005, gap G5).
- The painted-contour and visibility-at-contact recognition built for L3-01 barlines is the basis TOP-02 intends to share with noteheads, stems and beams. Reuse it where it fits.

## Deliverable

A duration reader for the notation staff. For every event (note, chord or rest) it emits a duration record:

- the page, system, bar and event index;
- the notehead kind (hollow or filled) and whether there is a stem;
- the identified flag glyphs, or the number of distinct beam lines meeting that stem;
- dots, rest glyph type, tuplet ratio and group, and ties;
- the resulting value.

Each field cites the drawn symbols it came from. Expose the reader through a CLI command that writes the records as JSON under a caller-chosen output directory.

When the symbols are ambiguous, the event is recorded as **unread**, with a located reason. It is never guessed.

## Acceptance

1. **Symbol-derived records.** Every duration record is derived from symbols, per the rule above:
   - a flag count is a count of identified flag glyphs, never of drawing segments;
   - a beam count is the number of distinct beam lines meeting that stem;
   - dots, rests, tuplets and ties are read;
   - each field cites its source symbols.
2. **Forbidden sources.** No duration comes from event counts, note spacing, a default, or the bar total. The bar total against the time signature is reported as a check only. An ambiguous event is recorded as unread, with a located reason.
3. **Synthetic public fixtures.** Committed, generated PDFs, read 100% correctly:
   - a bar mixing a half note and eight thirty-second notes (the maintainer's example);
   - dotted and double-dotted notes;
   - an eighth beamed to two sixteenths, and a partial beam;
   - a triplet;
   - each rest type;
   - a tie across a barline.
4. **Real-source accuracy.** Read `Lesson-3.pdf` and compare per event with `Lesson-3.gp`, using the independent oracle reader rather than the product's own model.
   - Every event of the first system is read, and equals the ground truth.
   - For the whole document, report coverage and match rate, and list every mismatch or unread event by page, bar and event index with its cause.
   - Committed reports hold counts, indices and codes only.
5. **Mutation checks.** Each of these changes makes the tests fail:
   - replacing flag-glyph identification with a segment count;
   - ignoring dots;
   - ignoring tuplets;
   - deriving values from the number of events in a group.
6. **Validation.** `python -m pytest`, `export-schema` (no schema diff unless the change is intended and documented), `validate-ir`, `scripts/artifact_audit.py` and `git diff --check` all pass.

## Constraints

- No duration guess of any kind, and no gate loosened to make a fixture pass.
- The conversion route is out of scope (DUR-02).
- Commit no private musical content, note or fret data, or coordinates. Real-source outputs stay under `work/`.
