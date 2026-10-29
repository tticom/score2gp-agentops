# FND-03B: Repair the GP writer's dangling chord diagram links

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001:U13
- **Depends on:** FND-03A
- **Branch:** `feat/fnd-03b-repair-writer-chord-diagram-links`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Repair the GP writer so every chord diagram link points at a staff-local target that exists. Found by FND-03A's independent reader on 2026-10-29 (author-reported, zero-based locations to re-measure): output 04 has 4 dangling chord targets, output 09 has 12 (for example (0,0,0,0), (2,0,0,0)). Maintainer 2026-10-29: 'Create and prioritise the task.'

## Acceptance

1. Measure first: reproduce the dangling chord-diagram links in the GP files score2gp writes for every converting private source (counts per source, located by staff/bar/voice/beat); the author-reported 4 in output 04 and 12 in output 09 are leads. Find the cause in the writer by reading it.
2. Fix the writer so each chord diagram attached to a beat resolves to a diagram that exists in the staff-local list, with no change to diagrams already correct; the independent reader from FND-03A (tests/gp_structure_oracle.py) is the check, not the writer's own bookkeeping.
3. Before and after, for every converting private source: dangling links (must be zero after), and every other written bar unchanged; any other change is reported as a located difference.
4. A named mutant (reintroduce the wrong staff-local target or bar index) fails a test; synthetic tests carry no acceptance weight and the handback says so.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
