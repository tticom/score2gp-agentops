# PDF-GROUP-03: Songbook transcriptions refused at bar-box construction

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** PDF-GROUP-02, SCALE-01 (both merged)
- **Branch:** `feat/pdf-group-03-song-bar-boxes`

This comes from the 2026-10-08 fixture survey (main `95a6802`) and a short read-only diagnosis of the same day. It is investigate-first, like PDF-GROUP-01 and PDF-GROUP-02: **read the PDF-GROUP-01 close-out (completed_tasks in `projects/score2gp/ORCHESTRATION_STATE.json`, governance #763) first, because the gates it named and stopped at may overlap this one.** This is not the string-line-gap gate of PDF-GROUP-02 (A7-Blues-Lick and E_Chord_Lick_Chord pass it now). Every number below is a lead: re-measure it. Never commit private content; report counts, codes and distances only.

**Private fixtures.** The corpus is grouped by category on fixtures `main` (49 files); the author launcher flattens it into `fixtures/private/`. **Before starting, verify that `fixtures/private/` contains all nine files named below plus `Lesson-3.pdf` to `Lesson-7.pdf` and `Melodic Soloing Masterclass.pdf`**; if any is missing, stop and say exactly what is missing.

## What was measured (leads to VERIFY)

- Nine with-score sources refuse at layout gating with the same codes: `pdf_only_tab_grouping_unsafe`, with `details.refusal_warning_code = pdf_bar_box_construction_not_enough_for_build_ir`. They are **Back In Black, Black Dog, Brown Sugar, Castles Made of Sand, Crossroads, Ex 2 Hands Up, Heartbreaker, Hey Joe and Pride and Joy** (all converted with `--pdf-only-tab --time-signature 4/4`; PDF grouping itself is reported `grouped`, the refusal is that too few bar boxes are built).
- In each of the nine the barline detector discards most candidate strokes with the diagnostics `barline_too_short`, `barline_does_not_cross_staff`, `barline_partial_staff_crossing`, `barline_crosses_insufficient_string_gaps`, `barline_outside_system_bounds` and `barline_outside_staff_region` (4 to 14 of each per file). The files that convert (the GP-exported lessons) show the same diagnostics at lower counts, so the counts alone do not discriminate: **find what is different about the nine's barline strokes** (stroke length against the staff height or string spacing, whether they span the TAB only, the notation staff only or both, whether they are drawn in pieces, their x position against the system, their line cap or width).
- Eight of the nine have no reference `.gp`. **Ex 2 Hands Up has one** (repeat-ends at bars 1, 4, 6 and 8, no double bars), which makes it the measurable target: compare with the independent oracle (`tests/test_dur_02_oracle.py`) after conversion and report every difference.
- Hypothesis to test, not to assume: these are songbook-style transcriptions from a different engraver than the GP-exported lessons, with different barline construction. Record the PDF producer string and page count of each (counts and labels only).

## Goal

Find why bar boxes are not built for these nine and, if a SCALE-RELATIVE rule can build them without loosening a gate, build them; otherwise stop and report the finding with measurements, as PDF-GROUP-01 did. Anything ambiguous stays refused with a located reason.

## Acceptance

1. **Measure first.** A table for the nine and for the converting lessons: producer, pages, systems, string and staff spacing, the barline strokes found per system with their lengths as multiples of the string spacing, and which strokes each of the six rejection diagnostics discards. Counts and distances only. Say which rejection is wrong (a true barline discarded) and which is right (a stem or other vertical stroke).
2. **The rule**, if one exists: staff-relative, with no new absolute point limit, that keeps true barlines and still rejects stems, ledger lines and other vertical strokes. Two separate staves must never be joined.
3. **Each of the nine ends in one of two stated states:** converts with every written bar passing the existing bar checks, or stays refused with a located reason naming the geometry that fails (counts and distances only). Report each file's before and after: status, bars written and refused, refusal codes.
4. **Ex 2 Hands Up**: if it passes grouping, report its later refusals by code and compare every written bar with the reference through the oracle. A refusal-code change is reported separately from a conversion. No claim of correctness for files without a reference: say so.
5. **Real-source tests that bite.** Private-corpus tests assert the changed behaviour on real sources from more than one producer (the nine and at least two converting lessons), with negative controls taken from real sources (a stem, a ledger line and a vertical stroke between two staves in real files must NOT become barlines), and a mutant keeping the old rejection fails those tests on the real files. Tests are CI-safe: create `<repo>/work` before using it and prove them on a clean `git archive` copy. Public synthetic fixtures are supplementary non-domain infrastructure only, with a stated rationale, and carry no acceptance weight.
6. **Nothing that worked may change.** Measure on the whole private set at base and at head: every file that converts today keeps a byte-identical GPIF, and every refusal keeps its code except the files reported. The before and after table covers every converting and every refused file.
7. No change to the `build_ir.py` gating sets.
8. `python -m pytest` (exact-head CI), export-schema, validate-ir, `scripts/artifact_audit.py` and `git diff --check` pass; list the known Windows baseline failures by ID if they fail locally.

## Rules

- **Domain evidence (AGENT_CONTROL.md):** acceptance rests on genuine approved sources, or reproducible extracts that keep their source provenance and reach the changed seam; general claims need more than one approved corpus input. Synthetic, mocked or generated-notation tests carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity claims; they may supplement non-domain infrastructure only with a stated rationale.
- **Read from the source, or refuse.** Never invent a value, never copy one from a reference `.gp`, never loosen a gate to raise a count (a count is a result, not a target).
- **Scale-relative only:** every new limit is a multiple of the measured string or staff spacing.
- **Stop** if a fix needs changing a gate's meaning rather than its scale, and report what the gate is.
- **Stay inside `allowed_paths`;** if you need another path, stop and report it.
- **Private tests convert under `<repo>/work`** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02.
- Out of scope: the no-score, ascii, hand-written and Books categories (they refuse for their own reasons, and their policy is a maintainer decision). The survey has five other grouping refusals in those categories (one no-score file, the ascii file, the hand-written file and the two tab books): report their status unchanged.
