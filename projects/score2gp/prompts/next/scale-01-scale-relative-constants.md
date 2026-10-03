# SCALE-01: Make the staff and barline detection constants relative to the staff space (Melodic Soloing Masterclass reads no notation bars)

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** DUR-03
- **Branch:** `feat/scale-01-scale-relative-constants`

This comes from a read-only governance diagnosis (2026-10-01, main 3cb2079; report `C:\Users\niall\src\score2gp-workspace\launchers\cfw-diagnosis.md`, model-written: treat every number as a lead and re-measure it).

## What governance measured (leads to VERIFY)

"Melodic Soloing Masterclass" is refused up front as `pdf_only_tab_no_notation_bars`: no notation staff is found and 82 TAB digits stay unplaced. Its page is 2480 x 3508 pt with a staff space of about 17.7 pt, far larger than the other sources. Two constants are in absolute points and fail on that scale:
- `find_staves` in `src/score2gp/notation_omr/note_duration.py` has a 15 pt step cap;
- `extract_page_symbols` accepts rectangles only up to 1.5 / 1.0 pt thick, so its barlines stay as glyphs.

With both raised in a scratch process (no repo change): 8 bars were found (the reference has 8), 4 were written and identical to the reference, none wrong, 4 refused. Raising the limits in points would break rest blocks on normal pages: **the fix must be staff-space relative**, derived from the page's own measured staff space, and leave normal pages (staff space about 6-7 pt) exactly as they are.

## Goal

Replace the absolute-point limits by limits derived from the measured staff space, so large-scale pages find their staves and barlines, and write the bars that then pair unambiguously with their TAB digits. Anything that cannot be read unambiguously stays refused with a located reason.

## Acceptance

1. **Measure first.** On all 30 mounted PDFs, record the page size, the measured staff space and which absolute-point constants in the staff and symbol detection code (search the whole of `src/score2gp/notation_omr/` and `src/score2gp/pdf_*.py` for point-valued thresholds, not only the two named) are binding; counts and distances only.
2. **Staff-space relative rule.** Express each binding threshold as a multiple of the measured staff space, justified by measurement on the sources where it currently works (the multiples must reproduce today's behaviour on normal pages exactly) and on Melodic Soloing. No constant fitted to one file.
3. **Melodic Soloing against the reference.** Through the independent GPIF reader, compare every written bar with the reference `.gp` (note count, string, fret, written value): the diagnosis expects 8 bars found and 4 written correctly; report the real numbers, with a located reason for each refused bar. **A bar paired wrongly is worse than a refused bar.**
4. **Nothing that worked may change.** Every PDF whose staff space is in the normal range produces a byte-identical GPIF (compare the full XML for all 30 PDFs at base and head; report any change with its evidence). TAB-only PDFs (12 Bar Blues, 5 Must Know, Finger position tips) must stay refused as `pdf_only_tab_no_notation_bars`.
5. **Tests that bite.** A public synthetic fixture engraved at the large scale (staff space about 17-18 pt, thick barline rectangles) that fails at the base and passes now, and a normal-scale fixture proving no change. Mutants (restore an absolute threshold; scale a threshold wrongly) must each fail a test. Tests must be CI-safe: create `<repo>/work` before using it and prove them on a clean `git archive` copy without `work/`.

## Rules

- **Read from the source, or refuse.** Never invent a value, never copy one from the reference `.gp`, never loosen a gate to raise a count.
- **Protect what already works:** DUR-02/03 bars, OMIT-01/02/03/05, LAYOUT-01, MEM-01, CFW-04 if merged.
- **Stay inside `allowed_paths`;** if you need another path, stop and report it so governance can amend scope.
- **Private tests convert under `<repo>/work`** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path`. Commit no private content; counts, codes and distances only.
- **Pass the product checklist:** pytest, export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`; exact-head CI is the full-suite result. List the two known Windows baseline failures by ID if they fail locally.

## Scope amendment (governance, 2026-10-03, authority revision 104)

The first author run found that the staff-space-relative change makes Melodic Soloing Masterclass locate notation staves (0 to 8 located bars, 7 written bars identical to the reference), which makes `tests/test_npg03b_floating.py::test_private_acceptance_melodic` fail on its stale assertion `records["systems"] == []`. That file is now in `allowed_paths`, for one purpose only:

- Replace that one stale assertion with an assertion of the new located notation behaviour (counts only, converted under `<repo>/work` in a `tempfile.TemporaryDirectory`, nothing private committed).
- Do not weaken, delete or skip any other assertion in the file. The three TAB-only controls (12 Bar Blues, 5 Must Know, Finger position tips) must still assert 0 notation staves.
- Touch no other part of that file.
