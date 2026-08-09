# 0044 - M6: Port and Harmonize Barline Detection

## Objective
Update the OMR pipeline and barline thresholds to accept compact notation barlines, resolve edge double barlines, and inherit notation staff barlines cleanly to prevent `partial_pdf_grouping` refusals on compact scores (e.g. `Lesson-5.pdf`).

## Start
1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `feature/agy/m6-barline-harmonization`.
3. Read `projects/score2gp/reports/2026-08-09-master-conversion-failure-diagnosis.md`.
4. Verify standard tests pass.

## Implementation Scope & Seam Contract
Modify only the barline extraction and mapping modules:
1. **Compact Barline Thresholds**: In `src/score2gp/pdf.py`, modify:
   - `MIN_INHERITED_INTERNAL_BAR_WIDTH` from `130.0` to `20.0` points.
   - Relative height checks in `filter_tab_barline_candidates` from `height >= 20.0` to `height >= min(15.0, staff_height - 2.0)`.
2. **Edge Double Barlines**: Update mixed-primitive checks in `filter_tab_barline_candidates` to resolve representative edge barlines within `10.0` points of the system boundaries, rather than marking them ambiguous.
3. **Notation Staff Inheritance**: Update `src/score2gp/notation_omr/pipeline.py` to extract confirmed barlines from standard notation staves (using `extract_structural_skeleton_diagnostics_dict`) and merge them into `barline_locations` while deduplicating against TAB-inherited barlines.
4. **Isolated Unit Testing**: If isolated unit testing adds coverage value, write/update a separate unit test using public/synthetic inputs that can run in GitHub Actions.

## Validation Commands
1. Run sidecar generation on `Lesson-5.pdf`:
   ```bash
   ../score2gp/.venv/bin/score2gp generate-sidecar --pdf /home/tticom/work/score2gp-workspace/score2gp-private-fixtures/fixtures/private/Lesson-5.pdf --out /tmp/Lesson-5.mxl
   ```
2. Unzip and verify it contains exactly `38` measures:
   ```bash
   unzip -p /tmp/Lesson-5.mxl | grep -c "<measure"
   ```
3. Run the standard test suite:
   ```bash
   PYTHONPATH=. .venv/bin/python3 -m pytest
   ```

## Deliverables
- Branch `feature/agy/m6-barline-harmonization` pushed to `origin`.
- Only `src/score2gp/pdf.py` and `src/score2gp/notation_omr/pipeline.py` changed.
- Pull Request opened on GitHub.

## Stop Conditions
- Standard unit tests fail post-implementation.
- `Lesson-5.pdf` sidecar fails to generate or has a measure count other than `38`.
