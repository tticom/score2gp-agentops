# TABGUESS-01: Design and score the spacing model for TAB that prints no rhythm

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/tabguess-01-design-and-score-the-spacing-model`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

The 53 bars refused as note_duration_event_unread / tab_column_without_rhythm_mark and most of the 29 bars refused as bar_without_notation_or_tab_item are TAB that prints no rhythm at all (no stems, beams, flags, notation staff or beat counts), so reading strategies 1 to 3 in knowledge/tab-rhythm-reading-strategy.md produce nothing. The maintainer decided on 2026-10-27 (option B) that a labelled guess is the last strategy, and on 2026-11-01 that rhythm 'should not guessed until no other reading strategy produces a plausible rhythm'. This task designs that last strategy and SCORES it; it does not write guessed bars into any output. The central difficulty is that nothing in these sources can show a guess is right, so score the model on sources where the rhythm is printed and read (strategies 1 and 2 give the truth) by hiding the printed rhythm, then apply it to the no-rhythm sources only as a labelled report.

## Acceptance

1. Measure first and write docs/tabguess-01-spacing-model.md: for each source that prints no rhythm, the number of TAB columns per bar, the column-spacing statistics, and the bars counts by code. Counts only; no private content. Then fix the model on paper before scoring it: what it infers from spacing, how it reaches a bar total equal to the meter, and the label format (GUESS in the report and in any output).
2. Score the model: take the sources whose rhythm is printed and read, hide the printed rhythm, infer from spacing alone, and report per source and in total the share of bars whose inferred rhythm equals the read rhythm, split by meter and by how regular the printed spacing is. Design on some sources and hold out at least two: score them once and do not tune on them. State what accuracy would make a labelled guess worth offering to the maintainer; this is a recommendation for the maintainer's decision, not a promotion.
3. No guessed duration is written to any output, report-as-read or counted as a read result in this task; the only change to src is whatever the scorer needs behind a test hook, and every source stays byte-identical. Reference-less sources are labelled not independently verified.
4. A named mutant (change the spacing rule; drop the meter-total check) fails a test on a real source; synthetic tests carry no acceptance weight and the handback says so.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
