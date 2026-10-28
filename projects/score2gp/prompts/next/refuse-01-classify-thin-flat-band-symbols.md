# REFUSE-01: Classify the thin flat band symbols that leave bars refused as note_duration_event_unread

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/refuse-01-classify-thin-flat-band-symbols`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Classify the thin flat band symbols that leave bars refused as note_duration_event_unread. Source: authority item REFUSE-01. Measured 2026-10-27 on the latest survey: across 9 partly refused PDFs, 799 symbols were unclassified (symbol_unclassified) and 751 of them share one shape (constant-thickness band, about 3.9 by 0.7 staff spaces, drawn). Measure first what they are on real approved sources, then classify or explicitly refuse them with a located reason. Goal: fewer refused bars with no false success. Acceptance must use real approved sources, not synthetic ones.

## Acceptance

1. Measure first, on the approved real PDFs only: across the PDFs that currently refuse bars with note_duration_event_unread, count the unread symbols whose reason is symbol_unclassified and group them by shape_class; the 2026-10-27 survey saw 799 such symbols in 9 PDFs, 751 of them constant-thickness bands about 3.9 by 0.7 staff spaces (drawn). State what the bands are, with located examples (page, system, bar) and a rendered crop for each kind kept in the handback only if it contains no private content beyond counts and codes.
2. Handle each kind that is a real musical symbol by classifying it (so its bar can be read) and each kind that is not by recording it as ignored for a stated reason; any kind that cannot be settled stays unread and refuses with a located reason. Nothing is invented and no duration is guessed.
3. On the whole private set, report before and after: bars written, bars refused by code, and every source whose written GPIF changed; no source that converted may lose a correct bar and no bar may be written with a wrong duration (check every newly written bar against its reference where one exists, otherwise against the printed notation, and say which). Reference-less sources are labelled as not independently verified.
4. A named mutant (drop one new rule) fails a test; synthetic tests carry no acceptance weight and the handback says so.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
