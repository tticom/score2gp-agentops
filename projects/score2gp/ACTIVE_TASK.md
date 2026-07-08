# Active Task

**Task**: Req-114 / Task 48: Implement quarter rest extraction
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Executable Task
Yes

## Completion Evidence
Developer must create a function to extract `QuarterRestCandidate` from `GeometryCandidateSet` using the Architect's bounding box heuristics.

## 1. Baseline
- The Architect's quarter rest extraction proposal was merged in PR #351.
- The Reviewer approved the proposal in PR #267.
- `GeometryCandidateSet` contains `x_aligned_clusters` with primitives.

## 2. Context
We need to extract quarter rests from the staff body geometry. This allows us to start processing rhythmic elements independently of pitch.

## 3. Goal
Create a new module `src/score2gp/pdf_candidate_quarter_rest.py` with the function `extract_quarter_rest_candidates(geometry: GeometryCandidateSet, staff_spacing: float, staff_center_y: float) -> list[QuarterRestCandidate]`.
Implement the heuristic:
1. `primitive_count == 1` and `kind` in (`text_span`, `curve`, `vertical_stroke`).
2. `height / staff_spacing` between 2.0 and 4.0.
3. `height / width` > 1.5.
4. Vertical midpoint within 0.5 staff spaces of `staff_center_y`.

## 4. Non-goals
- Do not extract other rests or notes.
- Do not build ScoreIR events.
- Do not handle polyphony or overlapping primitives in this pass.

## 5. Required Output & Outcome
A product PR with the implementation and tests proving a quarter rest candidate is successfully returned when given a valid `x_aligned_cluster`.

## 6. Next Steps
- After Developer PR merges, run Reviewer implementation conformance.
