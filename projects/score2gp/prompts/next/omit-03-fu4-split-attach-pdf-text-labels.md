# OMIT-03-FU4: pdf_text_labels: split attach_pdf_text_labels, name the thresholds, move the late import to module level

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** OMIT-03
- **Branch:** `feat/omit-03-fu4-split-attach-pdf-text-labels`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

pdf_text_labels: split attach_pdf_text_labels, name the thresholds, move the late import to module level. Source: authority item OMIT-03-FU4. Non-blocking follow-up 4 from tticomgov-code's approving re-review 5365611424 of tticom/score2gp#473 (OMIT-03) at 51f8f05. Suspected smell only: attach_pdf_text_labels is one function of about 90 lines with nested branches and inline thresholds (5 spaces, 2 pt margin, 1 pt boundary, 7/15/16 pt sizes), cli.py imports pdf_text_labels inside convert_command, and a test imports the private _classify. Split into classify, locate-bar and choose-beat steps, name the thresholds, and keep the written GP byte-identical.

## Acceptance

1. Measure first: record length and nesting depth of attach_pdf_text_labels in src/score2gp/pdf_text_labels.py, list the inline thresholds (5 spaces, 2 pt margin, 1 pt boundary, 7/15/16 pt sizes), the late import in cli.py convert_command and the test import of the private _classify.
2. Split into classify, locate-bar and choose-beat steps with named threshold constants and the import at module level; no behaviour change: the whole private set gives a byte-identical GPIF before and after, shown in the handback.
3. Existing label tests pass unchanged; a named mutant (change one named threshold) fails a test.
4. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
