# OMIT-04: Arpeggio marks: detect rolled-chord marks and write them

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** DUR-02
- **Branch:** `feat/omit-04-arpeggio-marks`

This comes from the maintainer's review of the first real output (DUR-02, Lesson-3.gp, 2026-09-27): "It looks good, the best one so far but I already see omissions rather than failures."

## Goal

Detect the vertical wavy arpeggio (rolled-chord) mark beside a chord and write GPIF `Arpeggio` on that beat. The reference Lesson-3.gp has 2; the output has none.

## Acceptance

1. The arpeggio mark is recognised as a vertical wavy line spanning a chord's notes on the notation or TAB staff, with its direction (up or down) where an arrow shows it. It cites its source strokes.
2. Each recognised mark sets Arpeggio on its chord's beat. Lesson-3.gp has the 2 reference arpeggios on the reference beats, with the direction equal.
3. A wavy mark that cannot be tied to one chord unambiguously is recorded with a located reason.
4. Lessons 4-7 are compared, and every difference is reported.

## Rules

These are the project's standing rules for every omission task:
- **Read from the source, or refuse.** Every value comes from the source PDF. If the product cannot read a value unambiguously, it records a located diagnostic and writes nothing for it. It never invents a value, and never copies one from the reference `.gp`: the reference is only for comparing after conversion.
- **Measure the fix against the maintainer's real files.** The acceptance is the private reference `Lesson-3.gp` (then Lessons 4-7 where the feature occurs), compared through the independent GPIF reader in `tests/test_dur_02_oracle.py`, which you extend for this feature. Report coverage and every difference.
- **Protect what already works.** Nothing may regress in the DUR-02 comparison: durations, rests, strings, frets and techniques in every written bar.
- **Test first, and prove the tests bite.** Write a failing test first, and add a committed synthetic public fixture for the feature. Run a mutation check: removing the feature's reading must fail the tests.
- **Pass the product checklist:** pytest, export-schema (a schema change must be intended and documented, with contract versions bumped), validate-ir, `scripts/artifact_audit.py` and `git diff --check`. The exact-head CI run is the full-suite result. List any local Windows baseline failures by ID.
- **Keep private material out of the repo.** Commit no private musical content, note or fret data, or coordinates. Real-source outputs stay under `work/`.
