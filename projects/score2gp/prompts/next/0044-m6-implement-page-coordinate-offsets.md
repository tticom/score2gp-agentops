# 0044 - M6: Implement Page Coordinate Offsets and Global Indexing

## Objective
Enable sequential measure tracking across page boundaries and compute cumulative page height coordinate offsets in the OMR candidate parser to prevent page-boundary index conflicts.

## Start
1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `feature/agy/m6-page-offsets`.
3. Read `projects/score2gp/reports/2026-08-09-master-conversion-failure-diagnosis.md`.
4. Verify standard tests pass.

## Implementation Scope & Seam Contract
Modify only `src/score2gp/pdf.py`:
1. **Sequential Page Indexing**: Update `_extract_pdf_text_candidates` to track `running_bar_index` dynamically across page iterations, passing it to `_detect_tab_systems` instead of re-initializing to 1 on page change.
2. **Cumulative Page Offsets**: Calculate global y-coordinate offsets by summing the heights of preceding pages (`page.rect.height`) to prevent candidate overlap and coordinate collisions.

## Validation Commands
1. Run sidecar generation on `Lesson-6.pdf`:
   ```bash
   ../score2gp/.venv/bin/score2gp generate-sidecar --pdf /home/tticom/work/score2gp-workspace/score2gp-private-fixtures/fixtures/private/Lesson-6.pdf --out /tmp/Lesson-6.mxl
   ```
2. Verify it outputs sequentially incrementing measures across all 6 pages.

## Deliverables
- Branch `feature/agy/m6-page-offsets` pushed to `origin`.
- Only `src/score2gp/pdf.py` changed.
- Pull Request opened on GitHub.

## Stop Conditions
- Global y-coordinate overflow or incorrect layout offsets causing bounding box validation errors.
