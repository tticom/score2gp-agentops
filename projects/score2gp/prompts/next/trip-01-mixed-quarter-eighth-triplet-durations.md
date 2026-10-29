# TRIP-01: Check and fix recognition of mixed quarter, eighth and quarter-note-triplet durations

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001:U13
- **Depends on:** none
- **Branch:** `feat/trip-01-mixed-quarter-eighth-triplet-durations`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Investigate whether duration recognition handles mixed quarter notes, eighth notes and quarter-note triplets (1/4-note triplets, as the maintainer wrote; eighth-note triplets are checked as well if the score prints them), using Mixing Lead & Rhythm pt1.pdf (the PDF, which is not corrupted). Maintainer 2026-10-29: 'The note counts are consistent, but maybe highlighting a flaw in the codes note duration recognition as there are mixed 1/4, 1/8 and 1/4 note triplets in the score. So if we can't recognise that we've found a system flaw.' Its reference .gp is unreadable (high-entropy score member), so the printed notation is the only check and results are labelled not independently verified.

## Acceptance

1. Measure first on Mixing Lead & Rhythm pt1.pdf: per bar, which note types and tuplet groups are printed (quarter, eighth, quarter-note-triplet and any eighth-note-triplet groups, each with its bracket or number and its tuplet base value) versus what the pipeline reads; report bars written, refused (by code) and any bar whose written duration disagrees with the printed notation, located by page, system and bar. Counts and codes only in the handback; no private content.
2. Quarter-note triplets are explicitly in scope and are not satisfied by eighth-note-triplet support alone; state which tuplet base values the PDF actually prints before narrowing anything. If triplets or mixed values are misread or silently dropped, make the reader recognise them from note type plus grouping (beams, tuplet marks) and never from spacing or counts; anything that cannot be settled stays refused with a located reason. No duration is guessed.
3. Across the whole private set report before and after: bars written, bars refused by code, and every source whose written GPIF changed; no converted bar may lose correctness or gain a wrong duration (check against the reference where one is readable, otherwise against the printed notation, and say which).
4. A named mutant (drop the quarter-note-triplet rule, and separately the eighth-note-triplet rule if one is added) fails a test; synthetic tests carry no acceptance weight and the handback says so.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
