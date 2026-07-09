# Active Task

**Task**: Req-131 / Task 80: Implement read-only rhythm timeline diagnostics
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Developer must implement the `build_staff_timeline_preview` helper in `whole_note_recogniser.py` (reconstructing measure-local tick timelines and rest assignments as read-only preview diagnostics), write unit/integration tests, pass verification, push the branch, and open a product PR.

## 1. Baseline
- Req-131 rest/rhythm timeline schema is designed and approved.
- Clef, rest, and pitch mappings are implemented and tested.

## 2. Context
Having approved the rhythm timeline schema, we can now implement the timeline reconstruction logic in a safe, read-only diagnostic preview block.

## 3. Goal
Implement the timeline preview generator inside `score2gp`, collecting note/rest durations, updating voice cursors, resetting at barlines, and outputting to `"timeline_preview"`.

## 4. Non-goals
- Do not modify core ScoreIR translation logic.
- Do not modify playable GP export.

## 5. Scope
Allowed files:
- `src/score2gp/whole_note_recogniser.py`
- `tests/` unit/integration tests for rhythm diagnostics

## 6. Suggested Work Branch
`feature/req-131-rhythm-diagnostics-v0.1`

## 7. Required Validation
Run the full verification suite `make verify`.

## 8. Acceptance Criteria
- Timeline preview logic is implemented.
- Correctly assigns quarter, half, whole rests.
- Resets at barlines and clusters notes into vertical time slices.
- Outputs diagnostics strictly under `"timeline_preview"`.
- `make verify` passes.

## 9. Next Steps
- Review Req-131 read-only rhythm timeline diagnostics implementation.
