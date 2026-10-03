# PDF-GROUP-01: Group TAB systems whose last bar ends in a thin+thick double barline and whose first bar has no accepted left barline, using scale-relative rules

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** PARTIAL-01, SCALE-01 (both merged)
- **Branch:** `feat/pdf-group-01-final-barline-first-bar-boundary`

This comes from a read-only investigation of 2026-10-03 (private corpus, 31 PDFs, product main `fb9cd49`; report `docs/investigations/unsafe-grouping-root-cause.md` in `tticom/score2gp-vector-parser`, model-written: treat every number as a lead and re-measure it). Files are labelled corpus-NN (NN is the alphabetical position in `fixtures/private`); report counts and labels only, never private content. Main now includes #478, #479 and #480 (SCALE-01); the absolute-point constants elsewhere in staff and bar detection may still bite on other pages.

## What the investigation measured (leads to VERIFY)

13 of 31 files refuse with `pdf_only_tab_grouping_unsafe`; 9 of those fail at bar box construction.

- **C1 (confirmed on 8 systems, files 03 04 05 07 08 14 15 28).** In the last system of a page the final double barline is a thin stroke at the staff end plus a thick stroke (2.4 pt wide) centred 3.4 pt = 0.57 staff spaces to its right. The thick stroke is chosen as the bar boundary, but `_TabSystem.grouping_warnings` in `src/score2gp/pdf.py` allows only a fixed 2.0 pt overhang, so it raises `pdf_bar_box_outside_system_bounds`. Patching the tolerance alone converts nothing (03, 15, 28 still refuse, see C2).
- **C2 (located, second gate NOT found; files 03 05 15 28 and any file with the same template).** In every system the first bar has no left boundary: fret digits lie left of the first accepted barline and are refused `pdf_candidate_outside_bar`. The left systemic barline, 2.1 staff spaces left of the staff start, is rejected `pdf_barline_outside_system_bounds` by the fixed 8 pt tolerance in `filter_tab_barline_candidates`. Widening that alone to max(8 pt, 2.5 ss) changed nothing, so a second gate also drops it. **You must find that gate.**
- **C3 (OUT of scope; record it only).** A fixed 30 pt minimum bar width in `grouping_warnings` rejects bars of 3.5 to 4.9 staff spaces (files 10 07 08 04). Do not change it; if your work makes it bite, report it.
- C4 to C8 (joint strokes not reaching the filter, stems on a small staff, raster or text TAB, scanned pages, TAB-only files) are out of scope.

Expected gain is an estimate of **3 to 4 files (03 05 15 28), not 9**; how many convert end to end after the later note-type route is unknown.

## Goal

Group safely the systems described by C1 and C2 using staff-space-relative limits only. Never invent a value, never loosen a gate to raise a count; anything ambiguous stays refused with a located reason.

## Acceptance

1. **Measure first.** For files 03 05 15 28 14 07 08 04, per affected system: the staff space, the overhang of the final thick stroke, the left-barline offset, the digits left of the first accepted barline, and which gate drops the left systemic barline (counts and distances only). Confirm or correct C1 and C2 and name the second C2 gate.
2. **End-of-system tolerance.** A staff-space-relative tolerance at the system end (not 2.0 pt) that takes the thin stroke of a thin+thick pair as the bar boundary; the pair must be recognised by measurement (full height, adjacent, thin plus thick), not by file.
3. **First-bar left boundary.** The first bar's left boundary is taken from the system start (or the rejected left systemic stroke within a staff-space multiple) **only when fret digits exist left of the first accepted barline**; with no such digits no boundary is invented. Limits are staff-space multiples with no fixed point value.
4. **Synthetic public fixtures** for both cases (double-barline overhang of about 0.57 ss; first-bar digits left of the first barline) that fail at the base and pass now, plus controls proving no change (a system with no left digits; a single barline).
5. **Mutants** each fail a test: the absolute 2.0 pt tolerance kept; the absolute 8 pt tolerance kept; a left boundary invented when no digits exist.
6. **Corpus table (counts and labels only).** Exit codes and refusal codes before and after for files 03 05 15 28 14 07 08 04. Report files that newly CONVERT separately from files whose refusal CODE merely changes; a changed code is not progress.
7. **Nothing that worked may change.** The 13 files that convert today produce byte-identical GPIF at base and head (full XML compared); report any change with evidence.
8. **No wrong pairing.** On every newly converting file, compare every written bar with the reference `.gp` where one exists through the independent GPIF reader (note count, string, fret, written value); a bar paired wrongly is worse than a refused bar.
9. **Tests are CI-safe:** create `<repo>/work` before using it and prove them on a clean `git archive` copy without `work/`.
10. `python -m pytest` (exact-head CI), export-schema, validate-ir, `scripts/artifact_audit.py` and `git diff --check` pass; list the known Windows baseline failures by ID if they fail locally.

## Rules

- **Read from the source, or refuse.** Never invent a value, never copy one from the reference `.gp`, never loosen a gate to raise a count.
- **Scale-relative only:** every new limit is a multiple of the measured staff space.
- **Stay inside `allowed_paths`** (`src/score2gp/pdf.py` for `grouping_warnings`, `filter_tab_barline_candidates` and bar box construction; `src/score2gp/pdf_tab_system_partition.py` only if needed; matching tests and fixtures; `docs/design/**`). Not the `build_ir.py` gating sets. If you need another path, stop and report it so governance can amend scope.
- **Stop** if finding the second C2 gate requires changing a gate's meaning rather than its scale, and report what the gate is.
- **Private tests convert under `<repo>/work`** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path`. Commit no private content; counts, codes and distances only.
- **Protect what already works:** DUR-02/03, OMIT-01/02/03/05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01.
