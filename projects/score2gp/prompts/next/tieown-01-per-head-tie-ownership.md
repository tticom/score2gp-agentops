# TIEOWN-01: Read which head of a chord owns a tie

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/tieown-01-per-head-tie-ownership`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime, and do not trust an older survey.

## Goal

REFUSE-12 deliberately excludes tie.start when it ties one head of a chord to the note before it, because copying would invent ties on other heads. The rest of the class is per-head tie ownership: a chord that is both a tie stop on one head and a tie start (a tied chain), a 6-head chord with 4 digits whose two heads are tie stops from a previous 2-head chord, the mixed_percussive_tie_ownership_unread bars (3), and the tie_stop_without_written_predecessor bars that cascade from them (10 at the last measurement). Leads, not facts: re-measure. Settle ownership from the tie arc's end points against each head's own position, never from counts.

## Acceptance

1. Measure first with the normal CLI over every approved PDF: record per affected bar the located reason (page, system, bar, event, code, cause) and rank the causes by bar count. Counts and codes only in the handback. Classify every refused class as a reader gap, a representation gap or unknown, never as a correct refusal: every approved fixture except the blank No Notes file is real teaching material a human can play from (maintainer, 2026-11-04). A bar the evidence cannot yet settle stays refused with a located reason, never guessed, and is reported as unfinished. Separate the cascade bars (their predecessor is refused) from the ownership bars, and say which refused predecessor each cascade waits for.
2. Read a tie's owner per head from the arc's start and end positions against the head positions, requiring exactly one head at each end; anything ambiguous stays refused with its located reason. Unlock the cascade bars only through this reading, never by writing a tie with no printed arc.
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
