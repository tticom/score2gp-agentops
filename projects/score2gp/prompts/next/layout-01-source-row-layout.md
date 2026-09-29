# LAYOUT-01: Reproduce the source's bars-per-row layout

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** OMIT-02
- **Branch:** `feat/layout-01-source-row-layout`

This comes from the maintainer's request on 2026-09-29: "could the exact format be copied or reproduced from the original to the output? ... can we produce the same number of bars on each row?"

## Goal

Write each track's `SystemsLayout` (bars per row) and `SystemsDefautLayout` from the systems read in the source PDF, so that Guitar Pro breaks rows where the source does. The writer currently emits a fixed 3 bars per row.

Governance measurement (2026-09-29, main 2e8c00b):
- For Lessons 3-7, the systems found by `read_note_durations` equal the reference `<SystemsLayout>` exactly (23, 29, 14, 34 and 25 rows).
- Every reference DoubleBar ends a row, with 0 exceptions. Some rows end without one, so the rows come from the systems and not from barline kind.

## Acceptance

1. Each track's `SystemsLayout` lists the source's bars per row, in order, and sums to the written bar count. For Lessons 3-7 it equals the reference exactly.
2. When the systems are unknown or disagree with the written bars (refused or merged bars, multi-page gaps), the writer falls back to the documented default and records a located diagnostic. It never guesses a row split.
3. The independent comparator (`tests/test_dur_02_oracle.py`) is extended to read and compare `SystemsLayout`. A public PDF-to-GPIF test covers uneven rows, and a private-corpus test asserts equality for Lessons 3-7.
4. No other GPIF element changes; the output matches the reference's element shape.
5. No regression in DUR-02 (durations, rests, strings, frets, techniques), OMIT-01 Key or OMIT-02 DoubleBar in any written bar of Lessons 3-7.

## Rules

- **Read from the source, or refuse.** Rows come from the PDF systems, never from the reference `.gp`.
- **Test first, and prove the tests bite.** Mutants that must fail: a fixed row length; rows from DoubleBar positions only; an off-by-one row split.
- **Private tests convert under `<repo>/work`,** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path`. `gpif.build_gpif` switches to a legacy layout when "pytest" is in argv or paths (OMIT-02-FU4).
- **Pass the product checklist:** pytest (exact-head CI), export-schema, validate-ir, `scripts/artifact_audit.py` and `git diff --check`.
- **Keep private material out of the repo.** Commit counts only.
