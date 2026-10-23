# DUR-02-FU2 (retargeted): A TAB-only source with no notation keeps its bars and writes no notes

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** DUR-02
- **Branch:** `feat/dur-02-fu2-npg03b-floating-asserts-real-refusal`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify `No Notes.pdf` and `no-notes.gp` exist there (category `no-score`) before starting; if either is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Why this task was retargeted

The first author run (2026-10-22) found the named private PDF has notation: fresh DUR-01 records give 3 systems and 8 bars, the route writes all 8 bars (82 events) and refuses none, so no 'no notation' refusal could truthfully be asserted. The maintainer then added a genuine no-notes source to the fixtures and directed (2026-10-23, own words): "I think the output should retain the bars but write no notes". The reference `no-notes.gp` has 9 bars and no beats.

## Goal

Today a source with printed staves but no notation is refused (`pdf_only_tab_no_notation_bars` for the no-score files that have TAB digits). For an empty-bar source such as `No Notes.pdf` the converter must instead keep every printed bar and write no notes. The decision is per source: bars with no TAB digits and no notation become empty bars; bars with TAB digits and no rhythm stay refused, because rhythm comes from note type plus grouping, never from counts or spacing. Find where the refusal is raised, change it only for the empty case, and keep `test_npg03b_floating`'s original numeric checks, updating its refusal assertion with the reason in the handback.

## Acceptance

1. Measure first: convert no-score/No Notes.pdf and every other no-score PDF at current main and list the outcome and cause code of each (counts and codes only); record what test_npg03b_floating calls and which guard it hits today; record the bar and beat counts of the reference no-notes.gp (counts only).
2. A source whose bars are printed but hold no TAB digits and no notation keeps one written bar per printed bar and writes no beats or notes, so its GPIF matches the bar count of no-notes.gp with no invented note, rhythm or rest. The oracle is the PDF's printed bars and the reference's counts, taken independently of the code under test.
3. A source that holds TAB digits but no rhythm stays refused with its located reason: the rhythm cannot be taken from notation, counts or spacing, and no note is invented for it. Every no-score file other than No Notes.pdf keeps its current outcome unless the handback lists the file and reason.
4. test_npg03b_floating keeps every original numeric check and asserts the new behaviour on its source; the reason is stated in the handback. New tests on the real files fail under named mutants (route refuses again; writes a guessed note; drops a bar; refuses with the generic guard), each shown failing.
5. Nothing that worked may change: whole private set measured at base and head, every file and bar written today keeps a byte-identical GPIF unless listed with reason; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant: drop the feature, hard-code the value, invert the condition, restore the old behaviour) and show that mutant failing. A test that only shows the happy path passing is not evidence and must not be added. Acceptance rests on genuine approved sources (the private corpus and its reference `.gp` files, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion. A test that encodes behaviour this task deliberately changes is updated with the reason stated in the handback; every numeric and reference check it had is kept.
- **Nothing that worked may change:** measure the whole private set at base and at head. Every file and bar written today keeps a byte-identical GPIF unless the task says otherwise and the handback lists the file, bar and reason.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only. Private tests convert under `<repo>/work` in a `tempfile.TemporaryDirectory`.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`. Complete the handback with every acceptance item PASS and the evidence for each.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
