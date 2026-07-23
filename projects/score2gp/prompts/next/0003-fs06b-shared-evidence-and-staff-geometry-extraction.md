# 0003 - FS-06B Shared Evidence and Staff Geometry Extraction

## Objective

Make the first behaviour-preserving extraction from src/score2gp/whole_note_recogniser.py into score2gp.notation_omr. Move only the six source functions named below, retaining whole_note_recogniser.py as the compatibility import surface.

## Start

1. Work only in canonical Ubuntu WSL paths under /home/tticom/work/score2gp-workspace.
2. Confirm gh auth status identifies tticom-automation and the product repository Git identity is tticom-automation with tticomautomation@gmail.com.
3. Read ACTIVE_TASK.md, AGENT_CONTROL.md, and this prompt.
4. Fetch origin/main. If the product worktree is not clean, stop and report; do not reset, clean, delete, or repair unrelated files.
5. Create agy/fs06b-shared-evidence-staff-geometry from origin/main.

## Allowed Product Files

- [NEW] src/score2gp/notation_omr/__init__.py
- [NEW] src/score2gp/notation_omr/evidence.py
- [NEW] src/score2gp/notation_omr/staff_geometry.py
- [MODIFY] src/score2gp/whole_note_recogniser.py
- [NEW] tests/test_notation_omr_staff_geometry.py

## Required Extraction

Move these functions without changing signatures, dictionary shapes, or behaviour:

- To evidence.py: shape_candidate_evidence.
- To staff_geometry.py: shape_ledger_line_candidate_evidence, map_ledger_line_candidates_to_read_only_outcomes, map_staff_geometry_to_read_only_report, _associate_staves, and map_ledger_lines_to_note_candidates.

whole_note_recogniser.py must import and re-export each moved function under its current name. Preserve test patch points at src.score2gp.whole_note_recogniser.

## Validation

Run:

    pytest tests/test_whole_note_staff_association.py tests/test_note_candidate_recognition_report.py tests/test_notation_omr_staff_geometry.py
    pytest
    git diff --check origin/main...HEAD

Add direct tests for the new module imports and at least one representative behaviour path for both evidence.py and staff_geometry.py. Do not weaken, delete, or rewrite existing tests merely to accommodate the move.

## Publish

1. Commit only the allowed product files.
2. Push normally and open exactly one product PR.
3. State the exact head SHA, moved symbols, focused and full test results, and any residual risk in the PR body.
4. Do not merge, force-push, use tokens or credential files, reset, clean, use admin flags, or open another PR.
5. Stop at READY_FOR_CODEX_REVIEW.
