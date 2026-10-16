# CFW-05: Can't Find My Way Home: write bar 6 now that dead-note heads are read

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** CFW-04, SCALE-01, UNREAD-02
- **Branch:** `feat/cfw-05-dead-note-bar-6`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Bar 6 of Can't Find My Way Home was refused because the dead-note head was unread. UNREAD-02 (product #489) now reads the cross head and writes percussive strikes. Measure what bar 6 does today; write it correctly if the pairing is unambiguous, otherwise keep it refused with a located reason.

## Acceptance

1. Measure first: the written/refused status and reason of every bar of Can't Find My Way Home at base, and what the reference `.gp` carries for bar 6 (the reference marks that note Muted/Enable; the writer emits DeadNote for a percussive strike: say which is right for the stored form and why, without copying a value from the reference into code).
2. Bar 6 is either written with the percussive strike in the position the PDF shows, with every other note and technique of the bar equal to the independent comparator's reading of the reference, or it stays refused with a located reason code naming bar 6. No invented value.
3. A real-source test on Can't Find My Way Home asserts bar 6's outcome and that a mutant (drop the strike; write it as an ordinary fret 0 note; move it one string) fails on the real file.
4. Nothing that worked may change: the 9 bars written today keep a byte-identical GPIF; measured on the whole private set, base versus head.
5. Validation commands pass; handback complete.

## Notes

Context: UNREAD-02 stores a percussive strike as a dead note whose stored fret follows the printed head position, else the next same-string note, else the previous, else open. Maintainer decision: the cross head tells the musician how to position the hand for what comes next; it makes no difference to pitch. Do not change that rule here; if bar 6 exposes a case it does not cover, report it.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant: drop the feature, hard-code the value, invert the condition, restore the old behaviour) and show that mutant failing. A test that only shows the happy path passing is not evidence and must not be added. Acceptance rests on genuine approved sources (the private corpus and its reference `.gp` files, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion. A test that encodes behaviour this task deliberately changes is updated with the reason stated in the handback; every numeric and reference check it had is kept.
- **Nothing that worked may change:** measure the whole private set at base and at head. Every file and bar written today keeps a byte-identical GPIF unless the task says otherwise and the handback lists the file, bar and reason.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only. Private tests convert under `<repo>/work` in a `tempfile.TemporaryDirectory`.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`. Complete the handback with every acceptance item PASS and the evidence for each.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
