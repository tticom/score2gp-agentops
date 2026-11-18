# CASCADE-01: Refused bars that follow a refused bar (tie stops), and the root refusal behind them

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** none
- **Branch:** `feat/cascade-01-tie-stop-cascade-black-dog-crossroads`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it on the current runtime.

## Why this task exists

Four earlier tasks (REFUSE-24 to 27) each re-ranked every refused bar over the whole private set and each ended blocked on the positive separate-source holdout gate, with the same totals. This task changes the objective so the gate can be met: it targets one named mechanism, with a design source and a different holdout source chosen in advance.

Maintainer observation (2026-11-18, from a fresh survey of 27 PDFs at product `16414f9`): refused bars in `Black Dog.pdf` and `Crossroads.pdf` mostly follow an earlier refused bar. A bar whose tie stop has no written predecessor is refused with `notation_note_without_tab_digit` / `tie_stop_without_written_predecessor`. In Black Dog, source bars 2, 3 and 4 follow source bar 1, which is refused with cause `no_tab_column_at_notation_event` (14 notation events, 10 TAB columns, 14 TAB digits, tab side `notation_has_extra`, digit recovery withheld because `printed_technique_owner_unread`; several curved forms over or beside noteheads are recorded unread). In Crossroads, source bars 6 and 7, 26 and 29 follow refused bars 5, 25 and 28. Treat all of this as a lead and re-measure.

## Goal

1. Measure the cascade on the current runtime over the whole private set: for every refused bar, say whether its own evidence refuses it or whether it is refused only because an earlier bar was refused. Counts and codes only.
2. Take the root refusal in the Black Dog chain (design source). Read the unread curved forms or whatever the page evidence shows owns them, so that the root bar can be written correctly; then the following tie-stop bars may become written because their predecessor is now written. A bar the evidence cannot settle stays refused with a located reason, never guessed.
3. Holdout source: `Crossroads.pdf`. Do not tune on it. Apply the finished reader to it once and report bar by bar against the printed page. The gate needs at least one bar newly written there by the same mechanism. If none is, report the task blocked, not complete; this gate is not waived and you must not substitute another source after seeing the result.

## Acceptance

1. Measure first with the normal CLI over every approved PDF; record per affected bar the located reason (page, system, bar, event, code, cause) and which bars are cascade-only. Classify each refused class as a reader gap, a representation gap or unknown, never as a correct refusal: every approved fixture except the blank No Notes file is real teaching material a human can play from (maintainer, 2026-11-04).
2. Fix the root in the design source only, then apply it once to the holdout source and report bar by bar against the printed page. A bar the evidence cannot settle stays refused.
3. Report before and after over the whole private set: bars written, bars refused by code, and every source whose written GPIF changed. Every source that converted before must keep a byte-identical inner Content/score.gpif unless a refused bar became written, which the handback lists. Check each newly written bar against its reference where a readable one exists, otherwise against the printed page, and say which. Black Dog and Crossroads have no reference file: label them not independently verified and say what the printed-page check was.
4. A named mutant (drop the new rule) fails a test on a real source; synthetic tests carry no acceptance weight and the handback says so.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion. In particular never write a tie stop as an unrelated new note, and never drop a tie to make a bar pass.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
