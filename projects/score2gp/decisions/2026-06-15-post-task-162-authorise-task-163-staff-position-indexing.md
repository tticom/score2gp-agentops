# Record Product Task 162 completion and authorise Product Task 163

## Product Task 162 Completion

Product Task 162 implemented read-only `ledger_line_candidate` extraction from existing diagnostic evidence. The task was recorded in PR #282 in `tticom/score2gp`.

* **PR URL**: https://github.com/tticom/score2gp/pull/282
* **Final head SHA**: `2fba20464b806f572fa5124c7ad0cc6e2c9bb8fe`
* **Merge commit**: `e32a585c8896aa5e72f2c09ad85d46ad53a2b105`
* **Merged timestamp**: `2026-06-15T14:06:43Z`

### Exact Files Changed
* `fixtures/public/generated_standard_staff_ledger_lines.json`
* `scripts/note_candidate_recognition_report.py`
* `src/score2gp/cli.py`
* `src/score2gp/whole_note_recogniser.py`
* `tests/fixtures/pdf/generated_standard_staff_ledger_lines.pdf`
* `tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py`
* `tests/test_note_candidate_recognition_cli.py`
* `tests/test_note_candidate_recognition_report.py`

### Fixture/Artifact Hygiene Statement
New public generated ledger-line fixture data was added:
* `fixtures/public/generated_standard_staff_ledger_lines.json`
* `tests/fixtures/pdf/generated_standard_staff_ledger_lines.pdf`

These fixtures are programmatically generated test data representing a standard staff with ledger lines. They contain no private score data, raw glyph content, or unverified structural elements, meaning they are completely safe to commit.

### Implemented `ledger_line_candidate` Boundary
The fail-closed boundary was preserved: ledger lines are emitted only when a horizontal stroke overlaps a core primitive within the same compact cluster; isolated horizontal strokes are not promoted.

### Candidate Shape
The output `ledger_line_candidate` object includes the following properties:
* `symbol_type`: `ledger_line_candidate`
* `candidate_id`
* `page_index`
* `system_index`
* `staff_index`
* `bbox`
* `source`: `diagnostic_candidate_evidence`

### Duplicate Beam/Ledger Suppression Approach
Primitives identified as `ledger_line_candidate`s are actively excluded from the `beam_candidate` pool to prevent double emission.

### Cross-page/staff Codex Fix Summary
Codex identified that the original duplicate suppression logic used only the bounding box across the entire document, which could erroneously suppress a valid beam on another page/staff if it coincidentally matched the coordinates of a ledger line. The suppression key was corrected to a fully scoped key including `page_index`, `system_index`, `staff_index`, and `bbox`. A regression test was added to guarantee cross-page suppression safety.

### Validation
* Validation Command: `pytest tests/test_note_candidate_recognition_report.py tests/test_note_candidate_recognition_cli.py tests/test_whole_note_recognition_cli.py`
* Validation Result: 35 passed.
* `git diff --check main...HEAD` Result: Clean.

### Codex Disposition
The Codex thread regarding duplicate suppression scoping was replied to and resolved before merging.

### Explicit Non-goals Preserved
* No pitch inference or ledger-line pitch mapping was implemented.
* `staff_position_index` and `assumed_treble_pitch` behaviour remains preserved.
* Whole-note recognition compatibility was preserved.
* No ScoreIR, MusicXML, Guitar Pro, GP output, OCR, rests, clef recognition, accidentals, key signatures, or rhythm inference were implemented.

## Authorisation

This document authorises the next task: **Product Task 163 — Add read-only staff-position indexing for ledger-line candidates**.
