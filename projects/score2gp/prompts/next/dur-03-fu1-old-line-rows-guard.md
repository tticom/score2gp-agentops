# DUR-03-FU1: TAB staff recovery: guard the old_line_rows >= 5 clause with a public fixture and a mutant

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** DUR-03
- **Branch:** `feat/dur-03-fu1-old-line-rows-guard`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

TAB staff recovery: guard the old_line_rows >= 5 clause with a public fixture and a mutant. Source: authority item DUR-03-FU1. Non-blocking follow-up 1 from tticomgov-code's approving review 5376313575 of tticom/score2gp#474 (DUR-03) at 5e52dee. Eight real TAB systems depend on the old_line_rows >= 5 clause in the recovery rule in src/score2gp/pdf.py. No public fixture or mutant exercises it: removing the clause passes all seven public DUR-03 tests, and only the private Lesson 5 bar count guards it. Add a committed synthetic fixture engraved like those systems and a mutant that must fail.

## Acceptance

1. Measure first: find the old_line_rows >= 5 clause in src/score2gp/pdf.py and count the real TAB systems that depend on it (the review found eight).
2. The clause is exercised on approved real sources: a test over the approved private corpus (counts and labels only) fails when the clause is removed or weakened, and names the real TAB systems that depend on it by count. A committed synthetic fixture may supplement this only as non-domain test infrastructure with a stated rationale; it carries no acceptance weight.
3. Named mutants (drop the clause; change 5 to 4 or 6) are each shown failing a test that runs on approved real sources; a mutant no approved real source can reach is reported as not killed, with counts, never claimed killed on a synthetic fixture alone. Real Lesson 5 bar counts are unchanged.
4. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
