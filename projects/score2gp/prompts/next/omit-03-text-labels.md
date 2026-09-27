# OMIT-03: Text labels: carry printed text onto the beat it annotates

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** DUR-02
- **Branch:** `feat/omit-03-text-labels`

This comes from the maintainer's review of the first real output (DUR-02, Lesson-3.gp, 2026-09-27): "It looks good, the best one so far but I already see omissions rather than failures."

## Goal

Carry printed text such as 'Example 1 - [0:13]' onto the beat it annotates, as GPIF `FreeText`. The reference Lesson-3.gp has 12 labels; the output has none. RES-REQ-0005 found 1,318 text candidates dropped silently from PDF-only builds (gap G16).

## Acceptance

1. Text candidates above the staff are classified. Section and example labels and other free text are distinguished from technique text (H, P, sl.), chord symbols, tempo marks, titles and page furniture, which have their own handling.
2. Each free-text label is attached to the beat it annotates by a stated, tested rule, citing its source text span. Anything that cannot be placed unambiguously is recorded with a located reason.
3. Lesson-3.gp carries the 12 reference labels on the reference beats, with the text equal. Lessons 4-7 are compared, and every difference is reported.
4. Dropped text candidates are counted by reason in the diagnostics, never silently discarded.

## Rules

These are the project's standing rules for every omission task:
- **Read from the source, or refuse.** Every value comes from the source PDF. If the product cannot read a value unambiguously, it records a located diagnostic and writes nothing for it. It never invents a value, and never copies one from the reference `.gp`: the reference is only for comparing after conversion.
- **Measure the fix against the maintainer's real files.** The acceptance is the private reference `Lesson-3.gp` (then Lessons 4-7 where the feature occurs), compared through the independent GPIF reader in `tests/test_dur_02_oracle.py`, which you extend for this feature. Report coverage and every difference.
- **Protect what already works.** Nothing may regress in the DUR-02 comparison: durations, rests, strings, frets and techniques in every written bar.
- **Test first, and prove the tests bite.** Write a failing test first, and add a committed synthetic public fixture for the feature. Run a mutation check: removing the feature's reading must fail the tests.
- **Pass the product checklist:** pytest, export-schema (a schema change must be intended and documented, with contract versions bumped), validate-ir, `scripts/artifact_audit.py` and `git diff --check`. The exact-head CI run is the full-suite result. List any local Windows baseline failures by ID.
- **Keep private material out of the repo.** Commit no private musical content, note or fret data, or coordinates. Real-source outputs stay under `work/`.
