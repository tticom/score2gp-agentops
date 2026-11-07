# TABEXT-03: Group the TAB digits that are printed but never reach a bar

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/tabext-03-digits-printed-but-not-grouped`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

REFUSE-17 found 7 bars (6 in one TAB-only source, 1 in another) that print digits TabRaw holds only as ungrouped text (tab_digits_printed_but_not_grouped), and 23 bars refused as bar_without_notation_or_tab_item where digits are printed that TabRaw never saw. Both are TAB extraction gaps in real teaching material. Leads, not facts: re-measure, view each bar.

## Acceptance

1. Measure first with the normal CLI over every approved PDF: record per affected bar the located reason (page, system, bar, event, code, cause) and rank the causes by bar count. Counts and codes only in the handback. Classify every refused class as a reader gap, a representation gap or unknown, never as a correct refusal: every approved fixture except the blank No Notes file is real teaching material a human can play from (maintainer, 2026-11-04). A bar the evidence cannot yet settle stays refused with a located reason, never guessed, and is reported as unfinished. For each bar say what is printed, which extraction stage drops the digits (text extraction, system geometry, grouping) and quote the code that drops them.
2. Fix the stage that drops readable digits so that they reach their bar with located positions, where the glyph geometry settles it. A digit that is a page number, legend or tempo mark stays excluded. A bar the evidence cannot settle stays refused with a located reason. No safety or overlap guard is loosened.
3. Report before and after over the whole private set: bars written, bars refused by code, and every source whose written GPIF changed. Every source that converted before must keep a byte-identical inner Content/score.gpif unless a refused bar became written, which the handback lists. Check each newly written bar against its reference where a readable one exists, otherwise against the printed page, and say which. Reference-less sources are labelled not independently verified. Report conversion time over the whole set; a new pass must not slow sources that do not need it.
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
