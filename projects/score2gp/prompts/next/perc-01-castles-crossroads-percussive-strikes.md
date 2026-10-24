# PERC-01: Castles Made of Sand.pdf and Crossroads.pdf: write the bars as printed, or refuse them with a located reason; write every printed percussive strike

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** OMIT-04-FU5
- **Branch:** `feat/perc-01-castles-crossroads-percussive-strikes`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Castles Made of Sand.pdf and Crossroads.pdf: write the bars as printed, or refuse them with a located reason; write every printed percussive strike. Source: authority item PERC-01. Maintainer 2026-10-22: both PDFs contain percussive strikes (dead-note X heads) and neither has a reference .gp. Survey 2026-10-20: both REFUSED with pdf_only_tab_grouping_unsafe, so the strike cannot be judged until the bars are written; depends on the grouping work and on the G-Am-C-Lick.pdf tasks. Oracle: the PDF's own notation and TAB plus the maintainer's check by ear and eye; no reference may be invented. Follow the storage convention in the percussive-strike decision (UNREAD-02). Needs detail: which grouping cause blocks each file and whether it is one shared fix.

## Acceptance

1. Measure first: convert both PDFs at current main; for each refused bar list the cause code (pdf_only_tab_grouping_unsafe is the lead), system and what the PDF prints (head counts, TAB candidates, distances only), and count every printed percussive strike (dead-note X head) per bar. Say whether one shared fix serves both files or not.
2. Root cause per refused bar is fixed in the recogniser or writer so the bar is written exactly as printed, or the bar stays refused with a located reason. No rhythm, string or fret is guessed, copied from another file or hard-coded for a file; rhythm comes from note type plus grouping, never from counts or spacing. No reference .gp exists and none may be invented.
3. An independent per-bar ledger covers EVERY written bar of both files: event kind, note value, dots, tuplets, ties, ordered string/fret groups and strikes are taken from the PDF's printed notation and TAB independently of the code under test and compared with the final GPIF. Any disagreement fails acceptance or leaves the bar refused.
4. Every printed percussive strike in a written bar is written as a dead note using the stored convention of the percussive-strike decision (UNREAD-02); a strike in a refused bar is reported as part of that bar's refusal, never dropped silently.
5. Real-file tests fail under named mutants: drop the fix; guess the rhythm from spacing or counts; write the bar without the head-to-string check; write a wrong non-strike value; drop a strike; restore the old behaviour. Each is shown failing.
6. Nothing that worked may change: G-Am-C-Lick.pdf and every file and bar written today keep a byte-identical GPIF unless the handback lists the file, bar and reason; the whole private set is measured at base and head.
7. The handback says plainly which bars are now correct, which remain refused and why, and that the maintainer should check the result by ear and eye since no reference .gp exists.
8. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
