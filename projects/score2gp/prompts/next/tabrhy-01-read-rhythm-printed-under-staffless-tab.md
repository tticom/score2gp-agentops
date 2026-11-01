# TABRHY-01: Read the rhythm printed under staffless TAB (stems, beams, flags, dots, ties, rests, triplets, whole-note chords)

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/tabrhy-01-read-rhythm-printed-under-staffless-tab`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

Read the rhythm that staffless TAB prints under the strings. Six of the seven no-score PDFs are refused (4 with pdf_only_tab_no_notation_bars, 2 with pdf_only_tab_grouping_unsafe; one converts). The supervisor viewed one of each refusal code: they are Guitar-Pro-style TAB with printed rhythm below the strings, so the durations are READ from it (strategy 2 below), never counted or guessed. The maintainer judged both: both should convert, and for the grouping_unsafe one "the tab grouping safety or resolution needs to be increased until the tab is safely determinable". The maintainer's judgements on the two named fixtures are in the private-fixtures file `fixtures/no-score/MAINTAINER-JUDGEMENTS-2026-11-01.md` (it reaches you as `fixtures/private/MAINTAINER-JUDGEMENTS-2026-11-01.md`); read it first. It is private: never copy its content into the repository, the PR or the handback.

## Reading order (maintainer, 2026-11-01: "it should not guessed until no other reading strategy produces a plausible rhythm")

Try these in order, per bar; the first that gives a plausible rhythm wins. A rhythm is plausible only if the bar's durations total exactly the printed meter's capacity (the rational meter utility) and nothing printed contradicts it.

1. **Printed notation staff**, where one exists: note types win (the existing reader).
2. **Rhythm marks printed under the TAB** (staffless TAB, as Guitar-Pro-style exports print it): stems, beams, flags, augmentation dots, tie arcs, rest glyphs, tuplet brackets with their numbers, and circled stemless chords.
3. **Printed beat-count text** under or over the TAB, where there is any.
4. **Last resort, a labelled guess:** infer the rhythm from the TAB itself (equal column spacing, count of columns). Every such duration is labelled GUESS in the report and in the GP file and is never counted as a read result. This is the separate authority item TABONLY-01 and is not part of this task.

If no strategy gives a plausible rhythm, the bar is refused with a located reason, as now.

## Musician knowledge (general; recorded from the maintainer and standard notation practice)

- A chord is the digits stacked on different strings at one horizontal position.
- In TAB-only notation a circle around stemless fret digits marks a whole note (one chord filling a bar in 4/4). The supervisor believes this; the author must show from a real PDF what the circle means before relying on it.
- A stem with no beam and no flag is a quarter note (when the beat unit is a quarter); one beam or one flag is an eighth; two are a sixteenth; a dot adds half the note's value; a bracket with a number groups a tuplet.
- A tie or slur arc between two notes of the same pitch holds the first for the length of both; a note that ends a tie carries on into the next beat.
- A rest glyph is a rest of its printed type.
- Where the printed notes in a bar total less than the meter and nothing else is printed for the remainder, the maintainer reads the remainder as a rest ("a missing rest"). Treat this as an implied rest: write it as a rest, but label it IMPLIED in the report, count it separately from printed rests and never use it to make a bar that otherwise disagrees (too many notes, or a contradicting mark) pass.
- Bends, slides, hammer-ons, pull-offs, vibrato, palm-mute spans, repeat signs and chord names are separate features and are not rhythm.

The same reading order and knowledge are recorded in projects/score2gp/knowledge/tab-rhythm-reading-strategy.md of the governance repository.

## Acceptance

1. Measure first, per no-score PDF (and the ASCII and hand-written ones only to confirm they stay out of scope, IN-02 and IN-03): the refusal code and the exact check that raises it (quote the code); the number of TAB systems and bars found; and per printed rhythm-mark class under the TAB (stems, beams by level, flags, dots, tie or slur arcs, rest glyphs, tuplet brackets and numbers, circled or stemless chords) a count. Counts and codes only in the handback, no private content. For each file say whether it is music the system can read, and for Finger position tips TAB whether it is music at all.
2. Implement reading strategy 2 and the order above: durations only from printed marks; each bar's total must equal the printed meter's capacity (use the NPG-04A rational meter utility, which exists) and a bar whose marks do not add up stays refused with a located reason and its numbers. Show from a real PDF what the circle around stemless digits means before using it. Implied rests (printed notes totalling less than the meter, nothing else printed) are written but labelled IMPLIED in the report and counted separately. No duration is guessed, counted from the number of columns, or taken from horizontal spacing in this task.
3. pdf_only_tab_grouping_unsafe: measure why bars or note groups are unsafe to separate, and raise the grouping resolution (use the stems and beams under the TAB to separate groups) until the TAB is safely determinable; do not loosen or bypass the safety check. A group or bar that the evidence still cannot settle stays refused with a located reason.
4. Held-out check: design and tune only on the two maintainer-judged fixtures, 5 MUST KNOW Pentatonic Licks In Em and Finger position tips TAB. Hold out 7_Grateful_Dead_Melodies (no_notation_bars) and 5_Grateful_Dead_Intros (grouping_unsafe): never use them to design or tune; apply the finished reader to them once and report bar by bar against the printed notation. Where the held-out result disagrees with the printed notation, say so and do not tune on it.
5. Report before and after over the whole private set: bars written (printed rhythm, implied rests, separately), bars refused by code, and every source whose written GPIF changed. Every source that converted before must be byte-identical. There is no reference .gp for these sources: check each newly written bar against the printed notation (note-type counts, rests, ties, tuplets), say that was the check, and label every result NOT independently verified. List which output files the maintainer should open and check. Record which printed features were left unread (bends, slides, vibrato, repeats, chord names).
6. Technique marks are not notes (hard test, real sources only): bends (an arrow or curve with a target number or a label such as FULL, often with the target fret in parentheses), vibrato squiggles, slide lines and hammer-on or pull-off arcs are not rhythm and must never create a note, a fret digit, a rhythm mark or a tie. Measure first and report, as counts only, how many such marks each no-score PDF prints and how the current reader treats them. Then add a test on real approved PDFs (not synthetic fixtures) that asserts, for bars that print a bend, that the bar's note count equals the number of printed noteheads, so a parenthesised bend target is never a second note, and that a vibrato squiggle never becomes a tie. The test must fail on the base where the base misreads them, and the handback names the mutants it rejects: read a parenthesised bend target as a note; read a vibrato squiggle as a tie; read a bend label as a fret digit. If the reader already ignores these marks, the test pins that and the handback says so. The marks themselves stay unread in this task and are listed as left unread.
7. A named mutant (drop the beam and stem reader; drop tie handling; drop the whole-note chord rule; count implied rests as printed) fails a test on a real source; synthetic tests carry no acceptance weight and the handback says so.
8. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
