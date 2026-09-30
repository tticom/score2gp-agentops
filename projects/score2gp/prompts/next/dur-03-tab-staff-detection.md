# DUR-03: Detect the TAB staves whose lines are drawn in broken segments (Lesson 6: 52 of 72 bars written empty)

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** DUR-02
- **Branch:** `feat/dur-03-tab-staff-detection`

This comes from the maintainer's review of the latest output (2026-09-30, `latest-output\Lesson-6.gp`): "Lesson-6 output seems to have missed most of the notes although the barline ends and formatting looks good."

## What governance measured (2026-09-30, main fea5149; leads to VERIFY, not facts)

Converting `Lesson-6.pdf` with `--pdf-only-tab --time-signature 4/4` writes 72 bars but **52 of them are empty**: 226 notes against 844 in the reference `Lesson-6.gp`. The report shows `pdf_only_tab_bar_refused` 52 times (`notation_note_without_tab_digit` 51, `notehead_digit_count_mismatch` 1).

A read-only governance diagnosis (full report: `C:\Users\niall\src\score2gp-workspace\launchers\dur03-diagnosis.md`; model-written, so re-measure everything you rely on) found:
- **The assembler thresholds are not the cause.** Where digits reach `pdf_tab_bar_assembler.py`, the signed offset from notehead to digit column is within ±0.06 staff spaces, and 12 combinations of `MATCH_SPACES` (0.5-1.5) and `COLUMN_SPACES` (0.25-0.75) give identical results. Do not retune them.
- **The digits are lost upstream.** In the 51 `notation_note_without_tab_digit` bars zero TAB digits reach the assembler. Only 235 fret candidates exist, in 10 detected tab systems, while 34 systems are drawn. About 600 more numeric candidates lie exactly on the lines of the undetected TAB staves and are tagged `pdf_fret_page_or_legend_number_excluded` and `pdf_candidates_unassigned_to_system`.
- **Likely mechanism:** this lesson uses only strings 1-3, and the drawing splits the top three TAB lines into short segments around each digit. After `merge_collinear_horizontal_segments`, most TAB staves keep only 3-5 of their 6 lines, and staves with 3 or 4 lines yield no tab system (`_detect_tab_systems`, `classify_staff_line_group` in `src/score2gp/pdf.py`). The exact gate that drops a group is NOT yet identified.
- **A scratch experiment (no repo change) fed every numeric text lying on a drawn TAB staff into the unchanged assembler** and matched the reference exactly on 71 of 72 bars of Lesson 6, with no bar paired wrongly. The remaining bar (0-based 26) has chords whose tied later heads are not printed in the TAB: `notehead_digit_count_mismatch`; that refusal is legitimate and must stay.
- Same cause elsewhere: Lesson 4 (2 refused bars) and Lesson 5 (8 of its 9). Lessons 3 and 7 have no refusals and must not change. Can't Find My Way Home and Derek Trucks have DIFFERENT causes (`bar_total_mismatch`, `note_duration_event_unread`): out of scope.

## Goal

Recover the TAB staves that are drawn with broken or partly missing lines, so their fret digits reach the assembler with the right string, system and bar, read from the source. Whatever still cannot be read unambiguously stays refused with a located reason.

## Acceptance

1. **Diagnosis first.** Confirm or correct the mechanism above by measurement on Lessons 4, 5 and 6: per TAB staff, the lines drawn, the lines after merging, and the exact gate that drops the group. Counts and distances only.
2. **A measured detection rule.** Recover the full six-line TAB staff from its segments (or from the staff's own geometry), and assign each digit's string from its position on a recovered line. Never guess a string. A digit that lies on no recovered line, or between two, is recorded with a located reason and not written.
3. **Non-fret numbers stay out.** Tuplet numbers, page numbers, timestamps, bar numbers, legend numbers and the "(" ")" ghost-note markers must not be read as frets. Show counts of these across the corpus before and after.
4. **Lesson 6 against the reference.** Through the independent GPIF reader in `tests/test_dur_02_oracle.py`, compare every written bar with the reference `Lesson-6.gp`: note count, string and fret, and report every difference. The diagnosis expects about 71 of 72 bars; report the real number and give every bar still refused a located reason. **A bar paired wrongly is worse than a refused bar**: there must be none.
5. **No regression.** On Lessons 3 and 7, and on Can't Find My Way Home, the full GPIF is byte-identical. On Lessons 4, 5 and 6, every bar that is written today is byte-identical, and every newly written bar is compared with the reference and reported. The OMIT-03 labels that were refused as `pdf_text_beat_unavailable` should now attach: report the new Lesson 4-7 coverage.
6. **Tests that bite.** Add a committed synthetic public fixture engraved like Lesson 6 (TAB lines split into segments around the digits, using only strings 1-3) that fails at the base and passes now, and a fixture where a digit sits between two lines or on no line that must stay refused. Run a mutation check: reverting the recovery, and recovering a staff from too few lines, must each fail a test.

## Rules

These are the project's standing rules:
- **Read from the source, or refuse.** Every value comes from the source PDF. If the product cannot read a bar unambiguously it records a located diagnostic and writes nothing for it. It never invents a value, never copies one from the reference `.gp`, and never loosens a gate to make a count look better. The reference is only for comparing after conversion.
- **Measure against the maintainer's real files.** The acceptance is the private reference `.gp` files, compared through the independent GPIF reader. Report coverage and every difference honestly.
- **Protect what already works.** Nothing may regress in DUR-02 durations, rests, strings, frets and techniques, or in OMIT-01 Key, OMIT-02 DoubleBar, OMIT-03 FreeText, OMIT-05 metadata, LAYOUT-01 SystemsLayout or the MEM-01 compact IR.
- **Existing tests:** a test that asserts the old detection may change only where the new behaviour is the intended one, and every such edit must be listed in the handback with the reason.
- **Private tests convert under `<repo>/work`,** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path` (`gpif.build_gpif` switches layout when "pytest" appears in a path).
- **Pass the product checklist:** pytest, export-schema, validate-ir, `scripts/artifact_audit.py` and `git diff --check`. The exact-head CI run is the full-suite result. List any local Windows baseline failures by ID.
- **Keep private material out of the repo.** Commit no private musical content, note or fret data, or coordinates; real-source outputs stay under `work/`.
