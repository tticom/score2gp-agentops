# PDFG-01: Mixing Lead & Rhythm pt1 and PARANOID refused with pdf_only_tab_grouping_unsafe: find the cause, fix it or locate it

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** UNREAD-02, PDF-GROUP-02
- **Branch:** `feat/pdfg-01-refused-new-fixtures`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Two of the three newest private fixtures are refused wholesale with `pdf_only_tab_grouping_unsafe`, so a user converting either gets nothing. Find which grouping condition fires and why, fix the cause where the PDF evidence is unambiguous, and otherwise narrow the refusal to the bars that are actually unsafe.

## Acceptance

1. Measure first: for each of the two files, the page, system and TAB group counts, which grouping check fires, on how many systems/bars, and the count of bars that would convert if the refusal were narrowed to the unsafe groups (counts and labels only).
2. The cause of each distinct failure is named with the function and the evidence it uses; a fix reads the grouping from the PDF evidence (staff geometry, barlines, brackets) with no per-file constant.
3. After the change each file either writes the bars whose grouping is unambiguous, equal to the independent comparator where a readable reference `.gp` exists (Mixing Lead & Rhythm has a reference whose GPIF payload may be opaque to the stdlib reader: if so, state exactly why and use only PDF-observable facts for that file, claiming no fidelity), or stays refused with a located code per unsafe group.
4. Real-source tests on both files assert the changed seam and fail under mutants (restore the blanket refusal; accept an unsafe group; merge two groups); a third approved source with grouping that already works is shown byte-identical.
5. Nothing that worked may change on the whole private set; validation commands pass; handback complete.

## Notes

Files: `Mixing Lead & Rhythm pt1.pdf`, `PARANOID - BLACK SABBATH.pdf` (names as in fixtures `MANIFEST.md`). PDF-GROUP-02 introduced the grouping safety check; read its design note and tests first and keep their guarantees.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant: drop the feature, hard-code the value, invert the condition, restore the old behaviour) and show that mutant failing. A test that only shows the happy path passing is not evidence and must not be added. Acceptance rests on genuine approved sources (the private corpus and its reference `.gp` files, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion. A test that encodes behaviour this task deliberately changes is updated with the reason stated in the handback; every numeric and reference check it had is kept.
- **Nothing that worked may change:** measure the whole private set at base and at head. Every file and bar written today keeps a byte-identical GPIF unless the task says otherwise and the handback lists the file, bar and reason.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only. Private tests convert under `<repo>/work` in a `tempfile.TemporaryDirectory`.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`. Complete the handback with every acceptance item PASS and the evidence for each.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
