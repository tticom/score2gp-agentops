# Decision Record — Authorise Multi-Staff Bridge Timing Developer Task

- **Status**: APPROVED
- **Role**: Supervisor
- **Date**: 2026-07-07

## 1. Context & Rationale
Following the merge of Governance PR #244 (merge commit: `d6f8d8fbb08eb12ebd3665f618b6fdf93401e179`), the Architect's research report has been recorded and approved (Outcome B). 
The report identified that the immediate timing blocker for multi-staff standard staff scores is in `notation_bridge.py`, which serializes candidates sequentially across staves and leads to duration overflow errors. To resolve this, we are now authorising a Developer task to implement parallel timing and track mapping at the bridge level.

## 2. Baselines
- **Product Merge Baseline**: Product PR #337 squash-merged at `eae13541de67899ff9563a09f48ed747171dea6b`.
- **Governance Merge Baseline**: Governance PR #244 squash-merged at `d6f8d8fbb08eb12ebd3665f618b6fdf93401e179`.

## 3. Selected Next Path
Option B — Bounded Developer implementation:
- **Title**: Developer implementation — multi-staff track separation and parallel timing in `notation_bridge.py`
- **Role**: Developer
- **Loop Tier**: Tier A (Full Loop)

## 4. Scope & Non-goals
- **Approved Scope**: Modifying `src/score2gp/notation_bridge.py` and `tests/test_notation_bridge.py` to map distinct `staff_index` values to separate tracks, and track onset ticks independently per track.
- **Explicitly Blocked**:
  - True polyphony or voice separation.
  - Same-staff multi-voice support.
  - Changing OMR candidate extraction logic.
  - Changing staff geometry diagnostics or extraction.
  - Committing new PDF or GP fixtures.
  - Modifying the GP writer (`gpif.py`, `gp_package.py`) unless strictly necessary and separately justified.

## 5. Review Sequence
1. Developer implementation.
2. Reviewer implementation conformance review (after Developer opens the product PR).
3. Reviewer PR readiness review (before merge).

## 6. Constraints & Stop Conditions
- Stop if the current data model cannot represent independent staff/track timing safely.
- Stop if product files outside authorised scope must be modified.
- Stop if private/copyrighted PDFs are required.
- Stop if tests cannot prove behaviour from safe committed data.
- No private/copyrighted PDFs may be processed.
- No new generated PDFs, GP files, screenshots, logs, or dumps may be committed to git.
