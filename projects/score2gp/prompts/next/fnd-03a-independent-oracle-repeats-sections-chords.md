# FND-03A: FND-03 slice A: extend the independent stdlib GP reader oracle to repeats and endings, sections and chord diagrams

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001:U13
- **Depends on:** none
- **Branch:** `feat/fnd-03a-independent-oracle-repeats-sections-chords`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

FND-03 slice A: extend the independent stdlib GP reader oracle to repeats and endings, sections and chord diagrams. Source: authority item FND-03A. Ex 2 Hands Up GP6 vs GP7 encode repeat counts differently (2 vs 4): raw attributes are not version-neutral.

## Acceptance

1. Measure first: list what the independent reader under tests/ or scripts/ (stdlib only) reads today and which GPIF elements it ignores (repeats and alternate endings, section markers, chord diagrams); re-locate it, do not assume.
2. The reader gains those three element kinds, written from the GPIF/GP file specification and from the real reference .gp files, not from score2gp's own writer code, so it stays independent; the handback states what each was derived from.
3. Run it on every private reference .gp and on the GP files score2gp writes for the same sources; report the agreements and disagreements by kind, and list any disagreement as a located defect rather than adjusting the oracle to match the writer.
4. A named mutant of each new reader rule fails a test; no change to the writer in this task.
5. This is slice A only. The rest of FND-03 (grace notes, ties, tuplets, slides, HOPO, bends, vibrato, accents, mutes, normalized play order, retiring or rewiring scripts/oracle.py) stays open under FND-03, which FND-04, BRD-01 and BRD-02 still depend on; do not claim FND-03 complete.
6. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
