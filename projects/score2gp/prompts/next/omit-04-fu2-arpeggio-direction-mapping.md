# OMIT-04-FU2: Arpeggio direction: comment the upward-arrow-to-Down mapping and verify Up on a real reference when one exists

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** OMIT-04
- **Branch:** `feat/omit-04-fu2-arpeggio-direction-mapping`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Arpeggio direction: comment the upward-arrow-to-Down mapping and verify Up on a real reference when one exists. Source: authority item OMIT-04-FU2. Non-blocking follow-ups from tticomgov-code's approving review 5378371016 of tticom/score2gp#475 (OMIT-04) at 3c5536d: _marks in src/score2gp/pdf_arpeggios.py labels an upward arrow 'down' (the GPIF value) with no code comment explaining it, and only the Down value occurs in the real references, so Up is verified only on a synthetic fixture. Document the mapping where it is made and verify Up against a real reference when one has an up arpeggio.

## Acceptance

1. Measure first: read _marks in src/score2gp/pdf_arpeggios.py and list which real references contain an arpeggio and in which direction (counts only).
2. The mapping of an upward arrow to the GPIF value is documented where it is made. If a real reference with an up arpeggio exists, Up is verified against it; otherwise the handback says plainly that Up remains verified only on a synthetic fixture.
3. A mutant that swaps the mapping fails a public test; no behaviour change.
4. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
