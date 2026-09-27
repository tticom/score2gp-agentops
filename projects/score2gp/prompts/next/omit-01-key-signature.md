# OMIT-01: Key signature: read it from the notation and write it on every bar

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** DUR-02
- **Branch:** `feat/omit-01-key-signature`

This comes from the maintainer's review of the first real output (DUR-02, Lesson-3.gp, 2026-09-27): "It looks good, the best one so far but I already see omissions rather than failures."

## Goal

Read the key signature from the notation staff and write it as GPIF `Key` (accidental count and mode) on every master bar, including key changes. In the reference Lesson-3.gp every one of the 66 master bars has 1 sharp, G major. The DUR-02 output has no `Key`, so Guitar Pro shows C major and every F sharp carries an accidental.

## Acceptance

1. The key signature is recognised from the accidental glyphs that follow the clef at the start of each system: their count and kind (sharps or flats), and a key change wherever a new signature appears mid-piece. Each value cites its source glyphs.
2. Every master bar carries the key in force. Lesson-3.gp has AccidentalCount 1 and mode Major on all 66 bars, equal to the reference.
3. The mode is Major unless the source shows otherwise. If the mode cannot be read, record that as a located diagnostic; do not guess minor or major from pitch content.
4. An ambiguous or partially read signature is refused with a located reason. It never falls back to C major silently.
5. Lessons 4-7 are compared for Key, and every difference is reported.

## Rules

These are the project's standing rules for every omission task:
- **Read from the source, or refuse.** Every value comes from the source PDF. If the product cannot read a value unambiguously, it records a located diagnostic and writes nothing for it. It never invents a value, and never copies one from the reference `.gp`: the reference is only for comparing after conversion.
- **Measure the fix against the maintainer's real files.** The acceptance is the private reference `Lesson-3.gp` (then Lessons 4-7 where the feature occurs), compared through the independent GPIF reader in `tests/test_dur_02_oracle.py`, which you extend for this feature. Report coverage and every difference.
- **Protect what already works.** Nothing may regress in the DUR-02 comparison: durations, rests, strings, frets and techniques in every written bar.
- **Test first, and prove the tests bite.** Write a failing test first, and add a committed synthetic public fixture for the feature. Run a mutation check: removing the feature's reading must fail the tests.
- **Pass the product checklist:** pytest, export-schema (a schema change must be intended and documented, with contract versions bumped), validate-ir, `scripts/artifact_audit.py` and `git diff --check`. The exact-head CI run is the full-suite result. List any local Windows baseline failures by ID.
- **Keep private material out of the repo.** Commit no private musical content, note or fret data, or coordinates. Real-source outputs stay under `work/`.
