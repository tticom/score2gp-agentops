# REFUSE-20: Reduce the next-largest remaining refused-bar class

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/refuse-20-next-refused-class-after-refuse-19`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

After REFUSE-19, re-rank every refused bar over the whole private set and take the largest remaining reader or representation class that the printed page settles and that REFUSE-19 did not address. Leads, not facts: re-measure on the current runtime.

## Acceptance

1. Measure first with the normal CLI over every approved PDF: record per affected bar the located reason (page, system, bar, event, code, cause) and rank the causes by bar count. Counts and codes only in the handback. Classify every refused class as a reader gap, a representation gap or unknown, never as a correct refusal: every approved fixture except the blank No Notes file is real teaching material a human can play from (maintainer, 2026-11-04). A bar the evidence cannot yet settle stays refused with a located reason, never guessed, and is reported as unfinished. Name the class REFUSE-19 addressed and show it is excluded or reduced in the ranking. Maintainer decision (2026-11-11, real session turn, "apply the same exclusion to REFUSE-20", after choosing "Exclude, measure at source level"): a source that produces no bar inventory at all (the two scanned books, the hand-drawn page and the ASCII-TAB source with no barlines or rhythm) is not required to have per-bar located reasons for the ranking; measure each such source at source level (refusal code and located cause), list it in the handback as unfinished outstanding work (reader or representation gap, never a correct refusal), and keep it out of the bar-count ranking. Every source that does produce a bar inventory is still measured bar by bar.
2. Read the largest remaining class that the page evidence settles; the rest stay refused with located reasons. Design on some sources and hold out at least one, applying the finished reader to it once and reporting bar by bar against the printed page. Maintainer decision (2026-11-12, real session turn: chose "Target next-largest class"): the largest class, TAB columns with no printed rhythm mark (tab_column_without_rhythm_mark, 82 bars at the last measurement), is recorded in the handback as unfinished outstanding work (reader gap, owned by the TAB-rhythm tasks; never a correct refusal, never guessed) and is not required to be read here; where a bar in it prints a rhythm mark or a notation staff the page settles, read it. Read the largest remaining class that the page evidence settles, with a positive separate-source holdout (a holdout source on which the reader writes at least one bar), bar-by-bar against the printed page.
3. Report before and after over the whole private set: bars written, bars refused by code, and every source whose written GPIF changed. Every source that converted before must keep a byte-identical inner Content/score.gpif unless a refused bar became written, which the handback lists. Check each newly written bar against its reference where a readable one exists, otherwise against the printed page, and say which. Reference-less sources are labelled not independently verified.
4. A named mutant (drop the new rule) fails a test on a real source; synthetic tests carry no acceptance weight and the handback says so.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
