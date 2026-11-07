# REFUSE-18: Reduce the largest remaining unread-duration class

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/refuse-18-largest-unread-duration-class-after-tsig`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

After TSIG-01 to PERF-02 the whole-set ranking is led by note_duration_event_unread at 88 bars (reader gap), including tab_column_without_rhythm_mark and unclassified_mark_below_strings in the newly routed TAB-only source. Leads, not facts: re-measure on the current runtime and pick by bar count and by whether the symbol is unambiguously musical.

## Acceptance

1. Measure first with the normal CLI over every approved PDF: record per affected bar the located reason (page, system, bar, event, code, cause) and rank the causes by bar count. Counts and codes only in the handback. Classify every refused class as a reader gap, a representation gap or unknown, never as a correct refusal: every approved fixture except the blank No Notes file is real teaching material a human can play from (maintainer, 2026-11-04). A bar the evidence cannot yet settle stays refused with a located reason, never guessed, and is reported as unfinished. Include the shape class of the unread symbol and view the printed page for a sample of every class.
2. Read the largest class that note type plus grouping, or an unambiguously musical symbol, settles; the rest stay refused with their located reasons. No duration is guessed and no spacing or count inference is used.
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
