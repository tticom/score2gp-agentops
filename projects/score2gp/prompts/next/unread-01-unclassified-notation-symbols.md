# UNREAD-01: Unclassified notation symbols refuse whole bars

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001 (folds in the former follow-up DUR-01-FU1, now DROPPED in the authority)
- **Depends on:** DUR-02, CFW-04 (both merged)
- **Branch:** `feat/unread-01-classify-notation-symbols`

This comes from the 2026-10-08 fixture survey (main `95a6802`) and a read-only diagnosis of the same day. Every number below is a lead: re-measure it. Never commit private content; report counts, codes, shapes and distances only.

**Private fixtures.** The corpus is grouped by category on fixtures `main` (49 files); the author launcher flattens it into `fixtures/private/`. **Before starting, verify that `fixtures/private/` contains `Derek Trucks BB King.pdf` and its reference `Derek Trucks BB King.gp`, `G-Am-C-Lick.pdf`, `Am-blues-lick.pdf`, `Just-Practice-Like-THIS-Every-Day.pdf`, `The_EXACT_System_Pros_Use_To_Sound_Great_On_ANY_Chord.pdf` and `Lesson-3.pdf` to `Lesson-7.pdf`**; if any is missing, stop and say exactly what is missing.

## What was measured (leads to VERIFY)

