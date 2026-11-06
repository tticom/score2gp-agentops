# RASTER-00: Scope the scanned and hand-drawn sources that need raster reading

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/raster-00-scope-the-scanned-and-hand-drawn-sources`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

NOROUTE-01 found three approved sources that are images, not vector pages: two scanned books (177 and 105 pages, notation and TAB staves, 0 vector drawings and 1 image per page) and a one-page hand-drawn source. They are real teaching material and the largest unread share of the corpus. Reading them needs raster recognition, which is the territory of the REC recognition items and DEC-01 (still undecided), so this task scopes and measures; it does not build the recogniser. Leads, not facts: re-measure.

## Acceptance

1. Measure first and write docs/raster-00-scoping.md: for each of the three sources, pages, image resolution, whether the notation and TAB staves can be located at all by the existing raster code (the repository already has raster diagnostics and Audiveris-based paths: list exactly what exists and what each does today), and the share of staves found. Counts and located reasons only; no private content.
2. Recommend the smallest honest first slice, measured on the one-page hand-drawn source and one page of each scanned book: which stage fails first (staff location, TAB digit reading, rhythm), how far a staff and digit read gets, and what each stage would cost to own in Python against replacing Audiveris. State the dependencies on DEC-01 and the REC items. No source's output changes in this task.
3. Every source stays byte-identical; only docs and a test hook for the scoring may change. Reference-less results are labelled not independently verified.
4. A named mutant (drop the staff-location measurement) fails a test on a real source; synthetic tests carry no acceptance weight and the handback says so.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
