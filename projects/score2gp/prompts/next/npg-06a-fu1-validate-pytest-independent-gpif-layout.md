# NPG-06A-FU1: NPG-06A validation: show the production GPIF layout does not depend on pytest

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001:U13
- **Depends on:** none
- **Branch:** `feat/npg-06a-fu1-validate-pytest-independent-gpif-layout`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Validate, without changing production code, that the earlier removal of the pytest-conditional GPIF layout holds. Rescoped to validation only on the maintainer's word (2026-10-28: 'approved: rescope NPG-06A to validation only'); the explicit legacy layout option and its test migration are NPG-06A-FU2.

## Acceptance

1. Measure first: confirm src/score2gp/gpif.py and gpif_builder.py hold no sys.modules, sys.argv or other pytest detection, quoting the search; list the tests that pick a GPIF layout explicitly (information only, no change).
2. For every converting private source, the GPIF written by the CLI is identical when the same command runs under pytest and outside it, including an output path under pytest's tmp_path; shown in the handback with counts per source. Any difference is a located defect, reported and not fixed here.
3. A regression test is added that fails if layout depends on pytest detection; a named mutant (reintroduce a sys.modules or sys.argv pytest branch) fails it.
4. No production code, existing test or layout option changes; GP8 acceptance output does not change.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
