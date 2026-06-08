# Standard-Staff Fixture Coverage Review
**Date:** 2026-06-08
**Reviewer:** Antigravity

> [!WARNING]
> **PROVISIONAL / SUPERSEDED**
> This review was merged prematurely based on accumulated branch state rather than verified product main after Tasks 1–4. Task 4 was not yet merged at the time of this review.
> It must not be used to authorize semantic interpretation work. A corrected coverage review is required after Task 4 is merged and verified on product main.

## Context
Tasks 1–4 from `APPROVED_TASK_QUEUE.md` established a set of purely geometric standard-staff fixtures designed to test staff geometry parsing without introducing musical semantics. The objective of this review is to determine whether the fixture coverage and the exposed diagnostic schema (`PdfStaffNotationGeometryDiagnostics`) are sufficient to support the next product implementation stage.

## Executed Commands and Test Results
To validate coverage, the following tests were run on the accumulated branch containing the Tasks 1-4 fixtures:

```bash
cd /home/tticom/work/score2gp-workspace/score2gp
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py
.venv/bin/python -m pytest tests/test_pdf_staff_geometry_diagnostics.py
```

**Results:**
- `test_pdf_standard_staff_diagnostics_fixtures.py`: 8 passed
- `test_pdf_staff_geometry_diagnostics.py`: 13 passed

## Fixture Coverage
1. **Dense Left Margins (Task 1):** Verified. Tests correctly ensure that dense margin primitives are correctly binned into left-margin counts.
2. **Sparse Baseline (Task 2):** Verified. Tests correctly assert that a sparse, zero-primitive margin reflects zero counts in `margin_text_span_count` and similar left margin fields.
3. **Wide Curves (Task 3):** Verified. Tests assert the presence of wide curve candidate metrics without assuming musical meaning (slur/tie).
4. **Complex Primitive Clusters (Task 4):** Verified. Tests assert that complex clusters containing stems, noteheads, and ledger lines are grouped correctly and reflected in `x_aligned_cluster_count` and primitive summary metrics.

## Diagnostic Schema Stability
The schema exposed in `src/score2gp/pdf_staff_geometry.py` provides extremely granular morphological statistics:
- `x_aligned_cluster_count`
- `max_primitives_per_x_aligned_cluster`
- `clusters_with_vertical_stroke_candidate`
- `cluster_primitive_count_summary`
- Left margin text and curve aggregations.

This geometric abstraction perfectly fulfills the strict requirement to avoid semantic leaps before the infrastructure is ready. The schema is stable, highly observable, and decoupled from any semantic rule engines (ScoreIR).

## Verdict
**Verdict:** `fixtures sufficient for next stage`

The standard-staff geometry diagnostic layer is robust enough to proceed.

## Next Task Recommendation
**Proposed Next Task:** Start the geometric-to-semantic interpretation layer for standard-staff clusters.
**Description:** Add a bounded module that translates the geometric groupings (`x_aligned_clusters`) into neutral semantic primitives (e.g., NoteheadCandidate, StemCandidate) without yet committing to final musical semantics (Pitch, Duration).
