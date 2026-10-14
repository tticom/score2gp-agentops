# UNREAD-02: Dead-note X heads become TAB X events

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** UNREAD-01, DUR-02, CFW-04
- **Branch:** `feat/unread-02-dead-note-x-events`

This task exists because UNREAD-01's first author run stopped at its scope gate (2026-10-10) and the maintainer decided: "finish that pr and then widen the scope to fit in 1 as a or part of the next task." UNREAD-01 therefore leaves dead-note X heads as located `dead_note_x_head` refusals; this task turns them into written dead notes. Every number below is a lead: re-measure it. Never commit private content; report counts, codes, shapes and distances only.

**Private fixtures.** The corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. **Before starting, verify that `fixtures/private/` contains `G-Am-C-Lick.pdf`, `Derek Trucks BB King.pdf` with its reference `.gp`, and `Lesson-3.pdf` to `Lesson-7.pdf`**; if any is missing, stop and say exactly what is missing.

## What UNREAD-01's stopped run found (leads to VERIFY)

- G-Am-C-Lick has four cross-shaped heads (1.16 x 1.0 staff spaces). Their stems carry secondary constant-thickness beams that no recognised head owns: a direct probe of the stems at p0:d42.0 and p0:d43.0 finds no head, and the band alone is `stem_crossing_not_at_tip`. Accepting a band because it passes the beam shape test would silently drop its note ownership; do not.
- `src/score2gp/build_ir.py:1772` keeps only candidates with a numeric `parsed_fret` and `kind == "fret"` (plus the legacy `quarter_rest` token), and line 1801 passes only those into `assemble_note_type_bars`. `src/score2gp/tabraw.py:107` (`parse_fret_text`) parses only digits. An `X` on a string is therefore never a candidate, so a bar whose notation shows a dead note cannot be completed.
- The IR already has `NoteEvent.is_dead` (`ir.py:516`) and `gpif.py` supports the `dead-note` technique, so the representation downstream exists. The gap is the candidate and routing contract, not the schema.
- Whether `pdf.py` extraction keeps an `X` glyph on the TAB (as text or as drawn strokes) is not yet known. Measure it first; edit `pdf.py` only if the census proves the X is lost there.

## Goal

Read each dead-note X on the TAB as a candidate of its own kind (never a fret number), associate it with its notation head, stem, beam and duration by the same staff-space-relative rules as a digit, and write it as a dead note. A numeric-fret file is unchanged at every bar it writes. An X with no owner stays a located refusal.

## Acceptance

1. **Measure first.** Every X head in the approved sources, per file: on the TAB (string, bar, position) and in the notation (head shape, stem, beam); the located `dead_note_x_head` records from UNREAD-01; and, where a reference `.gp` exists, what it shows for the same bar (counts and shapes only; the reference never feeds the reader). Say which X-like glyphs are not dead notes and how the rule tells them apart.
2. **Candidate contract.** A TAB X is a candidate of its own kind with its own parsed value; it is never a fret number. List every consumer of numeric fret candidates that you audited.
3. **Association.** The X is associated with its head, stem, beam and duration by staff-space-relative rules; an X with no owning note, or a stem with no associated head, is a located refusal naming the class.
4. **`pdf.py`** is edited only where the census shows the X is lost at extraction, and the report names the change and its evidence.
5. **G-Am-C-Lick:** bars written and refused before and after, each dead note listed with string, bar and duration, written bars summing to the declared bar total. Files without a reference are not claimed correct; for any other approved source with a reference that contains dead notes, compare every written bar through the independent oracle (`tests/test_dur_02_oracle.py`).
6. **Real-source tests that bite.** Private-corpus tests assert, on more than one approved source, that each dead note is read with its string and duration and that an X with no owner stays refused with a located reason. Mutants: drop the X silently; write the X as fret 0. Each fails those tests on the real files. Public synthetic fixtures are supplementary non-domain infrastructure only, with a stated rationale, and carry no acceptance weight.
7. **Nothing that worked may change.** Measure on the whole private set at base and at head: every file that converts today keeps a byte-identical GPIF for every bar written at base; any bar whose status changes is listed.
8. `python -m pytest` (exact-head CI), export-schema, validate-ir, `scripts/artifact_audit.py` and `git diff --check` pass; list the known Windows baseline failures by ID if they fail locally. No schema change unless the census proves the IR cannot carry the note, and then report it first.

## Rules

- **Domain evidence (AGENT_CONTROL.md):** acceptance rests on genuine approved sources, or reproducible extracts that keep their source provenance and reach the changed seam. Synthetic, mocked or generated-notation tests carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity claims.
- **Read from the source, or refuse.** Never invent a fret, never copy a value from a reference `.gp`, never loosen the numeric-fret gate to raise a count.
- **Scale-relative only:** every new limit is a multiple of the measured staff space.
- **Stop** if the work needs changing what a gate means for numeric frets, or a path outside `allowed_paths`, and report the gate or path.
- **Private tests convert under `<repo>/work`** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, TS-READ-01, UNREAD-01, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02.
- Out of scope: other dead-note-like techniques (ghost notes, muted strums), `bar_total_mismatch` and the other bar-level causes unless the X reading removes one; report such side effects.

## Scope amendment 2026-10-13 (authority revision 126), approved by the maintainer

