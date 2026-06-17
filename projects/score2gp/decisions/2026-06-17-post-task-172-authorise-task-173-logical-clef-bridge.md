# Decision Record: Post-Task 172 — Authorise Task 173 Logical Clef Bridge

## Date
2026-06-17

## Context
Product Task 172 successfully implemented a conservative, deterministic, diagnostic-only logical clef candidate extractor/classifier over existing `LeftMarginPrimitiveCandidate` evidence in the `tticom/score2gp` repository.

### Product Task 172 Completion Summary
The logical clef classifier evaluates text span primitives independently and groups compatible curve primitives into combined bounding boxes when their proximity is within `staff_spacing`. It emits `treble_clef_candidate` only when unambiguous strong proportional evidence matches the thresholds and safely returns `unknown` for missing, weak, malformed, ambiguous, or competing evidence. It strictly maintains a diagnostic boundary and does not bridge into pitch mapping, alter raster diagnostics, alter `assumed_treble_pitch`, or declare `clef_resolved_staff_pitch` semantics.

### Prerequisite Verification
* **Governance PR #180:** Verified merged.
* **Product PR #290:** Verified merged.

### Product PR #291 Live Merge Evidence
* **State:** merged
* **Final Head SHA:** `b8be33b92f9e757886d1f4bc2f12c71dd384abd1`
* **Merge Commit:** `e4d010b31ca0fe034d4ce98173a5ac141c2386d0`
* **Changed Files:** 2 files (`src/score2gp/logical_clef_candidate_classifier.py`, `tests/test_logical_clef_candidate_classifier.py`)

### Validation Evidence from PR #291
* `.venv/bin/pytest tests/test_logical_clef_candidate_classifier.py`: 12/12 tests passed in 0.15s.
* `git diff --check`: Passed cleanly.

### Codex Disposition for PR #291
Two Codex P2 blockers were addressed in Product Task 172:
1. Trailing whitespace in the new module/test files was purged.
2. The classifier was updated to group compatible `curve` primitives into a combined bounding box before applying proportional thresholds. Competing candidate groups correctly fail closed to `unknown` rather than unsafely picking the tallest primitive.

### Safety and Privacy/Artifact Hygiene
Clean output verified. No sensitive artifacts, private fixtures, logs, PDFs, GP files, scratch files, or unapproved dependencies were committed.

## Current Limitation
The logical clef candidate evidence exists but is solely diagnostic; it is not yet bridged into the clef-resolved pitch mapping pipeline. Task 170's coverage analysis identified that 14/14 note candidates were skipped due to missing clef evidence.

## Reason for Product Task 173
Task 170’s dominant blocker was missing clef evidence. Product Task 172 successfully created bounded logical clef candidate evidence suitable for a bridge. Task 173 will bridge this evidence into read-only diagnostic/coverage mapping to reduce the missing-clef blocker in coverage reports.

## Explicit Boundary
Product Task 173 may bridge evidence into read-only diagnostic/coverage mapping **only**. It must not declare canonical pitch output or implement playable output. It must maintain the strict fail-closed boundary for ambiguous/weak clef evidence.
