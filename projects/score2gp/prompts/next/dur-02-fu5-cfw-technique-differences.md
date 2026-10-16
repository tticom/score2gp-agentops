# DUR-02-FU5: Can't Find My Way Home: fix or locate the technique differences in written bars (HOPO origin/destination, slide)

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** DUR-02, UNREAD-02
- **Branch:** `feat/dur-02-fu5-cfw-technique-differences`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

In the written bars of Can't Find My Way Home the independent comparator reported 4 HOPO origin, 4 HOPO destination and 1 slide difference against the reference `.gp` (2026-09-28 at OMIT-01 round 3, since then DUR-03, UNREAD-01/02 and others have landed). Re-measure, diagnose each remaining difference against the source and reference, fix the cause or locate it, and add a regression per distinct cause.

## Acceptance

1. Measure first at current main: every technique difference the comparator reports for the written bars (bar index, kind), with counts before and after.
2. Each distinct cause is named and either fixed by reading the evidence on the page (the DUR-02 rules: bounded cross-bar pairs, slide origin, located refusal when ambiguous) or turned into a located refusal of that bar; no value is copied from the reference.
3. A real-source test per distinct cause on Can't Find My Way Home fails under a mutant that restores the old behaviour; a second approved source shows its technique output unchanged.
4. Nothing that worked may change on the whole private set; validation commands pass; handback complete.

## Notes

Related follow-ups you may touch only if the cause is the same: DUR-02-FU1 (within-bar HOPO pairing must lie between the two notes), DUR-02-FU4 (slide type).

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant: drop the feature, hard-code the value, invert the condition, restore the old behaviour) and show that mutant failing. A test that only shows the happy path passing is not evidence and must not be added. Acceptance rests on genuine approved sources (the private corpus and its reference `.gp` files, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion. A test that encodes behaviour this task deliberately changes is updated with the reason stated in the handback; every numeric and reference check it had is kept.
- **Nothing that worked may change:** measure the whole private set at base and at head. Every file and bar written today keeps a byte-identical GPIF unless the task says otherwise and the handback lists the file, bar and reason.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only. Private tests convert under `<repo>/work` in a `tempfile.TemporaryDirectory`.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`. Complete the handback with every acceptance item PASS and the evidence for each.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
