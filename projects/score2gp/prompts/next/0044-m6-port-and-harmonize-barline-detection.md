# 0044 — Port and Harmonize Barline Detection & Geometry Cleanup (CRP-01)

Status: APPROVED — unblocked by Task 88 target architecture and migration decision.

## Objective
Port valid barline detection thresholds from PR 418 into `src/score2gp/pdf.py`, revert the `outer_tolerance = 300.0` geometry snapping hack, and enforce staff-relative barline height bounds without mutating higher-level layout models.

## Start
1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `agy/crp-01-barline-detection-harmonization`.
3. Read `docs/design/2026-08-09-conversion-recovery-architecture.md` and `docs/design/2026-08-09-conversion-module-migration-map.md`.
4. Verify standard tests pass (`pytest` / `python3 scripts/agent_verify.py`).

## Allowed Files
- `src/score2gp/pdf.py`
- `src/score2gp/pdf_staff_notation_diagnostics.py`
- `tests/test_pdf_geometry_candidate_extractor.py`

## Implementation Specification
1. Update `pdf.py` barline height check from `height >= 20.0` to `height >= min(15.0, staff_height - 2.0)`.
2. Update inherited bar width check to `MIN_INHERITED_INTERNAL_BAR_WIDTH = 20.0`.
3. Revert `outer_tolerance` in `pdf.py` back to standard tight tolerance (`24.0pt`).
4. Re-enable `pdf_candidate_outside_system` warning gate.

## Acceptance Criteria
- `pytest tests/test_pdf_geometry_candidate_extractor.py` passes cleanly.
- `python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf` successfully extracts 43 notation barlines on `Lesson-5.pdf` without triggering 300pt snapping hacks.
- `python3 scripts/agent_verify.py` passes with zero regression.

## Deliverables
- Branch `agy/crp-01-barline-detection-harmonization` pushed to `origin`.
- Only allowed files modified.
- Pull Request opened on GitHub with exact-head author handback comment.
