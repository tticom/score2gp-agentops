# TABONLY-01: TAB-only sources: infer rhythm from horizontal spacing as a labelled guess instead of refusing

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/tabonly-01-labelled-spacing-guess-for-tab-only-pdfs`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

TAB-only PDFs (the no-score category) are mostly refused: on the 2026-10-30 survey 6 of 7 refused, 4 with pdf_only_tab_no_notation_bars (12 Bar Blues Solo Guitar Jam, 5 MUST KNOW Pentatonic Licks In Em, 7_Grateful_Dead_Melodies, Finger position tips TAB) and 2 with pdf_only_tab_grouping_unsafe (5_Grateful_Dead_Intros, PARANOID - BLACK SABBATH); No Notes converts (9 bars). Maintainer decision 2026-10-27, option B (infer rhythm from horizontal spacing as a labelled guess instead of refusing), and 2026-11-01: 'The no-score refusals are concerning, keep me informed on how that work proceeds. Possibly I can help determine what the system should do with a given no-score fixture and from that you can infer the rule?'. Rhythm without notation is never a read result: every inferred duration is a labelled guess. ASCII and hand-written TAB are separate input classes (IN-02, IN-03).

## Acceptance

1. Measure first, per no-score PDF (and the ASCII and hand-written ones only to confirm they are out of scope, IN-02 and IN-03): the refusal code and its located reason, the number of TAB systems and bars found, whether bars and note groups can be separated at all, and what horizontal-spacing evidence exists (note-column positions per bar, with the spread). Counts and codes only in the handback, no private content. Say which files are not music at all (for example a finger-position diagram) and must stay refused with a plain reason.
2. Where bars and columns can be located, write the bar with durations inferred from horizontal spacing under one stated model (state the model, its tolerances and what makes it refuse a bar), and mark every such bar as a GUESS both in the conversion report and inside the GP file (a text annotation per bar). Guessed durations are never counted as read results, never mixed into the read-bar totals, and real note-type reading always wins wherever notation exists. A bar whose spacing is ambiguous stays refused with a located reason; no duration is invented to fill a bar, and no spacing or count inference is used outside the TAB-only path.
3. Where bars or groups cannot be separated (pdf_only_tab_grouping_unsafe), measure why and say whether spacing can safely help; if it cannot, they stay refused with a clearer reason and the handback says so. Do not loosen the grouping safety check to get more bars.
4. Held-out check, required before any result is described as more than a guess: before measuring any spacing, choose and record which no-score PDFs are held out (at least one per refusal code, so at least two) and never use them to design or tune the model. Decide the spacing model, its tolerances and the guess label format on the remaining files and state all three in the handback before applying the model to the held-out files, then apply it once and report the outcome. The maintainer has offered to judge named fixtures: where the maintainer's judgement of a held-out file is available it is the oracle and is quoted in the handback; otherwise the held-out result is labelled NOT independently verified and no accuracy claim is made. A model that only reproduces the files it was built on does not satisfy this item.
5. Across the whole private set report before and after: bars written (read), bars written (guessed, separately), bars refused by code, and every source whose written GPIF changed. Every source that converted before must be byte-identical, and the guessed-bar count must be zero outside the no-score category. There is no reference for these sources: label every result NOT independently verified and make no accuracy claim. The maintainer will judge named fixtures separately, so the handback lists, for each no-score PDF, what a reader should open and look at; it does not assert the rhythm is right.
6. A named mutant (drop the GUESS label from the report, and separately from the GP file; infer durations on a source that has notation) fails a test; synthetic tests carry no acceptance weight and the handback says so.
7. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
