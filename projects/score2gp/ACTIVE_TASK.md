# Active Task

**Task**: CR-03: Repair Generic Meter Evidence and Emission
**Authorised Role**: Developer, Architect, Reviewer, and Project Director
**Repository**: `tticom/score2gp` (product) and `tticom/score2gp-agentops` (governance)

## Status

APPROVED

## Task Authorised

Yes, Tier 2 development, testing, and PR stacking authorized.

## Reason For This Promotion

CR-02 is completed. The Visual Output Probe and First-Divergence Ledger have proven that the duration heuristic misinterpretation of triplets (treating them as standard eighth notes, inflating measure ticks to 5760, and triggering the 4/4 overfull penalty) is the first divergence leading to the 12/8 time signature mismatch in `Lesson-5.pdf` (VO-01).

The next smallest task is CR-03 to implement generic, tuplet-aware or common-time aware meter resolution.

## Start State

- Canonical product worktree: `/home/tticom/work/score2gp-workspace/score2gp` on `feature/teamwork-corpus-conversion-accuracy-v0.1` at `34b7c2e5` (frozen).
- Recovery worktree: `/home/tticom/work/score2gp-workspace/score2gp-recovery` on `feature/task-92-import-check-auto-fallback` at `46ccf7cf`.
- PR #371 and PR #372 are open and stacked in the product repository.

## Permissions and Boundaries

- Allowed product files to modify in `score2gp`:
  - `src/score2gp/whole_note_recogniser.py`
  - `src/score2gp/deterministic_musicxml.py`
  - `tests/` for verification
- No other files are allowed to be modified.
- No reference GP data or hardcoded fixture mappings are permitted.
- The rule must remain generic to the entire corpus.

## Completion Evidence

1. `Lesson-5.pdf` is correctly parsed as 4/4 (no ghost half rests emitted).
2. Triplet eighth notes are correctly scaled when triplet indicators are present.
3. Tests and `python scripts/agent_verify.py` pass cleanly.
