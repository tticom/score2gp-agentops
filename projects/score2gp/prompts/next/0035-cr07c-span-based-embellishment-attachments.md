# 0035 - CR-07C Span-Based Embellishment Attachments for Palm Mute & Let Ring

## Objective

Implement bounded Developer slice `CR-07C` in `tticom/score2gp`, as authorized by the merged architecture report `docs/design/cr07-bounded-embellishment-attachments-architecture.md`.

Attach extracted span-based embellishment candidates (palm muting "P.M." and let ring "let ring") to target ScoreIR note techniques (`PalmMuteTechnique`, `LetRingTechnique`) using explicit event ID span ranges in `src/score2gp/tabraw.py` and `src/score2gp/build_ir.py`.

## Authorized Product Files

- `src/score2gp/tabraw.py`
- `src/score2gp/build_ir.py`
- `tests/test_cr07_embellishment_attachments.py`

No other product files in `src/` or `tests/` may be edited in this task. Do not edit `docs/design/cr07-bounded-embellishment-attachments-architecture.md` during this Developer implementation slice.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/next/0035-cr07c-span-based-embellishment-attachments.md`, `docs/design/cr07-bounded-embellishment-attachments-architecture.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/cr07c-span-based-embellishment-attachments` in `tticom/score2gp`.
6. Run `python scripts/agent_verify.py` in `score2gp` before making code modifications.

## Implementation Scope & Seam Contract

1. **`src/score2gp/tabraw.py`**:
   - Integrate span-based text/bracket candidates ("P.M.", "let ring") into candidate grouping and alignment data structures.

2. **`src/score2gp/build_ir.py`**:
   - Map span candidate onset and offset horizontal boundaries to corresponding event IDs.
   - Attach `PalmMuteTechnique` and `LetRingTechnique` to notes within the span range carrying `end_event_id`.

3. **`tests/test_cr07_embellishment_attachments.py`**:
   - Add integration tests verifying end-to-end attachment of palm mute and let ring span candidates into ScoreIR event objects and GPIF serialization.

## Validation Commands

1. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_cr07_embellishment_attachments.py`
2. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python scripts/agent_verify.py`

## Non-goals

- Audio/OMR pitch resolution changes and non-span embellishments are deferred.
