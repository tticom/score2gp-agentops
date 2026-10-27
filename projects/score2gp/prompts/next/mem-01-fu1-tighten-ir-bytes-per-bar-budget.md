# MEM-01-FU1: Tighten the MEM-01 IR bytes-per-bar budget

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** MEM-01
- **Branch:** `feat/mem-01-fu1-tighten-ir-bytes-per-bar-budget`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Tighten the MEM-01 IR bytes-per-bar budget. Source: authority item MEM-01-FU1. Non-blocking follow-up 1 from tticomgov-code's approving review of tticom/score2gp#472 (MEM-01) at caf71f3. The budget bound in tests/test_mem_01_budget.py is 20,000 bytes per bar, but the compact IR measures about 9,040 bytes per bar on the public fixture, so a re-inflation of about 2x would not fail the test. Tighten the bound (or add per-fixture bounds) when more public engraved fixtures exist; keep the negative control that restores the full raw payload and must fail.

## Acceptance

1. Measure first: record the IR bytes per bar on every public fixture and the current bound (20,000) in tests/test_mem_01_budget.py.
2. The bound (or per-fixture bounds) is tightened to within about 25 percent above the measured value, so a 2x re-inflation fails; shown failing under a named mutant. The negative control that restores the full raw payload stays and must fail.
3. Tests only; no production change.
4. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
