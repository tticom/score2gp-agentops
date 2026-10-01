# CFW-04: Read grace notes, small stemless heads and wave glyphs, so more of Can't Find My Way Home is written

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** DUR-03
- **Branch:** `feat/cfw-04-grace-small-heads`

This comes from a read-only governance diagnosis (2026-10-01, main 3cb2079; full report `C:\Users\niall\src\score2gp-workspace\launchers\cfw-diagnosis.md`, model-written: treat every number as a lead and re-measure it). It supersedes CFW-01 and CFW-02.

## What governance measured (leads to VERIFY)

Converting "Can't Find My Way Home" with `--pdf-only-tab --time-signature 4/4` writes 9 of 21 bars; 12 are refused (5 `bar_total_mismatch`, 5 `note_duration_event_unread`, 2 `notehead_digit_count_mismatch`).
- **Small noteheads.** 16 heads are about 0.88 staff spaces wide against 1.18 for the other 260. Eight of them carry a stem and flag: grace notes (bars 1, 3, 5, 7, 9, 15 (two), 17). The duration reader treats them as ordinary eighths, so bars sum to 9/2. The reference stores each as a 32nd note tagged `GraceNotes OnBeat`. The other eight are stemless small heads (bend-target or ghost heads with no TAB digit and no beat of their own in the reference): they produce the `filled_notehead_without_stem` events.
- **Wave glyphs.** A vibrato squiggle in bar 11 gives 7 `rest_glyph_unidentified` events and an arpeggio fragment in bar 18 gives 1 `symbol_unclassified`; all lie outside the five-line staff band.
- **Stay refused.** Bars 3 and 9 are the legitimate tied-chord case (two heads, one printed digit) and bar 6 has a cross (dead-note) head the reader does not recognise: both stay refused, with located reasons. A scratch experiment (no repo change) that excluded graces from the bar total and dropped the stemless small heads and the outside-staff glyphs wrote 18 of 21 bars with rhythm, string and fret identical to the reference, none wrong, and changed nothing on Lessons 3-7, Gloria or Boring Scale.
- Writing a grace note needs IR support for a zero-duration grace (`ticks_for_quarters` in `src/score2gp/pdf_tab_measure_timing.py` raises on 0).

## Goal

Read the grace notes, stemless small heads and non-note glyphs from the source and write the bars they unblock, with the grace written the way the reference writes it. Whatever still cannot be read unambiguously stays refused with a located reason.

## Acceptance

1. **Measure first.** Re-measure the head sizes, the grace and stemless-head classification and the wave glyphs on Can't Find My Way Home and on every other PDF that has a small flagged head (the diagnosis mentions Just-Practice, Melodic Expressions and EXACT System, which have no reference): counts and distances only.
2. **A measured rule, stated.** Define how a small head is classified (grace with stem and flag, versus stemless small head), tied to the staff's own scale (staff-space relative, not absolute points), and how a grace is attached to the beat it ornaments. A non-note glyph outside the staff band is recorded with a located reason and ignored for the bar total, only if it cannot be a note or rest.
3. **Grace writing.** Write the grace the way the reference does (`GraceNotes OnBeat`, a 32nd note), through the IR and the writer, with a contract version bump if the IR or schema changes (`export-schema`, `validate-ir`, old 0.1.0 and 0.1.1 files still load, compact provenance from MEM-01 kept).
4. **Can't Find My Way Home against the reference.** Through the independent GPIF reader in `tests/test_dur_02_oracle.py`, compare every written bar with the reference (note count, string, fret, written value, grace tag): the diagnosis expects 18 of 21; report the real number, with a located reason for every bar still refused. **A bar paired wrongly is worse than a refused bar**: there must be none.
5. **Nothing that worked may change.** Lessons 3-7 and every PDF whose output does not involve a small head are byte-identical (compare the full GPIF XML); for the PDFs that do have small heads and no reference, report every changed bar and the evidence it is right, and refuse where you cannot tell.
6. **Tests that bite.** Public synthetic fixtures engraved like the real source (a grace note with stem and flag before a beat, a stemless small head, a vibrato squiggle outside the staff, a dotted bar with a cross head that must stay refused); they fail at the base and pass now. Mutants (no grace handling, grace counted in the bar total, stemless heads kept, absolute-point threshold) must each fail a test. Tests must be CI-safe: create `<repo>/work` before using it and prove them on a clean `git archive` copy without `work/`.

## Rules

- **Read from the source, or refuse.** Never invent a value, never copy one from the reference `.gp`, never loosen a gate to raise a count. The reference is only for comparing after conversion.
- **Protect what already works:** DUR-02/03 bars, OMIT-01/02/03/05, LAYOUT-01, MEM-01, Key, DoubleBar.
- **Stay inside `allowed_paths`;** if you need another path (an existing test that asserts the old behaviour), stop and report it so governance can amend scope.
- **Private tests convert under `<repo>/work`** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path`. Commit no private content; counts, codes and distances only.
- **Pass the product checklist:** pytest, export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`; exact-head CI is the full-suite result. List the two known Windows baseline failures by ID if they fail locally.

## Scope amendment (2026-10-01)

The first authoring run (branch `feat/cfw-04-grace-small-heads`, `febfc66`) writes 18 of 21 Can't Find My Way Home bars and stopped at two full-suite failures. `tests/test_omit_04_private.py` is added to `allowed_paths` **only** to update `test_other_reference_arpeggios_have_located_refusals`, which asserts that the output has no arpeggios; four now appear on newly written bars. Verify each of the four against the source and the reference, then change the assertion to expect exactly those, with located refusals for the rest. Do not suppress or loosen anything to keep the old count. The second failure, `tests/test_pdf_tab_route_support.py::test_synthetic_records_have_the_readers_shape`, is fixed inside `note_duration.py` by emitting the `grace` field only on grace records. Rerun the whole suite and the product checklist, then hand back.
