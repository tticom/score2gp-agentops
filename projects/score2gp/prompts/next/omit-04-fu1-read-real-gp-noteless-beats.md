# OMIT-04-FU1: Read a whole real Guitar Pro file that has noteless non-rest beats, or refuse them with a located reason

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** OMIT-04
- **Branch:** `feat/omit-04-fu1-read-real-gp-noteless-beats`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Read a whole real Guitar Pro file that has noteless non-rest beats, or refuse them with a located reason. Source: authority item OMIT-04-FU1. Found by the author of tticom/score2gp#475 (OMIT-04) and confirmed as pre-existing by tticomgov-code's approving review 5378371016: extract_score_ir_from_gp refuses the whole real Lesson-3.gp with a noteless-beat error, also at the base with the arpeggios stripped. validate_roundtrip, compare_gp and scripts/oracle.py therefore cannot round-trip a real Guitar Pro file end to end, only the public fixtures. Read beats that carry no note and are not rests (for example a beat that holds only a symbol), or refuse them with a located reason, and add a read test on a real reference.

## Acceptance

1. Measure first: reproduce the refusal of the real Lesson-3.gp reference by extract_score_ir_from_gp at current main; count the noteless non-rest beats and say what they hold.
2. Such beats are read faithfully (no invented note or rest) or refused with a located reason (bar, track, beat); the whole real file then either reads or is refused for a named, located cause.
3. A read test on the real Lesson-3.gp reference fails under mutants (drop the beat silently; turn it into a rest; keep the old whole-file refusal), and validate_roundtrip, compare_gp and scripts/oracle.py are exercised on the real file end to end, or the blocker is named.
4. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant: drop the feature, hard-code the value, invert the condition, restore the old behaviour) and show that mutant failing. A test that only shows the happy path passing is not evidence and must not be added. Acceptance rests on genuine approved sources (the private corpus and its reference `.gp` files, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion. A test that encodes behaviour this task deliberately changes is updated with the reason stated in the handback; every numeric and reference check it had is kept.
- **Nothing that worked may change:** measure the whole private set at base and at head. Every file and bar written today keeps a byte-identical GPIF unless the task says otherwise and the handback lists the file, bar and reason.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only. Private tests convert under `<repo>/work` in a `tempfile.TemporaryDirectory`.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`. Complete the handback with every acceptance item PASS and the evidence for each.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
