# REFUSE-03: Measure and reduce alignment and total-mismatch bar refusals

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/refuse-03-alignment-and-total-mismatch-refusals`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

Measure and reduce the refused bars that REFUSE-02 does not cover. On the 43-PDF baseline the refusals by code were (leads, re-measure): notation_note_without_tab_digit 25, bar_total_mismatch 18, bar_without_notation_event 15, notehead_digit_count_mismatch 11, mixed_percussive_tie_ownership_unread 2. REFUSE-02 handles note_duration_event_unread (unread symbols); this task handles the alignment and total-mismatch classes, where notation and TAB disagree or a bar has no notation event. Some refusals may be correct (the source is wrong, ambiguous or not music); those stay refused with a clearer reason.

## Acceptance

1. Measure first with the normal CLI over every approved PDF: for each bar refused with one of these codes, record the located reason (page, system, bar, event, reason code and the disagreement: which side has the extra or missing item), and rank classes by bar count. Counts and codes only in the handback. For each class say whether the refusal is correct (the evidence really disagrees), a reader gap, or unknown.
2. Pick the largest class that is a reader gap and can be settled honestly from the printed notation and TAB together (never from counts or spacing), and fix it; anything not settled stays refused with its located reason. Do not loosen the alignment or total checks to write more bars.
3. Report before and after over the whole private set: bars written, bars refused by code, and every source whose written GPIF changed. No source that converted may lose a correct bar and no bar may be written with a wrong duration; check each newly written bar against its reference where a readable one exists, otherwise against the printed notation, and say which. Reference-less sources are labelled not independently verified.
4. A named mutant (drop the new rule) fails a test on a real source; synthetic tests carry no acceptance weight and the handback says so.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
