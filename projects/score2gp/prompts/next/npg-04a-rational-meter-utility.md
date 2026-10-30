# NPG-04A: One rational meter utility replacing fixed 4/4/3840 capacity

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001:U06
- **Depends on:** none
- **Branch:** `feat/npg-04a-rational-meter-utility`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

Replace the fixed 4/4, 3840-tick bar capacity with one rational meter utility driven by printed meter evidence, so 12/8, 6/8, 3/4 and other printed meters are read, not forced. Evidence: two private sources print 12/8 and the survey harness forced 4/4 and refused them with time_signature_conflict; this is the backlog item NPG-04A (plans/2026-08-19-native-pdf-to-gp-and-audiveris-retirement.md section 16), which also absorbs RHY-03 and the Lesson 5 tempo-mismatch candidate.

## Acceptance

1. Measure first: list every place in src/score2gp that assumes 4/4 or the 3840-tick capacity (search and quote), and for each approved PDF the printed meter, tempo and key evidence the pipeline can read versus what it uses; report counts per source. Re-locate, do not assume.
2. Introduce one rational meter utility (numerator, denominator, ticks per bar derived from them) and route every bar-capacity use through it; a printed meter wins over a parameter default, and a conflict between printed meter and a parameter is a located refusal, not a silent choice.
3. Over the whole private set report before and after: bars written, bars refused by code (time_signature_conflict in particular) and every source whose written GPIF changed. Bars in 4/4 sources must be byte-identical before and after; newly readable non-4/4 bars are checked against the printed notation or a readable reference, and the check named. Reference-less sources are labelled not independently verified.
4. A named mutant (hardcode 4/4 or 3840 again in one use) fails a test; synthetic tests carry no acceptance weight and the handback says so.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
