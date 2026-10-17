# OMIT-05-FU1: Header and footer templates: reproduce Guitar Pro's default rich-text font sizes as project-owned policy

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** OMIT-05
- **Branch:** `feat/omit-05-fu1-header-footer-font-sizes`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

The minimal header/footer template markup drops Guitar Pro's default rich-text font sizes (for example the 35 pt title), a visible difference in Guitar Pro. Reproduce the default sizes as documented project-owned policy constants with provenance (never read from a reference file during conversion), and extend the oracle to compare them.

## Acceptance

1. Measure first: the font sizes the five reference files carry for each header and footer field, and what the writer emits.
2. The writer emits the documented default sizes from project-owned constants whose provenance is documented in code and docs; no reference file is read during conversion.
3. The independent oracle compares the sizes and a real-source test fails under mutants (drop the sizes; wrong field mapping; read from a reference).
4. Record in the handback that the maintainer's Guitar Pro open test is still required to confirm the visible result (a human check; do not claim it done). Nothing else changes; validation commands pass.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant: drop the feature, hard-code the value, invert the condition, restore the old behaviour) and show that mutant failing. A test that only shows the happy path passing is not evidence and must not be added. Acceptance rests on genuine approved sources (the private corpus and its reference `.gp` files, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion. A test that encodes behaviour this task deliberately changes is updated with the reason stated in the handback; every numeric and reference check it had is kept.
- **Nothing that worked may change:** measure the whole private set at base and at head. Every file and bar written today keeps a byte-identical GPIF unless the task says otherwise and the handback lists the file, bar and reason.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only. Private tests convert under `<repo>/work` in a `tempfile.TemporaryDirectory`.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`. Complete the handback with every acceptance item PASS and the evidence for each.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
