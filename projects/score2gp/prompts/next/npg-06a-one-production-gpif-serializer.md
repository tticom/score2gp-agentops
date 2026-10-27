# NPG-06A: One production GPIF serializer: remove the pytest-conditional writer branch

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001:U13
- **Depends on:** none
- **Branch:** `feat/npg-06a-one-production-gpif-serializer`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

One production GPIF serializer: remove the pytest-conditional writer branch. Source: authority item NPG-06A. Detail: plans/2026-08-19-native-pdf-to-gp-and-audiveris-retirement.md §16 (NPG-06A). Also the architect's FND-01.

## Acceptance

1. Measure first: describe the branch in gpif.py (around line 149) that chooses a legacy layout when pytest is in sys.modules or any argv, list every test that depends on the legacy layout, and quote the memory note that CLI-subprocess tests are affected.
2. Exactly one production serializer remains, with no dependence on sys.modules or argv; tests that relied on the legacy layout are migrated to the production layout or deleted with a stated reason.
3. The GPIF written by the CLI for every converting private source is identical when run under pytest and outside it, shown in the handback; GP8 acceptance output does not change relative to the production layout before this task.
4. A named mutant (reintroduce a pytest-conditional) fails a test.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
