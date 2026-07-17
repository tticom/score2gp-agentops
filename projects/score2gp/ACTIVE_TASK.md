# Active Task

**Task**: Task 93: Standard Notation Sharp/Flat (Key Signature) Detection
**Authorised Role**: Developer, Architect, Reviewer, and Project Director
**Repository**: `tticom/score2gp`, `tticom/score2gp-agentops`, and the approved local fixture repository

## Status

APPROVED

## Task Authorised

Yes, branch and PR work authorized.

## Reason For This Promotion

The corrected Task 92 implementation is complete:
- Import boundary checks are fully generic and integrated into the verification suite.
- Standard convert refusing unsafe TAB-only extraction is verified.
- Labeled explicit approximate/draft path (--pdf-only-tab) is fully functional and covered by tests.

The next smallest implementation task is standard notation key signature detection, moving beyond the hardcoded 0 fifths fallback in MusicXML generation.

## Start State

- Canonical product worktree: `/home/tticom/work/score2gp-workspace/score2gp` on `feature/teamwork-corpus-conversion-accuracy-v0.1` at `34b7c2e5` (frozen).
- Recovery worktree: `/home/tticom/work/score2gp-workspace/score2gp-recovery` on `feature/task-92-import-check-auto-fallback` at `46ccf7cf`.
- PR #371 (Task 92) and PR #372 (Task 90 prerequisite) are open and stacked in the product repository.

## Permissions and Boundaries

- Tier 2 branch and PR work.
- Allowed product files to modify in `score2gp`:
  - `src/score2gp/deterministic_musicxml.py`
  - `src/score2gp/whole_note_recogniser.py`
  - `tests/` for verification
- Do not modify rhythm, duration, rest, or layout logic.
- Keep changes minimal and focused on standard staff sharp/flat candidate parsing and fifths attribute generation.

## Completion Evidence

1. Key signature (sharps/flats) is correctly recognized from standard staves and written to `deterministic_omr.musicxml` key fifths.
2. Neutral key is correctly omitted when unknown.
3. Tests and `python scripts/agent_verify.py` pass cleanly.
