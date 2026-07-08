# Active Task

**Task**: Req-104 / Task 25: Add PDF geometry candidate extraction diagnostics skeleton
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status

APPROVED

## Executable Task

Yes

## Completion Evidence
Developer must implement the candidate extractor skeleton, commit to `score2gp`, push the branch, and open a PR.

## 1. Baseline
- Reviewer verified that the Architect's single-prompt autonomous cycle was blocked (Req-102 returned `cannot verify`).
- Pivot to Epic B (Geometry Candidate Extraction) to maintain momentum.
- Product baseline is post-schema-snapshot.

## 2. Context
As part of the geometry candidate extraction architecture (Epic B), we need a skeleton extractor function. This function will accept `NotationStaffDiagnostics` and return a minimal `GeometryCandidateSet`. This establishes the structural boundary without yet implementing extraction logic.

## 3. Active Blocker
Subsequent extraction tasks (like extracting specific curve or rectangle candidates) cannot proceed until the fundamental extraction function signature and models are present.

## 4. Goal
Add a pure function that accepts `NotationStaffDiagnostics` and returns an empty or minimal `GeometryCandidateSet`, without implementing extraction rules yet.

## 5. Non-goals
- No real extraction rules beyond pass-through metadata.
- No parser integration.
- No ScoreIR emission.
- No semantic candidates (forbidden semantic leakage).

## 6. Repo Scope
- **Allow**:
  - `src/score2gp/pdf_geometry_candidate_extraction.py`
  - `src/score2gp/pdf_geometry_candidates.py`
  - `tests/test_pdf_geometry_candidate_extraction.py`
- **Stop before changing**:
  - `ACTIVE_TASK.md` (once authorised).
  - any unrelated product files.

## 7. Branch Suggestion
`feature/geometry-candidate-extractor-skeleton-v0.1`

## 8. Required Output & Outcome
A PR in `score2gp` implementing the skeleton function with tests verifying its signature and anti-semantic properties.

## 9. Incremental Progress Check
- **What new evidence will this task produce?**: Tests proving the extraction function can be called.
- **Which prior result must it not merely repeat?**: Must build upon existing raw diagnostics to introduce the new candidate layer.
- **How will we know the task moved the project forward?**: A PR implementing the extractor interface is opened.
- **What is the smallest next decision this task enables?**: Proceeding to add actual extraction logic for curves and snapshots (Req-105).

## 10. Next Steps
- Promote Req-105 (Task 29) to add candidate extraction JSON snapshot tests.
