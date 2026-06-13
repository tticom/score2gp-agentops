# Decision: Authorise Product Task 105 (Whole-Note Recognition Outcome Mapping)

## Context
Product PR #258 has merged. It strengthened the diagnostics gate by making expected whole-note candidate counts explicit and fail-fast. This robust diagnostic foundation gives us the safer evidence we need to take our first concrete step toward actual product functionality. The overarching goal is to move from diagnostics-only processing to visible product progress, starting with a minimal, reviewable piece of whole-note recognition.

## Evidence
- **Product PR**: [#258](https://github.com/tticom/score2gp/pull/258)
- **Head SHA**: `7ce22047a567237b8b795fa446670d02d3efb861`
- **Merge Commit SHA**: `1527cfed8ee1f67fd4cf2dedbde66d936ad1a65b`
- **Changed Files in PR #258**:
  - `scripts/raster_diagnostics_gate_report.py`
  - `tests/test_raster_diagnostics_gate_report.py`
- **Validation**:
  - `PYTHONPATH=. .venv/bin/pytest tests/test_raster_diagnostics_gate_report.py` completed with 28 passed in 18.82s.
  - Test coverage directly asserts exact `whole_note_candidate_count_gate_status`, verification of failure checks via zero mismatches, unexpected half-notes, and unexpected blanks explicitly triggering `FAIL` on aggregate diagnostics.
  - Live fixture evidence reported via PR body confirmed that `generated_standard_staff_whole_note.pdf` evaluates to exactly 2 candidates.

## Next Direction
Because our diagnostics gating precisely detects any mismatches or regressions in candidate expectations, we are secure in leveraging this data.
We will now execute Product Task 105. This task will consume the existing whole-note candidate evidence and map it to a read-only recognition/conversion outcome for the safe public whole-note fixture, without impacting any other components or diagnostics.

## Acceptance Criteria for Product Task 105
- Implement a first read-only whole-note recognition outcome mapping.
- The outcome mapping only translates validated candidates (already exposed by diagnostics) into a recognition representation.
- Ensure no diagnostics or existing validations are weakened or removed.
- Produce output only for the safe public generated whole-note fixture without touching unrelated symbol recognition or exporting broad GP/MusicXML.
- Include a small, targeted test for this specific conversion outcome.

## Non-goals
- Do not implement broad music recognition.
- Do not attempt full MusicXML/GP export unless the existing code already has a narrow safe insertion point.
- Do not alter candidate detection thresholds unless evidence proves that is necessary.
- Do not add or commit private PDFs.
- Do not remove diagnostics or weaken existing tests.
- Do not update large documentation files unless needed for continuity.

## Next Recommended Action
Next recommended action: after this governance PR is merged, create the Product Task 105 executable prompt in ChatGPT.
