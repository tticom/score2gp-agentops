# Decision: PR #330 Read-Only StaffPositionDiagnostics Merged

**Date:** 2026-06-27
**Product PR:** [tticom/score2gp#330](https://github.com/tticom/score2gp/pull/330)
**Reviewed Head SHA:** `2c1b7a1f3de0cb2be38926f3627faeadd4bde430`
**Merge Commit:** `dc511e6f663c08c180e1beae473c5b0d31f31bc4`

## 1. Summary
Product PR #330 has been successfully merged into `main`, introducing a read-only `StaffPositionDiagnostics` capability. This diagnostic calculates geometric staff-relative vertical positions (`staff_step_index`) for candidate notations using `MeasureBucketDiagnostics` and `NotationStaffGeometry`.

## 2. Changes and Validation
- **Exact files changed**: `src/score2gp/pdf_staff_position_diagnostics.py`, `tests/test_pdf_staff_position_diagnostics.py`.
- **Validation**: All 39 focused and broad tests passed.
- **Review Threads**: Both Codex P2 threads (partial geometry, off-grid centers) were resolved and fixes validated.
- **Scope Guard**: Zero semantic changes. Pitch, clef, rhythm, and ScoreIR were untouched. No private artifacts were committed.

## 3. Explicit Limitations
- The diagnostic enforces exactly 5 staff lines; partial geometries fall back to `ambiguous_vertical_position`.
- Candidates must snap to the grid within `OFF_GRID_TOLERANCE = 0.25` or are flagged `ambiguous_vertical_position` (and `off_grid_candidate_center`).
- Noteheads with stems (quarter, half notes) intentionally preserve `ambiguous_notehead_center`.
- **No semantic pitch** is inferred. Pitch requires clef context, which this diagnostic explicitly avoids.

## 4. Next Active Blocker
The new blocker is determining whether this strictly geometric staff-position evidence is sufficient to support the next concrete note-recognition step, or if further diagnostics/architecture work is required first.

## 5. Next Authorised Task
**Architect diagnostic task:** use the merged read-only `StaffPositionDiagnostics` capability on committed safe fixtures to evaluate the evidence and decide the next viable recognition path. No semantic implementation is authorised.
