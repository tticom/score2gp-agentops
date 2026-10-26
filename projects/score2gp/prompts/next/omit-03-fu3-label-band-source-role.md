# OMIT-03-FU3: Labels: measure the 51 corpus lines between five and seven staff spaces above the staff and give the rotated tab-clef glyph its own reason code

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** OMIT-03
- **Branch:** `feat/omit-03-fu3-label-band-source-role`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Labels: measure the 51 corpus lines between five and seven staff spaces above the staff and give the rotated tab-clef glyph its own reason code. Source: authority item OMIT-03-FU3. Non-blocking follow-up 3 from tticomgov-code's approving re-review 5365611424 of tticom/score2gp#473 (OMIT-03) at 51f8f05. The label band is a fixed five staff spaces above the top staff line. One real Lesson 4 reference label sits 6.4 spaces above and is refused, and 51 corpus lines between five and seven spaces still need a measured source-role rule before the band can widen without admitting a wrong read. In Lesson 4 pdf_text_outside_annotation_band also holds the rotated tab clef glyph, so the missing label is identifiable only by its located bbox: give that glyph its own reason code.

## Acceptance

1. Measure first: list, per approved real source, the text lines between five and seven staff spaces above the top staff line (counts, distances, source role only), and the Lesson 4 label at 6.4 spaces.
2. The rotated tab clef glyph in Lesson 4 is refused under its own reason code, not pdf_text_outside_annotation_band. The band is widened only if a measured source-role rule admits no wrong read; otherwise the band is unchanged and the handback says so with the counts.
3. No label is guessed or copied from a reference; named mutants (drop the new reason code; widen the band without the rule) fail a public or real-file test.
4. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