- `note_duration_event_unread` is the largest bar-level refusal in the survey: **34 bars** (Derek Trucks BB King 19 of its 20 bars, G-Am-C-Lick 8 of 9, The_EXACT_System 5, Am-blues-lick 1, Just-Practice 1). For the first refused bars of Derek Trucks and G-Am-C-Lick the recorded detail is `symbol_unclassified` (the event whose symbol the notation reader could not classify; `src/score2gp/notation_omr/note_duration.py`).
- **Derek Trucks BB King** writes 0 of 20 bars, so no file is produced. Its `note-durations.json` also records **29 `key_clef_unread` records** (`src/score2gp/notation_omr/key_signature.py`) and 52 unclassified records, which suggests a clef or key form the readers do not know, besides the symbols. It has a reference `.gp`, which makes it the measurable target.
- G-Am-C-Lick (no reference) writes 1 of 9 bars; its refused bars are `symbol_unclassified` as well.
- Folded in from the former follow-up DUR-01-FU1 (review 5328475963 of #466): an unrecognisable glyph overlapping a notehead or stem is counted by reason today instead of recorded as a located unread event; in Lessons 3 to 7 these are only accidentals or articulations, so keep that case visible for unsupported overlapping forms.

## Goal

Find out which symbols are unclassified, in which classes and how many, then read the ones that are standard notation by a staff-space-relative rule, and give every other one a located reason that names its shape class. A bar is never written with a symbol silently dropped.

## Acceptance

1. **Measure first.** A census over all 34 refused bars (and every `key_clef_unread` record): per file and per class of symbol, with its size as a multiple of the staff space, where it sits (on a stem, on a head, between events, above or below the staff), and what the reference shows there for Derek Trucks (counts and shapes only; the reference is for comparison only and must never feed the reader).
2. **The key and clef forms** that Derek Trucks BB King triggers: say what they are and whether they are in OMIT-01's remit; read them if the rule is staff-relative and unambiguous, otherwise a located refusal.
3. **Reading rules** for the largest classes, each staff-space-relative, with no new absolute point limits; classes you do not read are recorded as located unread events (page, system, bar, event), with their class name, not as a count by reason (DUR-01-FU1).
4. **Derek Trucks BB King**: report bars written and refused before and after. For every bar that is written, compare with the reference through the independent oracle (`tests/test_dur_02_oracle.py`) and report every difference. **G-Am-C-Lick, Am-blues-lick, Just-Practice and The_EXACT_System have no reference: say so**, report which bars changed status and verify that written bars sum to the declared bar total.
5. **Real-source tests that bite.** Private-corpus tests assert, on more than one approved source (Derek Trucks BB King, G-Am-C-Lick and at least one converting lesson), that each class you read is read, and that an unreadable overlap in a real file stays refused with a located reason. Mutants: drop an unclassified symbol silently; accept a class by a fixed point size. Each fails those tests on the real files. Public synthetic fixtures are supplementary non-domain infrastructure only, with a stated rationale, and carry no acceptance weight.
6. **Nothing that worked may change.** Measure on the whole private set at base and at head: every file that converts today keeps a byte-identical GPIF for every bar written at base. The before and after table covers every converting and every refused file; any bar whose status changes is listed.
7. `python -m pytest` (exact-head CI), export-schema, validate-ir, `scripts/artifact_audit.py` and `git diff --check` pass; list the known Windows baseline failures by ID if they fail locally.

## Rules

- **Domain evidence (AGENT_CONTROL.md):** acceptance rests on genuine approved sources, or reproducible extracts that keep their source provenance and reach the changed seam; general claims need more than one approved corpus input. Synthetic, mocked or generated-notation tests carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity claims; they may supplement non-domain infrastructure only with a stated rationale.
- **Read from the source, or refuse.** Never invent a value, never copy one from a reference `.gp`, never loosen a gate to raise a count (a count is a result, not a target). A symbol that cannot be classified stays a located refusal.
- **Scale-relative only:** every new limit is a multiple of the measured staff space.
- **Stop** if reading a class needs changing a gate's meaning rather than its scale, and report the gate.
- **Stay inside `allowed_paths`;** if you need another path, stop and report it.
- **Private tests convert under `<repo>/work`** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02.
- Out of scope: `bar_total_mismatch`, `notehead_digit_count_mismatch`, `bar_without_notation_event` and `notation_note_without_tab_digit` (other bar-level causes in the survey, 47 bars) unless a symbol class you read removes one; report such side effects.

## Maintainer decision of 2026-10-10 (supersedes the dead-note part of the goal)

The first author run stopped at the scope gate: G-Am-C-Lick contains standard dead-note X heads, and writing them needs a TAB `X` candidate and routing contract in `build_ir.py:1772/1801` and `tabraw.py:107`, which are not in `allowed_paths`. The maintainer's decision (2026-10-10, option 2): "finish that pr and then widen the scope to fit in 1 as a or part of the next task."

For this task that means:

- **Dead-note X heads are a located refusal.** Each is recorded as an unread event with class name `dead_note_x_head` (page, system, bar, event), and its bar stays refused. Do not write an `X` event, do not edit `build_ir.py`, `tabraw.py` or `pdf.py`, and do not read a band attached to such a head as a beam of another note (that would silently drop note ownership).
- **Everything else stays in scope**: the constant-thickness bands that are real beams, the narrow curved strokes, the other curved forms and rest-sized curves, the overlap case folded in from DUR-01-FU1, and the clef and key forms.
- **The music-font clef and key glyphs** of Derek Trucks BB King (embedded font `GPBravuraRegular`: U+E050 clef, U+E260 flat, and the head, flag and rest code points U+E0A4, U+E241, U+E4E5 and U+E4E6) are text, not drawings, so the drawing-glyph clef reader never sees them. Read them if the reader can take them from the page text by a staff-relative rule inside `allowed_paths`; otherwise record a located refusal that names the font-glyph form. Do not edit `pdf.py` for this; if it cannot be done inside `allowed_paths`, report the exact seam.
- **The follow-up** is UNREAD-02 (dead-note X contract, wider paths). Do not do any of it here; leave the located `dead_note_x_head` records that UNREAD-02 will consume.
- **Leads from the stopped run** (re-measure; counts and shapes only). At base, reader level: Derek Trucks 20 bars, 0 read / 62 unread (52 `symbol_unclassified`, 10 `rest_glyph_unidentified`, 19 incomplete bars); G-Am-C-Lick 9 bars, 70 / 12; Am-blues-lick 19 / 1; Just-Practice 114 / 3; The_EXACT_System 265 / 9; incomplete-bar sum 34. Of the 62 Derek unread events, 50 pass the constant-thickness-band shape test (width 0.88 to 25.33 spaces, bbox height 0.5 to 2.0), eight are narrow curved strokes (0.8 x 1.0), three are other curved forms and one is a rest-sized curve. G-Am-C-Lick has six unattached bands, four cross-shaped heads (1.16 x 1.0) and two other curved forms. Derek has nine systems, each with one clef and four flats (key of minus four) as music-font text; its reference has sixteen master bars against twenty reader partitions, so do not assume the indices align.
