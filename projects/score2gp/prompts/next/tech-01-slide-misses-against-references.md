# TECH-01: Slides the reference files have and the product does not write

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/tech-01-slide-misses-against-references`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below, and their sibling `.gp` references, exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime.

## Why this task exists

REFUSE-24 to 27 and CASCADE-01 all ended blocked: the refused-bar causes left are a long tail with no reference to verify against. This task changes the objective to something the references can settle. The maintainer (2026-11-19) pointed at two small scored sources that have a `.gp` reference: `Melodic Soloing Masterclass.pdf` and `Ex 2 Hands Up.pdf`. Converted today they write every bar, yet differ from their references. The independent oracle (`tests/test_dur_02_oracle.py`, which does not import score2gp) compares slides, vibrato, hammer-ons, palm mute and let-ring, but not bends.

Lead from a fresh comparison at product `16414f9` (re-measure): slide differences against the reference in `Melodic Soloing Masterclass` (6: the reference has slides, the output has none), `Can't Find My Way Home` (3), `Bebop Licks in Am` (2), `Ex 2 Hands Up` (1) and `Lesson-5` (1). A slide reader already exists (`src/score2gp/pdf_slide_marks.py`, SLIDE-01), so the question is why these slides are not read.

## Goal

1. Measure first: for every source that has a `.gp` reference, list each slide the reference has that the output lacks or writes differently (source, bar, event, string, fret, expected flag, actual), and say which printed mark the page shows for it. Counts, positions and codes only.
2. Design on `Melodic Soloing Masterclass.pdf` only. Find why its slides are not read and make the reader write them as the reference does, from the printed page evidence (never from the reference).
3. Holdout sources, named in advance and not tuned on: `Can't Find My Way Home`, `Bebop Licks in Am` and `Ex 2 Hands Up`. Apply the finished reader once and report each slide against the reference. The gate needs at least one reference slide newly matching in a holdout source. If none does, report the task blocked, not complete; the gate is not waived and no other holdout may be substituted after the result is seen.
4. List any other reference difference you see (vibrato, repeat count, grace position, tie, double bar) as located findings with counts. Do not fix them in this task.

## Acceptance

1. Measure first, as in Goal 1, over every source with a reference, using the oracle.
2. The reader writes the reference's slides on the design source, and at least one more on a holdout source, compared with the oracle, with the mechanism stated.
3. Report before and after over the whole private set: bars written, bars refused by code, and every source whose written GPIF changed. Every source that converted before keeps a byte-identical inner Content/score.gpif unless a named slide became correct, which the handback lists with the oracle result. Because references exist, newly written slides are checked against them (not just the printed page); say so.
4. A named mutant (drop the new rule) fails a test on a real source; synthetic tests carry no acceptance weight and the handback says so. Never copy a slide type or position from the reference into code.
5. Nothing that worked may change (Lesson-5's slide must not get worse); validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** run the full `python -m pytest`; if it is too slow to finish, say exactly how far it got and run the test files for every module you touched plus the oracle tests to completion, and report both. Also export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, SLIDE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
