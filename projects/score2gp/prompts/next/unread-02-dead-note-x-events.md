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
