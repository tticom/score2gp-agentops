# TECH-02: Bends the reference files have, checked by the independent oracle

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** TECH-01 (merged)
- **Branch:** `feat/tech-02-bends-against-references`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below, and their sibling `.gp` references, exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime.

## Why this task exists

The maintainer (2026-11-19) said `Melodic Soloing Masterclass.pdf` and `Ex 2 Hands Up.pdf` have string bends and `.gp` reference files, and that both are small and scored. The independent oracle (`tests/test_dur_02_oracle.py`, which does not import score2gp) compares slides, vibrato, hammer-ons, palm mute and let-ring, but not bends, so a bend written by the product, right or wrong, is currently unchecked. TECH-01 settled slides the same way and merged. Lessons 3 to 7 and Bebop contain a release but no string bend (maintainer, 2026-11-19), so they cannot judge bends.

## Goal

1. **Oracle first.** Add bends to the independent oracle: read the bend properties of each note from the `.gp` (origin, destination, middle values and offsets as the file stores them) and compare them as a field of its own, located by bar and event, like the existing technique fields. The oracle must not import score2gp. Tests for the oracle fail on a mutated bend (the project's mutant style in the oracle tests).
2. **Measure.** For every source that has a `.gp` reference, list each bend the reference has that the output lacks, writes differently, or writes where the reference has none (source, bar, event, string, expected, actual) and say which printed mark the page shows. Counts, positions and codes only.
3. **Design on `Melodic Soloing Masterclass.pdf` only.** Make the product write the reference's bends from the printed page evidence (never from the reference). A bend the page does not evidence stays unwritten and located.
4. **Holdout, named in advance and not tuned on: `Ex 2 Hands Up.pdf`.** Apply the finished reader once and report each bend against the reference. The gate needs at least one reference bend newly matching in the holdout. If none does, report goal 3 blocked, not complete; the gate is not waived and no other holdout may be substituted after the result is seen. Goals 1 and 2 stand on their own and are delivered either way, labelled as oracle and measurement only.
5. List any other reference difference you see as located findings with counts. Do not fix them here.

## Acceptance

1. The oracle compares bends, with tests that fail on a changed bend value, a dropped bend and an extra bend, shown failing against named mutants. Existing oracle tests pass unchanged.
2. Measure first, as in Goal 2, over every source with a reference.
3. If goal 3 is unblocked: the reader writes the reference's bends on the design source and at least one more on the holdout, compared with the oracle, with the mechanism stated. Otherwise the handback says blocked for goal 3.
4. Report before and after over the whole private set: bars written, bars refused by code, and every source whose written GPIF changed. Every source that converted before keeps a byte-identical inner Content/score.gpif unless a named bend became correct, which the handback lists with the oracle result; list every bend added where no reference can check it, as a stated risk.
5. A named mutant (drop the new rule) fails a test on a real source; synthetic tests carry no acceptance weight and the handback says so. Never copy a bend value or position from the reference into code.
6. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** run the full `python -m pytest`; if it is too slow to finish, say exactly how far it got and run the test files for every module you touched plus the oracle tests to completion, and report both. Also export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Handback format:** `handback-evidence.json` validation_runs entries use `command`, `status` (PASS or FAIL), `exit_code`, `passed`, `failed`, `errors`, `skipped`, `xfailed`, `deselected`; acceptance entries use `criterion` (the text), `status`, `command`, `observed`, `oracle`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, SLIDE-01, TECH-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
