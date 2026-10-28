# NPG-06A-FU1: NPG-06A follow-up: retire the explicit legacy GPIF layout and migrate the tests bound to it

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001:U13
- **Depends on:** none
- **Branch:** `feat/npg-06a-fu1-retire-explicit-legacy-gpif-layout`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

NPG-06A follow-up: retire the explicit legacy GPIF layout and migrate the tests bound to it. Source: authority item NPG-06A-FU1. Residual of NPG-06A: the author run (2026-10-28) found the sniffing already removed but explicit legacy layout selection and legacy-bound tests still present, so the original acceptance 2 to 4 (one serializer, per-test migration, corpus equivalence, mutant) remain open.

## Acceptance

1. Measure first: the pytest sniffing is already gone (NPG-06A resolved 2026-10-28). Re-locate what remains in src/score2gp/gpif.py and gpif_builder.py: the GpifLayout type with a legacy value, the layout argument of build_gpif (around lines 198-215) and the legacy writers bound by tests/gpif_test_helpers.py; list every test that selects the legacy layout (tests/test_gpif_layout_selection.py and others) and what each one covers.
2. Exactly one production serializer remains with no legacy layout option and no dependence on sys.modules, sys.argv or any pytest detection; every legacy-dependent test is migrated to the production layout with equivalent coverage (each migrated test named in the handback); no test is deleted or skipped. If a legacy-layout consumer outside the tests exists, stop and report it instead of removing the option.
3. The GPIF written by the CLI for every converting private source is identical before and after, and identical when the same command runs under pytest and outside it (including an output path under pytest's tmp_path), shown in the handback; GP8 acceptance output does not change.
4. Two named mutants fail a test: reintroduce a layout switch, and reintroduce a pytest-conditional (sys.modules or sys.argv) branch.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
