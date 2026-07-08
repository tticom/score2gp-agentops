# Active Task

**Task**: Req-109 / Task 36: feat(pdf): expose primitive-level geometry diagnostics
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Executable Task
Yes

## Completion Evidence
Developer must ensure `PrimitiveGeometry` instances are cleanly serialized and made available to downstream processes in the diagnostic payload, commit to `score2gp`, push the branch, and open a PR.

## 1. Baseline
- The backwards compatibility test for geometry diagnostics (Req-108) has been completed and merged.
- The governance PR lane is clean.

## 2. Context
Currently, the extraction process relies heavily on aggregate counts of primitives. To perform actual optical candidate extraction, we need the actual bounding box geometries (`x0, y0, x1, y1`) of individual primitives to be serialized and available downstream.

## 3. Active Blocker
Subsequent optical candidate extraction tasks cannot proceed until the raw primitive geometries are available in the diagnostics payload.

## 4. Goal
Ensure `PrimitiveGeometry` instances (with real `x0/y0/x1/y1` fields) are cleanly serialized in the diagnostics model and payloads, removing reliance on aggregate counts and unblocking optical candidate extraction.

## 5. Non-goals
- Do not build candidate extractors themselves yet.
- Do not implement complex heuristic geometric mapping.
- No semantic candidates or interpretation.

## 6. Repo Scope
- **Allow**:
  - `src/score2gp/pdf_staff_geometry.py`
  - `src/score2gp/pdf_staff_notation_diagnostics.py`
  - `tests/test_pdf_geometry_diagnostics.py` or similar
- **Stop before changing**:
  - `ACTIVE_TASK.md` (once authorised)
  - Unrelated product code files.

## 7. Branch Suggestion
`feature/primitive-geometry-diagnostics-v0.1`

## 8. Required Output & Outcome
A product PR implementing primitive-level geometry diagnostics serialization, with corresponding test validation.

## 9. Incremental Progress Check
- **What new evidence will this task produce?**: Tests proving primitive bounding boxes are correctly serialized.
- **Which prior result must it not merely repeat?**: Must expand existing diagnostic schema beyond aggregate counts to explicit geometry coordinates.
- **How will we know the task moved the project forward?**: A PR enabling primitive serialization is opened.
- **What is the smallest next decision this task enables?**: Proceeding with extraction of specific candidate types like curves or vertical bars.

## 10. Next Steps
- Promote the next available Epic B task (e.g., Task 33: geometry candidate layer review).
