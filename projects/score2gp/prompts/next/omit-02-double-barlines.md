# OMIT-02: Double barlines: detect section-ending double barlines and write them

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** DUR-02
- **Branch:** `feat/omit-02-double-barlines`

This comes from the maintainer's review of the first real output (DUR-02, Lesson-3.gp, 2026-09-27): "It looks good, the best one so far but I already see omissions rather than failures."

## Goal

Detect double barlines in the notation or TAB staves and write GPIF `DoubleBar` on the master bar they close. The reference Lesson-3.gp has 11, at bars 3, 7, 13, 18, 25, 28, 34, 40, 49, 53 and 59; the output has none.

## Acceptance

1. Double barlines are distinguished from single barlines, repeat barlines (which already have their own meaning under REQ-0001, recognising bar ends and their meanings) and final barlines. The barline topology and painted-contour primitives from L3-01 are reused.
2. Each recognised double barline sets DoubleBar on the master bar it closes, citing its source strokes.
3. Lesson-3.gp has DoubleBar at exactly the 11 reference bars. Lessons 4-7 and Ex 2 Hands Up are compared, and every difference is reported.
4. A barline whose kind cannot be decided is recorded with a located reason, never promoted or demoted by guess.

## Rules

These are the project's standing rules for every omission task:
- **Read from the source, or refuse.** Every value comes from the source PDF. If the product cannot read a value unambiguously, it records a located diagnostic and writes nothing for it. It never invents a value, and never copies one from the reference `.gp`: the reference is only for comparing after conversion.
- **Measure the fix against the maintainer's real files.** The acceptance is the private reference `Lesson-3.gp` (then Lessons 4-7 where the feature occurs), compared through the independent GPIF reader in `tests/test_dur_02_oracle.py`, which you extend for this feature. Report coverage and every difference.
- **Protect what already works.** Nothing may regress in the DUR-02 comparison: durations, rests, strings, frets and techniques in every written bar.
- **Test first, and prove the tests bite.** Write a failing test first, and add a committed synthetic public fixture for the feature. Run a mutation check: removing the feature's reading must fail the tests.
- **Pass the product checklist:** pytest, export-schema (a schema change must be intended and documented, with contract versions bumped), validate-ir, `scripts/artifact_audit.py` and `git diff --check`. The exact-head CI run is the full-suite result. List any local Windows baseline failures by ID.
- **Keep private material out of the repo.** Commit no private musical content, note or fret data, or coordinates. Real-source outputs stay under `work/`.
