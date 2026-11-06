# PERF-02: Reduce retained inspection data so a long source fits the existing resource budget

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/perf-02-reduce-retained-inspection-data`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

NOROUTE-01 found that a 34-page notation-and-TAB source stops with pdf_resource_inspection_page_nodes_exceeded (2,060,433 nodes against the 2,000,000 PERF-01 budget, at page index 10). PERF-01 is a protected resource limit and is not touched: the fix is to retain less inspection data, not to raise or bypass the budget. Leads, not facts: re-measure which structures hold the nodes (per-page drawing, glyph and text objects kept after they are no longer needed) and how much each contributes. This is also a first measured step toward the Rust bottleneck list.

## Acceptance

1. Measure first: for the failing source and two others of different size, the page nodes retained per page, by structure, and the peak memory and time of the inspection stage. Counts and numbers only. State which structures are needed after their page is processed and which can be released or summarised.
2. Release or summarise the retained structures that no later stage needs, without changing any output: every source that converts must keep a byte-identical inner Content/score.gpif, the budget value and its check stay exactly as they are, and the failing source must now fit under the unchanged budget or the handback says what still holds it. Report conversion time and peak memory before and after over the whole set.
3. A named mutant (retain the released structure again) fails a test on a real source; synthetic tests carry no acceptance weight and the handback says so.
4. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
