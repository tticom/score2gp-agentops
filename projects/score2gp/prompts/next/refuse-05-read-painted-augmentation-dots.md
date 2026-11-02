# REFUSE-05: Read augmentation dots painted in the page but absent from the reader's inputs

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/refuse-05-read-painted-augmentation-dots`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

Read the augmentation dot that is painted in the page but absent from the drawings, text characters and font outlines the duration reader uses. REFUSE-04 (merged) found this is the largest suspected reader gap behind the short bar totals: in at least two sources a dotted rest or dotted eighth is painted, the reader counts no dot, the bar totals short (bar_total_mismatch, 12 bars, 10 short) and the following tied bar cascades into notation_note_without_tab_digit (29 bars, 10 of them cascades). Leads, not facts: re-measure on the current runtime. Read the dot from the rendered page (raster or font level) only where it is unambiguous; never infer it from the bar total.

## Acceptance

1. Measure first with the normal CLI over every approved PDF: for each short bar_total_mismatch bar and each cascade, state whether a painted dot exists on the printed page (view the page) and which of the reader's inputs lacks it. Counts and codes only in the handback. State how many of the short bars a dot explains.
2. Implement a dot read from the page itself (raster or font outline) that is attached to exactly one note or rest by position and size, and never from the bar total (the total is the check, not the evidence). A dot that cannot be attached to exactly one note stays unread and the bar stays refused with its located reason. No loosening of the total check.
3. Report before and after over the whole private set: bars written, bars refused by code, and every source whose written GPIF changed. No source that converted may lose a correct bar and no bar may be written with a wrong duration; check each newly written bar against its reference where a readable one exists, otherwise against the printed page, and say which. Reference-less sources are labelled not independently verified.
4. A named mutant (drop the dot reader; attach the dot to the wrong note; take the dot from the bar total) fails a test on a real source; synthetic tests carry no acceptance weight and the handback says so.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
