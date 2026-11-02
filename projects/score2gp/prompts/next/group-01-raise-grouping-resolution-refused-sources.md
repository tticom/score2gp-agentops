# GROUP-01: Raise the TAB grouping resolution for sources refused at grouping

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/group-01-raise-grouping-resolution-refused-sources`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

Nine private sources produce no route because they are refused at grouping (pdf_only_tab_grouping_unsafe, ambiguous_bar_assignment), including two that carry a score. REFUSE-02 found these are a grouping problem, not an unread symbol, and TABRHY-01 raised the grouping resolution for staffless TAB only. This task measures the rest. Raise the grouping resolution only where the evidence (staff and TAB line geometry, barlines, digit positions) makes the grouping safely determinable; do not loosen or bypass the safety check. The maintainer's standing view: the grouping safety or resolution needs to be increased until the TAB is safely determinable.

## Acceptance

1. Measure first, per grouping-refused source: the refusal code, the exact check that raises it (quote the code), the systems and bars found, and the warning that blocks it (barline, line spacing, digit-interrupted lines, bar assignment). Counts and codes only in the handback. Say for each source whether it is music the system can read.
2. Pick the largest cause the page evidence can settle safely and fix the resolution, not the threshold: a group or bar that the evidence still cannot settle stays refused with a located reason. Do not loosen or bypass a safety check. Design and tune on some sources and hold out at least two: apply the finished reader to them once and report bar by bar against the printed notation, without tuning on them.
3. Report before and after over the whole private set: bars written, bars refused by code, sources newly producing a route, and every source whose written GPIF changed. Every source that converted before must be byte-identical. Label each newly written bar not independently verified unless a reference exists, and list which output files the maintainer should open and check.
4. A named mutant (drop the new resolution rule) fails a test on a real source; synthetic tests carry no acceptance weight and the handback says so.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
