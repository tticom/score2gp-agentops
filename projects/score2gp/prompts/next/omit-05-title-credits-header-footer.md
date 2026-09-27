# OMIT-05: Title, credits and page header/footer

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** DUR-02
- **Branch:** `feat/omit-05-title-credits-header-footer`

This comes from the maintainer's review of the first real output (DUR-02, Lesson-3.gp, 2026-09-27): "It looks good, the best one so far but I already see omissions rather than failures."

## Goal

Carry the printed title and credits into `Score/Title` and `Score/Music`, and write Guitar Pro's header/footer templates where the reference has them. The output currently writes the invented placeholders 'PDF-Only Inferred Score', 'Unknown Composer' and 'Unknown', and hard-codes all four header/footer fields as empty (`gpif.py`, around lines 412-415).

## Acceptance

1. The printed title and credit on page 1 are read into Score/Title and Score/Music. For Lesson-3.gp these must equal the reference: 'Major Triad Exercises' and 'Rick Beato'. A value that cannot be read is left empty with a located diagnostic.
2. The invented placeholders 'PDF-Only Inferred Score', 'Unknown Composer' and 'Unknown' are removed from every output path.
3. FirstPageHeader, FirstPageFooter and PageFooter carry Guitar Pro's templates as the reference does, for example '%TITLE% %SUBTITLE% %ARTIST% %ALBUM% %WORDS&MUSIC%' and 'Page %page%/%pages%'. PageHeader stays empty, as in the reference. Literal header text is never written.
4. Copyright comes from the source or stays empty.
5. All four header/footer fields and Title/Music equal the reference in Lesson-3.gp. Lessons 4-7 are compared, and every difference is reported.

## Rules

These are the project's standing rules for every omission task:
- **Read from the source, or refuse.** Every value comes from the source PDF. If the product cannot read a value unambiguously, it records a located diagnostic and writes nothing for it. It never invents a value, and never copies one from the reference `.gp`: the reference is only for comparing after conversion.
- **Measure the fix against the maintainer's real files.** The acceptance is the private reference `Lesson-3.gp` (then Lessons 4-7 where the feature occurs), compared through the independent GPIF reader in `tests/test_dur_02_oracle.py`, which you extend for this feature. Report coverage and every difference.
- **Protect what already works.** Nothing may regress in the DUR-02 comparison: durations, rests, strings, frets and techniques in every written bar.
- **Test first, and prove the tests bite.** Write a failing test first, and add a committed synthetic public fixture for the feature. Run a mutation check: removing the feature's reading must fail the tests.
- **Pass the product checklist:** pytest, export-schema (a schema change must be intended and documented, with contract versions bumped), validate-ir, `scripts/artifact_audit.py` and `git diff --check`. The exact-head CI run is the full-suite result. List any local Windows baseline failures by ID.
- **Keep private material out of the repo.** Commit no private musical content, note or fret data, or coordinates. Real-source outputs stay under `work/`.
