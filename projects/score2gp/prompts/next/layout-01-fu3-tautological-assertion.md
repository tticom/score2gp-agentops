# LAYOUT-01-FU3: Remove the tautological assertion at tests/test_layout_01_public.py:55

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** LAYOUT-01
- **Branch:** `feat/layout-01-fu3-tautological-assertion`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Remove the tautological assertion at tests/test_layout_01_public.py:55. Source: authority item LAYOUT-01-FU3. Non-blocking follow-up 3 from review 5355475879 of tticom/score2gp#471 at b612713. tests/test_layout_01_public.py:55 asserts source_system_bars is None immediately after the test assigned counts, which is already None. The real assertions on the helper return and warning.provenance carry the check, so replace the line with an assertion that can fail, or delete it.

## Acceptance

1. Measure first: confirm the assertion that source_system_bars is None holds trivially after the test assigned counts.
2. Replace it with an assertion that can fail, shown failing under a named mutant; if instead it is deleted, the handback shows a named mutant of the helper return or warning.provenance still failing a remaining assertion. The real assertions on the helper return and warning.provenance stay.
3. No production change.
4. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
