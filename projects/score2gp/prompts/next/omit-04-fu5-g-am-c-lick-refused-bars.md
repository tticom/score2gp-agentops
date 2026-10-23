# OMIT-04-FU5: G-Am-C-Lick.pdf refused bars and missed percussive strikes

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** OMIT-04-FU1
- **Branch:** `feat/omit-04-fu5-g-am-c-lick-refused-bars`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify `G-Am-C-Lick.pdf` exists there before starting; if it is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Why this task exists

OMIT-04-FU1 (product PR 507) added a source ledger and located-refusal evidence for `G-Am-C-Lick.pdf` but fixed no bar: 4 of 9 bars are written (3, 5, 7, 9) and 5 are refused (1, 2, 4, 6, 8; `note_duration_event_unread` x3, `notehead_digit_count_mismatch` x2). The maintainer listened to the output (2026-10-22/23): most of the score is missing, a few percussive notes are present and sound good, and not all percussive strikes were found. The ledger showed zero strike mismatches in the written bars, so the missed strikes are most likely in the refused bars, which write no beats. This task reads those bars. No reference `.gp` exists and none may be invented: the PDF's printed notation and TAB are the only oracle.

## Goal

Write each refused bar exactly as printed, or leave it refused with a located reason, and make every printed percussive strike in a written bar come out as a dead note. Rhythm comes from note type plus grouping, never from counts or spacing.

## Acceptance

1. Measure first: convert G-Am-C-Lick.pdf at current main and list, for each of the five refused bars (1, 2, 4, 6, 8), its cause code, system and what the PDF prints there (head counts, TAB candidates, distances only), and count every printed percussive strike (dead-note X head) per bar against the strikes written. Re-measure; the earlier counts are leads.
2. Root cause per refused bar: bars with 2 notation heads against 1 printed TAB candidate (bars 2 and 6) and the bar with an unread rest or multi-head X form beside a note (bar 8) are fixed in the recogniser or writer so the bar is written exactly as printed, or the bar stays refused with a located reason. No rhythm, string or fret is guessed, copied from another file or hard-coded for this file.
3. An independent per-bar ledger covers EVERY written bar, including each newly recovered bar: event kind, note value, dots, tuplets, ties, ordered string/fret groups and strikes are taken from the PDF's printed notation and TAB independently of the code under test and compared with the final GPIF. Any disagreement fails acceptance or leaves the bar refused; byte identity of already-written bars does not stand in for this. No reference .gp may be invented.
4. Every printed percussive strike in a bar that is written is written as a dead note, using the stored convention of the percussive-strike decision; a ledger compares strikes printed and strikes written per bar, taken from the PDF independently of the code under test. A strike in a refused bar is reported as part of that bar's refusal, never dropped silently.
5. Real-file tests fail under named mutants: drop the fix; guess the rhythm from spacing or counts; write the bar without the head-to-string check; write a wrong non-strike value (note value or fret) in a recovered bar; drop a strike; restore the old behaviour. Each is shown failing.
6. Nothing that worked may change: bars 3, 5, 7 and 9 of G-Am-C-Lick.pdf and every file and bar written today keep a byte-identical GPIF unless the handback lists the file, bar and reason; the whole private set is measured at base and head.
7. Validation commands pass; handback complete. It says plainly which bars are now correct, which remain refused and why, and that the maintainer should check the result by ear and eye since no reference .gp exists.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
