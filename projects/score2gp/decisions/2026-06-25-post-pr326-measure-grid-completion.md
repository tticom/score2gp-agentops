# Decision Record: PR #326 Measure-Grid Completion and Next Architecture Task

## Verified Baseline
- **Product PR:** https://github.com/tticom/score2gp/pull/326
- **Product PR Title:** diagnostic: add measure-grid structural evidence
- **Product PR State:** merged
- **Head SHA:** e63c4919d8cc488a69e2dd27d0ba0f3a4476c747
- **Merge Commit:** 7565e751e0dea624a209aeb4233373338296262a
- **Product Scope:** Added read-only `MeasureGridDiagnostics` payload exposing start/end X bounds for spatial measure regions. Uses confirmed internal barlines from structural-skeleton logic.
- **Explicit Non-capability:** No notation interpretation, no ScoreIR semantic changes, no rhythm recognition, no whole-note recognition, no GP export behaviour change.

## Fixture Evidence Recorded in PR #326
- `generated_standard_staff_quarter_note.pdf`: one measure region `[50.0, 550.0]`.
- `generated_standard_staff_multi_staff.pdf`: two measure regions per staff, `[50.0, 250.0]` and `[250.0, 545.28]`.
- `generated_standard_staff_ledger_lines.pdf`: one measure region `[50.0, 550.0]`.
- `generated_paired_notation_tab_system_double_barline.pdf`: one measure region, avoiding false empty regions from adjacent double barlines.

## Tests Recorded in PR #326
- `tests/test_pdf_measure_grid_diagnostics.py`: 5 passed.
- `tests/test_pdf_structural_skeleton_diagnostics.py`: 4 passed.

## Active Blocker
Score2GP now has structural measure-grid evidence, but it does not yet have verified evidence that detected notation candidates can be assigned into measure regions safely enough to support recognition work. Can structural skeleton + measure-grid diagnostics support candidate-to-measure spatial assignment on approved fixtures without relying on semantic recognition?

## Next Authorised Task
**Role:** Architect
**Task:** Conduct bounded research to test whether candidate-to-measure spatial assignment is viable using the newly merged structural diagnostics without needing notation semantics. Developer implementation remains strictly blocked until Reviewer architecture verification approves an approach.

The Architect must produce exactly one of the following outcomes:
- **Outcome A:** Candidate-to-measure spatial assignment is viable using the merged measure-grid and existing candidate geometry. Developer implementation may be proposed only after Reviewer architecture verification approves the approach.
- **Outcome B:** Measure-grid is useful but existing candidate evidence is insufficient. The Architect must define the smallest additional diagnostic evidence needed before implementation.
- **Outcome C:** Candidate-to-measure assignment is not viable with the current raster/vector diagnostics. No Developer work is authorised and a pivot is required.

**Stop/Pivot condition:** If existing diagnostics cannot support candidate-to-measure assignment, the Architect must not recommend implementation. They must choose Outcome B or Outcome C.

## Required Reviews
1. PR readiness review for this governance PR.
2. Reviewer architecture verification after the Architect research task.
