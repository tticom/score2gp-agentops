# OMIT-04-FU1 (retargeted): Convert G-Am-C-Lick.pdf correctly, or refuse each unreadable bar with a located reason

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** OMIT-04
- **Branch:** `feat/omit-04-fu1-g-am-c-lick-pdf`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify `G-Am-C-Lick.pdf` exists there before starting; if it is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Why this task was retargeted

The original task (read a whole real `Lesson-3.gp` that has noteless non-rest beats) was blocked at preflight on 2026-10-20: at `main` `a2d232d` the file already reads (66 bars, 465 events) and the two noteless beats (track 1, bar 19, beats 1 and 2) are already decoded as rests, which `tests/test_gpif_layout_selection.py::test_native_reference_rests_decode_without_rest_tags` requires. The maintainer then directed (2026-10-21, own words): "I think you need to change the fixture used for this development item. Focus the development on G-Am-C-Lick.pdf although currently there is no equivalent gp file." Nothing about the Lesson-3.gp reading behaviour is to change in this task.

## Goal

`G-Am-C-Lick.pdf` (with-score category) converts PARTIAL today: the 2026-10-20 survey at `main` `2eaf679` wrote 4 bars and recorded 5 shortfalls (`note_duration_event_unread` x3, `notehead_digit_count_mismatch` x2). Find the root cause of each shortfall and fix it so the bar is written correctly, or leave the bar refused with a located reason (bar, system, cause). The file also holds the percussive strike (dead-note X head) the maintainer listens to; it must keep converting as it does now.

There is no reference `.gp` for this file and none may be invented. The only oracle is the PDF itself: per bar, the printed notation (rhythm, note types, grouping, rests) and the printed TAB (string and fret) must agree with what is written. Rhythm comes from note type plus grouping, never from counts or spacing.

## Acceptance

1. Measure first: convert `G-Am-C-Lick.pdf` at current `main` and list every shortfall with its bar, cause code and what the PDF shows there (counts, codes and distances only, no musical content). Record the Lesson-3.gp reading result above as re-measured, unchanged.
2. A per-bar ledger of the written bars: for each bar, rhythm and string/fret taken from the PDF's printed notation and TAB independently of the code under test, compared with what the converter writes. A bar that disagrees is a defect to fix or to refuse, never to explain away.
3. Each root cause is fixed in the recogniser or writer, or the bar stays refused with a located reason. No rhythm, fret or string is guessed, copied from another file, or hard-coded for this file.
4. Tests on the real file (private, `work/` temp directory, counts and codes only) fail under named mutants: drop the fix; guess the rhythm from spacing or counts; write the bar without the check; restore the old behaviour. Show each mutant failing.
5. Nothing that worked may change: measure the whole private set at base and head; every file and bar written today keeps a byte-identical GPIF unless the handback lists the file, bar and reason. The percussive-strike output is unchanged.
6. Validation commands pass; handback complete. Say plainly which bars of `G-Am-C-Lick.pdf` are now correct, which are refused and why, and that the maintainer should check the result by ear and eye, since no reference exists.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
