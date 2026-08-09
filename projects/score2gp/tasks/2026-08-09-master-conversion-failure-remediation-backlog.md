# Milestone 6: Master Conversion Failure Remediation Backlog

All tasks in this backlog must strictly adhere to the following **Test Writing and Isolation Standards**:
- **Real-World Test Requirement**: Every code modification MUST be verified by an in-situ integration test loading `Lesson-5.pdf` or `Lesson-6.pdf` from the private fixtures repository.
- **Isolated Unit Test Requirement**: If isolated unit testing adds coverage value, write a separate unit test using public/synthetic inputs.
- **CI Portability**: All in-situ integration tests that require private fixtures MUST use a graceful skip mechanism (e.g., `@pytest.mark.skipif`) when the private fixtures repository is not present. This ensures that the public unit tests still run in public GitHub Actions.
- **Banned**: Purely synthetic/mocked tests are banned from being the *sole* validation instrument.

---

## M6-1: In-Situ Real-Fixture Testing Integration & Fallback Cleanup
* **Status**: APPROVED
* **Owning Repo**: `score2gp`
* **Branch**: `feature/agy/m6-in-situ-testing`
* **Target Files**: `src/score2gp/build_ir.py`, `src/score2gp/pdf.py`, `tests/test_real_fixtures_alignment.py` (New File)
* **Prompt**: `projects/score2gp/prompts/next/0043-m6-in-situ-real-fixture-testing.md`
* **Acceptance**:
  - `synthesize_missing_tab` standard tuning fallback is completely deleted from `build_ir.py`.
  - `outer_tolerance` snapping tolerance is reset to `24.0` points in `pdf.py`.
  - New test suite loads `Lesson-5.pdf` and `Lesson-6.pdf` from the private fixtures repository.
  - Asserts exactly `38` and `72` measures respectively and verifies no unassigned playable candidates remain.
  - Integration tests use `pytest.mark.skipif` to skip gracefully when private fixtures are missing, allowing CI to pass.

## M6-2: Port and Harmonize Barline Detection
* **Status**: APPROVED
* **Owning Repo**: `score2gp`
* **Branch**: `feature/agy/m6-barline-harmonization`
* **Target Files**: `src/score2gp/pdf.py`, `src/score2gp/notation_omr/pipeline.py`
* **Prompt**: `projects/score2gp/prompts/next/0044-m6-port-and-harmonize-barline-detection.md`
* **Acceptance**:
  - `MIN_INHERITED_INTERNAL_BAR_WIDTH` is `20.0` points.
  - Short relative barlines (min height `15.0` or `staff_height - 2.0`) are accepted.
  - Edge double barlines are resolved.
  - Notation staves' confirmed barlines are inherited in OMR pipeline.
  - `Lesson-5.pdf` sidecar generates with exactly `38` measures.
  - Governed by both in-situ and isolated tests (if value added).

## M6-3: Implement Page Coordinate Offsets and Global Indexing
* **Status**: APPROVED
* **Owning Repo**: `score2gp`
* **Branch**: `feature/agy/m6-page-offsets`
* **Target Files**: `src/score2gp/pdf.py`
* **Prompt**: `projects/score2gp/prompts/next/0045-m6-implement-page-coordinate-offsets.md`
* **Acceptance**:
  - `running_bar_index` sequentially tracks measure indices across page boundaries.
  - Cumulative y-offsets are calculated dynamically based on page heights.
  - Standard OMR sidecar measures are sequentially incremented.
  - Governed by both in-situ and isolated tests (if value added).

## M6-4: Prevent Fret Digit Over-Merging
* **Status**: APPROVED
* **Owning Repo**: `score2gp`
* **Branch**: `feature/agy/m6-digit-merging-guard`
* **Target Files**: `src/score2gp/pdf.py`
* **Prompt**: `projects/score2gp/prompts/next/0046-m6-prevent-digit-over-merging.md`
* **Acceptance**:
  - Merged fret values never exceed `24`.
  - Consecutive single-digit notes (e.g., `7 10`) are preserved as separate candidates.
  - Governed by both in-situ and isolated tests (if value added).
