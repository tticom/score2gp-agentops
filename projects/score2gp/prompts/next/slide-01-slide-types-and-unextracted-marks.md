# SLIDE-01: Slides: write the slide type the source shows, and report slide marks that were not extracted

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001, REQ-0005
- **Depends on:** DUR-02, DUR-03
- **Branch:** `feat/slide-01-slide-types-and-unextracted-marks`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Every slide is written as one fixed type regardless of the source mark (shift, legato, in, out), and a curved slide mark with no extracted candidate (Lesson 5 bars 16 and 17) produces no slide and no warning. Read the type from the source where it is readable, otherwise record why not, and make every unextracted slide mark a located diagnostic: no silent omission.

## Acceptance

1. Measure first: for each approved source with slides, the slide count written, the slide types the reference `.gp` files carry (counts by type) versus what the writer emits, and the slide marks visible on the page that produce no candidate (Lesson 5 bars 16 and 17 are the known cases).
2. The writer emits the type the PDF evidence supports for each slide; where the evidence cannot decide the type, the slide technique is NOT written (uncertain input is never guessed, REQ-0001; REQ-0005 section 2): the mark is refused with a located reason code, bar and run status, and a real-source ambiguous case shows a final GPIF with no guessed slide. A mutant that injects a default type while keeping the warning must fail that test.
3. An unextracted slide mark yields a located diagnostic (code, bar, system) in the conversion report; the diagnostic code exists in `src`, tests and docs (the earlier handback named a code that existed nowhere).
4. Real-source tests on Lessons 3 to 7 assert slide types and the diagnostics at the changed seam and fail under mutants (always Flags 2; drop the diagnostic; swap in and out); other techniques byte-identical.
5. Validation commands pass; handback complete.

## Notes

Do not copy slide types from reference files into code: derive them from the drawn mark.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant: drop the feature, hard-code the value, invert the condition, restore the old behaviour) and show that mutant failing. A test that only shows the happy path passing is not evidence and must not be added. Acceptance rests on genuine approved sources (the private corpus and its reference `.gp` files, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion. A test that encodes behaviour this task deliberately changes is updated with the reason stated in the handback; every numeric and reference check it had is kept.
- **Nothing that worked may change:** measure the whole private set at base and at head. Every file and bar written today keeps a byte-identical GPIF unless the task says otherwise and the handback lists the file, bar and reason.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only. Private tests convert under `<repo>/work` in a `tempfile.TemporaryDirectory`.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`. Complete the handback with every acceptance item PASS and the evidence for each.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
