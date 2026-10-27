# LAYOUT-01-FU2: Exercise the row-layout fallback end to end from an engraved public source

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** LAYOUT-01
- **Branch:** `feat/layout-01-fu2-row-layout-fallback-end-to-end`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Exercise the row-layout fallback end to end from an engraved public source. Source: authority item LAYOUT-01-FU2. Non-blocking follow-up 2 from review 5355475879 of tticom/score2gp#471 at b612713. The fallback is tested end to end only through the helper plus a hand-set IR through write-gp; no corpus PDF reaches it, and the public fixture covers a single (2,1) split. Add a public PDF whose systems disagree with the written bars (a refused bar mid-system and a page break), and cover multi-track and 12-bars-per-row layouts once Derek Trucks BB King and Ex 2 Hands Up stop refusing in pdf-only mode.

## Acceptance

1. Measure first: confirm which tests reach the row-layout fallback today and that no PDF does.
2. Add a public synthetic PDF whose systems disagree with the written bars (a refused bar mid-system and a page break) and convert it through the CLI to a GP file; a named mutant of the fallback fails the test. Multi-track and 12-bars-per-row layouts are covered only if a public source can show them without refusing; otherwise the handback says so.
3. Synthetic fixtures carry no acceptance claim; the handback states that. No production change unless a located defect is found, which is reported not fixed silently.
4. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