Author run 1 stopped at the scope gate and reported it first, as rule 8 requires: `Note` (`ir.py:513`) requires an integer `fret` (0-36) and `pitch`, and `gpif.py` emits a DeadNote alongside a numeric Fret/Midi, so a dead note read from an X that prints no fret cannot be stored without inventing one. The maintainer approved widening the scope on 2026-10-13 ("approved") after being shown this design, so `allowed_paths` gains `src/score2gp/ir.py`, `src/score2gp/gpif.py` and `schemas/scoreir.v0.1.schema.json`, on these conditions, which carry acceptance weight:

- `fret` and `pitch` may be absent only on a note with `is_dead = true`; a validator rejects a non-dead note without them. The schema change is additive: every existing IR document still validates, and `export-schema` output changes only by that relaxation.
- The reader never supplies a fret: a dead note leaves `fret` and `pitch` unset in the IR. Writing it as fret 0 in the IR stays the mutant that must fail.
- Only `gpif.py` chooses a storage value, at emission time, because the format requires one. Writer convention (maintainer's musical choice: a dead note is fretted nearest the next note): the fret of the next note on the same string in the same voice; else the previous note on that string; else the open string (0). The value is not a reading of the source, is named as a writer convention in the report, and the report states how Guitar Pro displays and plays the result, with the evidence available.
- Every consumer of `Note.fret` and `Note.pitch` (pitch checks, tuning, key and spelling, tie, merge, fingering, JSON and summary exports) is audited and listed; none may treat an absent value as 0.
- A numeric-fret file stays byte-identical at every bar written at base (acceptance 7 remains a hard stop).
- Census first: finish the X census over every approved source (Author run 1 covered G-Am-C-Lick, Derek Trucks BB King and Lessons 3-7). If G-Am-C-Lick is the only source with dead notes, say so, and acceptance 6 is then met on that source plus the refusal tests on the others; report it rather than claim a second source.

## Scope amendment 2026-10-14 (authority revision 127), maintainer instruction

Terminology (maintainer, 2026-10-14: 'rename "fretless note" as "percussive strike"'): a dead-note X is called a **percussive strike** in this task's reports, tests and documents. The IR flag stays `is_dead` and the GPIF element stays DeadNote (renaming either would be an unrelated schema break); a percussive strike is a note with `is_dead = true` and no fret or pitch. Wherever the amendment above says "fretless dead note", read "percussive strike".

Maintainer instruction the same day: 'We urgently need a way to handle percussive strikes', answering the proposal to extend the scope to the consumers that author run 2 found. Run 2 stopped at the scope gate and named two: `src/score2gp/black_key_spelling.py:52` (`note.pitch % 12` on every note; `TypeError` on a note without pitch) and `src/score2gp/gp_package.py:1651-1652, 1789-1796` (the ScoreIR summary reader maps absent fret/pitch to 0 and rebuilds notes without `is_dead`). `allowed_paths` gains both files, on these conditions:

- Absent stays absent: neither consumer may substitute 0 or the writer's storage convention for a percussive strike's missing fret or pitch; a percussive strike round-trips through the summary with `is_dead = true` and no fret or pitch.
- Spelling and every other pitch-based step skips a percussive strike explicitly, with a test on a real source that carries one (G-Am-C-Lick, E_Chord_Lick_Chord, Can't Find My Way Home at base).
- The consumer audit is completed and listed in full; if it finds another consumer outside `allowed_paths`, stop and report it (do not widen silently).
- Numeric-fret output stays byte-identical at every bar written at base (acceptance 7).

## Scope amendment 2026-10-14 (authority revision 128): the UNREAD-01 assertions this task supersedes

Author run 3 stopped at the scope gate: three UNREAD-01 real-source tests assert that G-Am-C-Lick's twenty crosses stay located unread events and their bars stay refused, which is exactly what UNREAD-01 limited the work to and UNREAD-02 supersedes: `tests/test_unread_01_dead_heads.py:18-33,54-59`, `tests/test_unread_01_mutants.py:53-70,104,118`, `tests/test_unread_01_font_glyphs.py:31-41`. They are added to `allowed_paths`, on these conditions:

- Only assertions that a percussive strike stays refused or unread may change, and each changed assertion is listed in the report with the source evidence that replaces it (a read event with its string and duration, or a located refusal naming the class where the strike has no owner).
- The attached-notehead gate, the numeric-fret expectations and every other assertion in those files stay as they are; no test is deleted or skipped; the mutants keep failing on the real files.
- If any other test outside `allowed_paths` asserts the superseded refusal, stop and report its path.

## Condition correction 2026-10-14 (authority revision 129): aggregate beam-count assertions

Author run 4 stopped at the revision 128 condition that every other assertion in those files stays as it is. Two assertions freeze the total number of read beamed events for G-Am-C-Lick at 54, counting every head kind: `tests/test_unread_01_font_glyphs.py:100-108` (`test_real_source_beams_reach_read_events[G-Am-C-Lick-54]`) and `tests/test_unread_01_mutants.py:30-38` (`_assert_beams`, used by `test_fixed_point_beam_size_mutant_fails_on_scaled_approved_sources[G-Am-C-Lick-54]`). Reading the percussive strikes and their beams necessarily changes that aggregate (the author's no-write probe measured base 54, probe 78). The maintainer approved this correction on 2026-10-14 ("approved"). `allowed_paths` is unchanged. Condition, replacing "every other assertion stays" for these two assertions only:

- The numeric-head part stays frozen: the count of read beamed events that are not percussive strikes remains 54, and the scaled-source mutants keep failing on the real files.
- The percussive-strike beamed events are asserted separately with the measured count, remeasured after complete ownership, and the report lists the old and new totals with the evidence.
- No other assertion in those files changes beyond the revision 128 conditions; nothing is deleted or skipped.
