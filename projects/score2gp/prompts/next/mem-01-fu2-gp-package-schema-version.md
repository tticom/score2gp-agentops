# MEM-01-FU2: gp_package.py: stamp GP-imported ScoreIR and ScoreBooklet with SCHEMA_VERSION

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** MEM-01
- **Branch:** `feat/mem-01-fu2-gp-package-schema-version`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

gp_package.py: stamp GP-imported ScoreIR and ScoreBooklet with SCHEMA_VERSION. Source: authority item MEM-01-FU2. Non-blocking follow-up 2 from tticomgov-code's approving review of tticom/score2gp#472 (MEM-01) at caf71f3. src/score2gp/gp_package.py builds GP-imported ScoreIR/ScoreBooklet at three sites with schema_version="0.1.0" while ir.SCHEMA_VERSION is now 0.1.1. Valid, because those objects carry no TabRaw provenance, but inconsistent. Use the constant and add a test; the small memory saving (about 2-4% peak working set) is covered by MEM-02 and MEM-03, not by this item.

## Acceptance

1. Measure first: list the three sites in src/score2gp/gp_package.py that hard-code schema_version 0.1.0 and the current ir.SCHEMA_VERSION.
2. The three sites use the constant; a public test fails if any site is changed back to a literal.
3. Nothing else changes; GP import output otherwise byte-identical.
4. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
