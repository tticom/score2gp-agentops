# REFUSE-02: Read the remaining unread-symbol classes: accidental beside notehead, rests, marks over and under noteheads, tuplets, parenthesised heads

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/refuse-02-read-next-unread-symbol-class`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

Read the next largest honestly readable unread-symbol class, measured on the current runtime. REFUSE-01B (natural signs, merged as #530) moved the 43-PDF baseline from 672 written and 134 refused to 682 and 124, and its report lists what still occurs (leads, re-measure): accidental beside notehead (38 unread, many as rest_sized_curve), over or under notehead (17 unread, 87 ignored), rests (9 unread), tuplet numbers (2 unread). Also diagnose Hey Joe and Pride and Joy (pdf_only_tab_grouping_unsafe with a score) and Black Dog (every bar refused). Real approved sources carry acceptance.

## Acceptance

1. Measure first with the normal CLI over every approved PDF: for each bar refused with note_duration_event_unread (and the other located codes), record the located reason (page, system, bar, event, reason code, shape class) and rank by bar count. Counts and codes only in the handback. State which classes in the leads still occur at all, and separately what blocks Hey Joe, Pride and Joy and Black Dog.
2. Pick the largest class that can be read honestly from note type plus grouping or from a symbol that is unambiguously musical, and read it; anything not settled stays refused with its located reason. No duration is guessed and no spacing or count inference is used (rhythm comes from notation).
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
