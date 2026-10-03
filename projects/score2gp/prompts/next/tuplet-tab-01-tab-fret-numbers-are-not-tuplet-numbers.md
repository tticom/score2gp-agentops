# TUPLET-TAB-01: TAB fret numbers are not tuplet numbers

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** SCALE-01 (merged)
- **Branch:** `feat/tuplet-tab-01-fret-numbers-not-tuplets`

This comes from a read-only investigation of bars 6-8 of Melodic Soloing Masterclass (`docs/investigations/melodic-bars-6-8.md` in `tticom/score2gp-vector-parser`, model-written: treat every number as a lead and re-measure it). The Melodic file is in the private corpus under `fixtures/private`; never commit private content, report counts and codes only. Main now includes #478, #479 and #480 (SCALE-01).

## What the investigation measured (leads to VERIFY)

- In Melodic Soloing Masterclass bar 7 (1-based; `bar_index` 6) no tuplet is drawn. The reference bar 7 has 16 sixteenth notes, no tuplet, 4 hammer-on/pull-off pairs and 3 slides.
- `note_duration._read_staff` takes every DIGITS text inside `_zone(staff)` (`ZONE_REACH_SPACES` 8.0, scale-relative) as a tuplet-number candidate.
- On this page `find_staves` detects no six-line TAB staff for the system, so the zone is not clamped at the TAB top. The reason is undetermined and out of scope, but record what you find.
- System 3's zone ends at 2072.0 pt while the top TAB line is at 2065.8 pt, so TAB fret numbers lie 0.37 staff spaces inside the zone. Four of them (x 467, 527, 587, 646) align within 0.5 space of events 3-6; `_read_tuplets` finds no bracket or beam group, so they stay unassociated and the four events get `tuplet_number_unassociated`, which refuses the whole bar.

## Goal

A digit text lying on or between TAB staff lines (or otherwise belonging to the TAB row) is never a tuplet-number candidate. A genuine printed tuplet number, with its bracket or beam group, must still be found. Never invent values, never loosen a gate to raise a count.

## Acceptance

1. **Measure first.** On Melodic system 3 and bar 7: the zone limits, the TAB line positions, the digit texts inside the zone and which belong to the TAB row (counts and distances only); confirm or correct the diagnosis and record why `find_staves` finds no TAB staff there.
2. **The rule.** A digit text on or between TAB staff lines, or otherwise belonging to the TAB row, is excluded as a tuplet-number candidate, by a stated staff-space-relative rule that does not depend on the file. Anything ambiguous stays a candidate or stays refused with a located reason.
3. **Melodic against the reference.** Melodic converts with bar 7 holding 16 sixteenths and the bar check `match` on 8 of 8 bars. Notes matched to the reference by string and fret per bar were 66 of 82 before and 82 of 82 are expected after; bar 7's strings and frets are unproven until run, so report the measured result honestly through the independent GPIF reader. A bar paired wrongly is worse than a refused bar.
4. **Tests that bite.** A new public synthetic test that puts a fret number inside the zone and shows it is not a tuplet number (fails at base, passes now); a test keeping a real printed tuplet number (with its bracket or beam group) found; a mutant with the rule removed fails a test. Existing tuplet tests pass. Tests are CI-safe: create `<repo>/work` before using it and prove them on a clean `git archive` copy without `work/`.
5. **Nothing that worked may change.** The 13 converting files and all other private-corpus files are unchanged in status, and every file that already converts produces byte-identical GPIF at base and head (counts only); report any file whose refusal code changes separately.
6. `python -m pytest` (exact-head CI), export-schema, validate-ir, `scripts/artifact_audit.py` and `git diff --check` pass; list the known Windows baseline failures by ID if they fail locally.

## Rules

- **Read from the source, or refuse.** Never invent a value, never copy one from the reference `.gp`, never loosen a gate to raise a count.
- **Stay inside `allowed_paths`:** `src/score2gp/notation_omr/note_duration.py`, `tests/test_note_duration*.py`, `tests/test_tuplet_tab_01_*.py`, `tests/fixtures/pdf/tuplet_tab_01/**`, `docs/design/**`; plus `tests/test_npg03b_floating.py` ONLY if its assertion about Melodic's refused bar must change to the new behaviour (update only that stale assertion; weaken nothing, and keep the three TAB-only controls at 0 notation staves). If you need another path, stop and report it so governance can amend scope.
- **Stop** on a stop condition and report; in particular if the fix would need a change to a gate's meaning rather than its scale.
- **Private tests convert under `<repo>/work`** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path`. Commit no private content; counts, codes and distances only.
- **Protect what already works:** DUR-02/03, OMIT-01/02/03/05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01.
