# SHORT-01A: Close the REQ-0005 silent gaps that contradict fail-closed rules (G5, G7, G8)

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0005
- **Depends on:** none
- **Branch:** `feat/short-01a-close-fail-closed-silent-gaps`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

First slice of the accepted REQ-0005 (explained shortfalls): the three silent gaps that its research map (projects/score2gp/research/2026-09-26-res-req-0005-explained-shortfalls/01-current-state-map.md, section 'silent gaps named') says already contradict existing fail-closed rules, as measured at product SHA 3af1925 in September: G7 inferred rhythm reported as `success`, G8 synthesised rests carried at confidence 1.0, and G5 `generate-sidecar` crashing without a reason code. They may already be fixed or changed since; re-measure each on the current runtime.

## Acceptance

1. Measure first: for each of G5, G7 and G8, reproduce or refute it on the current runtime with the normal CLI over the approved sources that exercise it, quoting the code path and the exact output (status, exit code, reason code). Counts and codes only in the handback. State for each whether it still occurs.
2. For each gap that still occurs, close it without loosening any fail-closed rule: a located reason code for the crash (G5); a result that is not `success` and says the rhythm was inferred, with the located bars, for inferred rhythm (G7); no synthesised rest carried at full confidence, with the confidence and provenance recorded honestly (G8). Anything that cannot be settled stays refused with a located reason. No duration is guessed.
3. Over the whole private set report before and after: bars written, bars refused by code, the status and exit code of every run whose status changes, and every source whose written GPIF changed. No source that converted may lose a correct bar and no bar may be written with a wrong duration. Newly changed statuses must be explained, not just counted.
4. A named mutant per fixed gap (restore the old behaviour) fails a test on a real source; synthetic tests carry no acceptance weight and the handback says so. If a gap no longer occurs, say so and add a guard test only if a real source can exercise it.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
