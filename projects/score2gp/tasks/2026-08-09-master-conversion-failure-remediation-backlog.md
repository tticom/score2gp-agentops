# Milestone 6: Master Conversion Failure Remediation Backlog

## M6-1: Port and Harmonize Barline Detection
* **Status**: APPROVED
* **Owning Repo**: `score2gp`
* **Branch**: `feature/agy/m6-barline-harmonization`
* **Target Files**: `src/score2gp/pdf.py`, `src/score2gp/notation_omr/pipeline.py`
* **Prompt**: `projects/score2gp/prompts/next/0043-m6-port-and-harmonize-barline-detection.md`
* **Acceptance**:
  - `MIN_INHERITED_INTERNAL_BAR_WIDTH` is `20.0` points.
  - Short relative barlines (min height `15.0` or `staff_height - 2.0`) are accepted.
  - Edge double barlines are resolved.
  - Notation staves' confirmed barlines are inherited in OMR pipeline.
  - `Lesson-5.pdf` sidecar generates with exactly `38` measures.

## M6-2: Implement Page Coordinate Offsets and Global Indexing
* **Status**: APPROVED
* **Owning Repo**: `score2gp`
* **Branch**: `feature/agy/m6-page-offsets`
* **Target Files**: `src/score2gp/pdf.py`
* **Prompt**: `projects/score2gp/prompts/next/0044-m6-implement-page-coordinate-offsets.md`
* **Acceptance**:
  - `running_bar_index` sequentially tracks measure indices across page boundaries.
  - Cumulative y-offsets are calculated dynamically based on page heights.
  - Standard OMR sidecar measures are sequentially incremented.

## M6-3: Prevent Fret Digit Over-Merging
* **Status**: APPROVED
* **Owning Repo**: `score2gp`
* **Branch**: `feature/agy/m6-digit-merging-guard`
* **Target Files**: `src/score2gp/pdf.py`
* **Prompt**: `projects/score2gp/prompts/next/0045-m6-prevent-digit-over-merging.md`
* **Acceptance**:
  - Merged fret values never exceed `24`.
  - Consecutive single-digit notes (e.g. `7 10`) are preserved as separate candidates.
  - All existing tests pass.

## M6-4: In-Situ Real-Fixture Testing Integration
* **Status**: APPROVED
* **Owning Repo**: `score2gp`
* **Branch**: `feature/agy/m6-in-situ-testing`
* **Target Files**: `src/score2gp/build_ir.py`, `src/score2gp/pdf.py`, `tests/test_real_fixtures_alignment.py` (New File)
* **Prompt**: `projects/score2gp/prompts/next/0046-m6-in-situ-real-fixture-testing.md`
* **Acceptance**:
  - `synthesize_missing_tab` standard tuning fallback is deleted.
  - `outer_tolerance` snapping tolerance is reset to `24.0` points.
  - New test suite loads `Lesson-5.pdf` and `Lesson-6.pdf` from the private fixtures repository.
  - Asserts exactly `38` and `72` measures respectively and verifies no unassigned playable candidates remain.
