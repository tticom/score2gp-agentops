# REFUSE-01B: Reduce refused bars by reading the largest honestly readable unread class, measured on the current runtime

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/refuse-01b-reduce-refused-bars-current-runtime`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

Reduce refused bars on the approved private PDFs by reading the largest honestly readable class of unread symbol or bar, measured on the current runtime. Replaces REFUSE-01, whose premise (thin bands) was stale: those bands are beams already owned. Baseline from the REFUSE-01 author run (leads, re-measure): 43 PDFs, 672 bars written, 134 refused: note_duration_event_unread 63, notation_note_without_tab_digit 25, bar_total_mismatch 18, bar_without_notation_event 15, notehead_digit_count_mismatch 11; residual unclassified symbols are arpeggio fragments, bend curves and vibrato marks. The older REFUSE-02 backlog counts (accidental beside notehead 93, rests 37, over or under notehead 35, tuplet numbers 31) came from the same stale survey and must be re-measured too.

## Acceptance

1. Measure first with the normal CLI over every approved PDF: for each bar refused with note_duration_event_unread, record the located reason (page, system, bar, event, reason code and shape class), then rank the reasons by bar count. Counts and codes only in the handback, no private content. State which of the REFUSE-02 classes still occur at all on the current runtime.
2. Pick the largest class that can be read honestly from note type plus grouping or from a symbol that is unambiguously musical, and read it; anything not settled stays refused with its located reason. No duration is guessed and no spacing or count inference is used (rhythm comes from notation).
3. Report before and after over the whole private set: bars written, bars refused by code, and every source whose written GPIF changed. No source that converted may lose a correct bar and no bar may be written with a wrong duration; check each newly written bar against its reference where a readable one exists, otherwise against the printed notation, and say which. Reference-less sources are labelled not independently verified.
4. A named mutant (drop the new rule) fails a test; synthetic tests carry no acceptance weight and the handback says so.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
