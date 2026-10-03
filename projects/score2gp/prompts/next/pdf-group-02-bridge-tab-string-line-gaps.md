# PDF-GROUP-02: Bridge TAB string-line gaps at full-chord digit columns

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** SCALE-01, TUPLET-TAB-01 (both merged)
- **Branch:** `feat/pdf-group-02-bridge-string-line-gaps`

This comes from a read-only investigation of 2026-10-03 (`docs/investigations/dense-licks-refusals.md`, written in the investigation worktree of `tticom/score2gp-vector-parser` and not yet on its main; model-written: treat every number as a lead and re-measure it). It is a NEW gate, not C1, C2 or C3 of the stopped PDF-GROUP-01. Main now includes #478, #479, #480 (SCALE-01) and #481 (TUPLET-TAB-01). Never commit private content; report counts, codes and distances only.

**Private fixtures.** `A7-Blues-Lick.pdf` and `E_Chord_Lick_Chord.pdf` are in `C:\Users\niall\src\score2gp-workspace\score2gp-private-fixtures\fixtures\private` (37 PDFs there now). Earlier author runs saw only 30 mounted PDFs. **Before starting, verify that your `fixtures/private` contains both files** (the launcher copies the private directory into your worktree at the start of the run); if either is missing, stop and say exactly what is missing. Do not copy private content into any repository.

## What the investigation measured (leads to VERIFY)

- **A7-Blues-Lick** (real file name; 4/4 declared with `--pdf-only-tab --time-signature 4/4`) refuses `pdf_only_tab_grouping_unsafe` (`ambiguous_bar_assignment`) at layout-gating. Each TAB string line is drawn in pieces with a 7.3 pt gap wherever a fret digit sits. At the two six-string chord columns (x about 168 and 371) all six strings are gapped at the same x.
- `merge_collinear_horizontal_segments` (pass 2) in `src/score2gp/pdf_geometry.py` merges gaps over 5.0 pt only if another line 2 to 45 pt away spans the gap; at a six-string chord none does. The staff splits into a partial-line TAB group plus a 5-line phantom group; two system topologies result; the TAB-height barline rectangles and the joint left stroke are discarded (`primitive_to_system = None`). Only 3 of 4 bars get boxes and 15 of 46 fret digits are unassigned. The constants 5.0, 45.0 and 120.0 are absolute points.
- A scratch change of `gap_len <= 5.0` to 8.0 converted A7 fully (4 bars, 31 events, 46 of 46 digits placed, every bar sums to 3840 ticks), but there is **no regression evidence** for that change: do not copy it, derive a scale-relative rule.
- **E_Chord_Lick_Chord** has the same cause in systems 2 and 4 (a full six-string chord gap at x 434 to 441). With the scratch patch it passes grouping, but then 7 of 16 bars refuse at the note-type route (`bar_total_mismatch` 3, `notehead_digit_count_mismatch` 3, `notation_note_without_tab_digit` 1), so it moves to a later refusal; the investigation also noticed the run still exits 0 with the refused bars written with 0 ticks, a separate question that you must report, not fix.
- Page geometry on both: TAB string spacing 9.66 pt, notation staff space 6.44 pt, gaps of 7.2 to 7.3 pt (about 0.75 of string spacing).

## Goal

A TAB staff whose six strings are all broken at the same x by digits is detected as ONE staff, so its barlines and the joint left stroke are owned by the system. Use a SCALE-RELATIVE rule (about 0.8 of the string spacing, aligned across strings or flanked by a digit). Never invent values, never loosen a gate to raise a count; anything ambiguous stays refused with a located reason.

## Acceptance

1. **Measure first.** On A7-Blues-Lick and E_Chord_Lick_Chord: string spacing, the gap lengths and where they fall, which gaps the current rule bridges and which it does not, and the effect on the system topology (counts and distances only). Confirm or correct the diagnosis.
2. **The rule.** A gap in a TAB string line is bridged when it is no longer than a stated multiple of the string spacing (about 0.8) and is aligned across the strings or flanked by a digit; the rule is staff-space-relative with no fixed point value for the new limit. Two separate staves on one line must NOT be merged.
3. **A7-Blues-Lick** converts from the CLI (with `--pdf-only-tab --time-signature 4/4`) with 4 bars and 46 of 46 digits placed. Report whether the pitches match what the TAB implies; **no reference `.gp` exists for it, and you must say so** rather than claim a match.
4. **E_Chord_Lick_Chord** passes layout-gating; report its later refusals by code and count. A refusal-code change is reported separately from a conversion.
5. **Tests that bite.** Public synthetic fixtures: a full-chord gap case that fails at base and passes now; a negative fixture for two staves on one line (must NOT merge); a stroke-ownership test (the TAB-height barline rectangles and joint left stroke are owned by the system). A mutant keeping the absolute 5.0 pt limit fails a test. Tests are CI-safe: create `<repo>/work` before using it and prove them on a clean `git archive` copy without `work/`.
6. **Nothing that worked may change.** Report the exact number of files that convert at base (the previous task measured 12 on the 30 mounted PDFs; measure on the full private set now) and compare each: all must produce byte-identical GPIF at head. Every refusal keeps its code except files explicitly reported. Other files with fragmented string lines may change status, so the before/after table must cover every converting and every refused file (counts and labels only).
7. No change to the `build_ir.py` gating sets.
8. `python -m pytest` (exact-head CI), export-schema, validate-ir, `scripts/artifact_audit.py` and `git diff --check` pass; list the known Windows baseline failures by ID if they fail locally (the previous run recorded 14).

## Rules

- **Read from the source, or refuse.** Never invent a value, never copy one from a reference `.gp`, never loosen a gate to raise a count.
- **Scale-relative only:** every new limit is a multiple of the measured string or staff spacing.
- **Stay inside `allowed_paths`:** `src/score2gp/pdf_geometry.py`, `tests/test_pdf*.py`, `tests/test_pdf_group_02_*.py`, `tests/fixtures/pdf/pdf_group_02/**`, `docs/design/**`. Not `build_ir.py`. If you need another path, stop and report it so governance can amend scope.
- **Stop** if a fix needs changing a gate's meaning rather than its scale, and report what the gate is.
- **Private tests convert under `<repo>/work`** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path`. Commit no private content; counts, codes and distances only.
- **Protect what already works:** DUR-02/03, OMIT-01/02/03/05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01.
