# MEM-04: Bring the longest source's report and conversion time inside the existing allowances

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/mem-04-report-size-and-time-for-the-longest-source`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

PERF-02 let the 34-page source convert but it takes about 780 s and 1.8 GB, and its report is about 40.8 MB, 1.7 MB over the existing size allowance (tests/test_mem_02_report.py is a strict xfail for it). The allowance and the PERF-01 budget are protected and are not touched: the fix is to write less report and spend less time. Leads, not facts: re-measure by stage.

## Acceptance

1. Measure first: for the 34-page source and two others of different size, the time and peak memory by stage and the report bytes by section. Counts and numbers only.
2. Reduce the report bytes and the slowest stage's time without changing any output: every converting source keeps a byte-identical inner Content/score.gpif, the size allowance and budget stay exactly as they are, and the xfail is removed only because the report now fits. Report the before and after of time, memory and report size over the whole set; list candidates for a Rust replacement by measured share.
3. A named mutant (restore the removed report content) fails a test on a real source; synthetic tests carry no acceptance weight and the handback says so.
4. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
