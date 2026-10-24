# OMIT-03-FU1: OMIT-03 label rules: kill the surviving margin mutants on approved real sources, or record which cannot be reached

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** OMIT-03
- **Branch:** `feat/omit-03-fu1-label-margin-mutants`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

OMIT-03 label rules: kill the surviving margin mutants on approved real sources, or record which cannot be reached. Source: authority item OMIT-03-FU1. Non-blocking follow-up 1 from tticomgov-code's approving re-review 5365611424 of tticom/score2gp#473 (OMIT-03) at 51f8f05. Mutants that relax the bar or system uniqueness check (!= 1 to < 1), the two-point tie margin (to 0.5 pt) and the status == "read" event filter survive both the public and the private tests. Show each mutant failing a test that runs on approved real sources; where no approved real source reaches the margin or overlap, record the mutant as not killed, with counts. Synthetic margin or overlap fixtures may supplement only as non-domain test infrastructure and carry no acceptance weight.

## Acceptance

1. Measure first: reproduce the surviving mutants (bar or system uniqueness check != 1 to < 1; two-point tie margin to 0.5 pt; status == 'read' event filter removed) against the public and private tests.
2. Each named mutant is shown failing a test that runs on approved real sources. Where no approved real source reaches the margin or the overlap, the handback says so with counts and records that mutant as a residual that is not killed; synthetic margin or overlap fixtures may be added only as non-domain test infrastructure with a stated rationale and carry no acceptance weight.
3. No production behaviour changes; label output on the real corpus is identical before and after.
4. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
