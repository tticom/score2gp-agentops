# OMIT-02-FU2: Correct the OMIT-02 design doc: vector repeat dots do occur in the real corpus

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** OMIT-02
- **Branch:** `feat/omit-02-fu2-design-doc-vector-repeat-dots`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Correct the OMIT-02 design doc: vector repeat dots do occur in the real corpus. Source: authority item OMIT-02-FU2. Non-blocking follow-up from tticomgov-code's approving round-2 review 5346382223 of tticom/score2gp#469 (OMIT-02) at d7eef3f. Thread at docs/design/omit-02-double-barlines.md:78 (N2): Gloria.pdf (Guitar Pro 7, macOS Quartz export) draws repeat dots as filled vector drawings with no music font; the reader reads its bars 2, 5 and 8 as repeat-end from two drawing dots each (bar 2 checked visually). The doc calls the vector form unestablished; say it is a real engraving form and cite the count. Documentation only.

## Acceptance

1. Measure first: count the real approved sources whose repeat dots are filled vector drawings with no music font (Gloria.pdf bars 2, 5 and 8 are the lead); counts only.
2. docs/design/omit-02-double-barlines.md states that the vector form is a real engraving form and cites the measured count; documentation only, no source change.
3. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
