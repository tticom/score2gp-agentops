# Milestone 6: Master Conversion Failure Remediation Backlog

All tasks in this backlog must strictly adhere to the following **Test Writing and Isolation Standards**:
- **Real-World Test Requirement**: Every code modification MUST be verified by an in-situ integration test loading `Lesson-5.pdf` or `Lesson-6.pdf` from the private fixtures repository.
- **Real-Source Unit/Contract Requirement**: Behavioural cases must be whole private fixtures or provenance-linked extractions from real PDFs.
- **CI Portability**: Public CI may report private tests as NOT_EVALUATED, but a skipped required suite cannot satisfy review or merge acceptance.
- **Banned**: Synthetic or mocked behavioural conversion tests as acceptance and refusal-only completion claims.
- **Architecture Gate**: Every M6 task below is blocked by Task 88 until its constants, seams, and oracle are accepted.

---

## M6-1: In-Situ Real-Fixture Testing Integration & Fallback Cleanup
* **Status**: BLOCKED — architecture and oracle prerequisites unresolved
* **Owning Repo**: `score2gp`
* **Branch**: `feature/agy/m6-in-situ-testing`
* **Target Files**: `src/score2gp/build_ir.py`, `src/score2gp/pdf.py`, `tests/test_real_fixtures_alignment.py` (New File)
* **Prompt**: `projects/score2gp/prompts/next/0043-m6-in-situ-real-fixture-testing.md`
* **Acceptance**:
  - `synthesize_missing_tab` standard tuning fallback is completely deleted from `build_ir.py`.
  - `outer_tolerance` snapping tolerance is reset to `24.0` points in `pdf.py`.
  - New test suite loads `Lesson-5.pdf` and `Lesson-6.pdf` from the private fixtures repository.
  - Asserts exactly `38` and `72` measures respectively and verifies no unassigned playable candidates remain.
  - A missing private corpus reports NOT_EVALUATED and cannot satisfy merge evidence.

## M6-2: Port and Harmonize Barline Detection
* **Status**: BLOCKED — architecture and oracle prerequisites unresolved
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
* **Status**: BLOCKED — architecture and oracle prerequisites unresolved
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
* **Status**: BLOCKED — architecture and oracle prerequisites unresolved
* **Owning Repo**: `score2gp`
* **Branch**: `feature/agy/m6-digit-merging-guard`
* **Target Files**: `src/score2gp/pdf.py`
* **Prompt**: `projects/score2gp/prompts/next/0046-m6-prevent-digit-over-merging.md`
* **Acceptance**:
  - Merged fret values never exceed `24`.
  - Consecutive single-digit notes (e.g., `7 10`) are preserved as separate candidates.
  - Governed by both in-situ and isolated tests (if value added).
