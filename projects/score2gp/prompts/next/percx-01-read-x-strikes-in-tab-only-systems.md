# PERCX-01: Read X percussive strikes in TAB that has no notation staff

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/percx-01-read-x-strikes-in-tab-only-systems`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

NOROUTE-01 found that a one-page TAB-only source (five systems, printed 4/4, chord names, no stems, beams or flags) stops with percussive_strike_without_owning_note: 0 notation bars, 82 TAB digits unplaced and 6 X strikes (system 4, bar 6). The maintainer decided the terminology and storage of X heads (percussive strikes) in UNREAD-02 (see the percussive-strike memory). Without a notation staff an X strike has no owning note, so the route refuses before any bar. The source prints no rhythm marks, so its durations are TABGUESS-01 territory; this task is only about letting a strike without an owning note be read and carried, so that the layer below rhythm is complete. Leads, not facts: re-measure.

## Acceptance

1. Measure first with the normal CLI over every approved PDF: record per affected bar the located reason (page, system, bar, event, code, cause) and rank the causes by bar count. Counts and codes only in the handback. Classify every refused class as a reader gap, a representation gap or unknown, never as a correct refusal: every approved fixture except the blank No Notes file is real teaching material a human can play from (maintainer, 2026-11-04). A bar the evidence cannot yet settle stays refused with a located reason, never guessed, and is reported as unfinished. For each X strike say what it is on the printed page (view it), which system and bar it is in, and what the UNREAD-02 convention would store.
2. Read an X strike in TAB-only input as a percussive strike under the UNREAD-02 convention, owned by its own TAB column, and let the route continue to the rhythm stage. The strike must never become a fret digit or a note with a pitch. The source still has no rhythm (it prints none), so it must still stay refused for that with a located reason and no guessed duration; the visible change is the refusal moving from the strike to the missing rhythm. Check this on a source that does print rhythm and has X strikes, where bars should now be written.
3. Report before and after over the whole private set: bars written, bars refused by code, and every source whose written GPIF changed. Every source that converted before must keep a byte-identical inner Content/score.gpif unless a refused bar became written, which the handback lists. Check each newly written bar against its reference where a readable one exists, otherwise against the printed page, and say which. Reference-less sources are labelled not independently verified.
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
