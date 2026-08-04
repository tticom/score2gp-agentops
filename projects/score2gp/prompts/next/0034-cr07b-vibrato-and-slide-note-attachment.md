# 0034 - CR-07B Proximity & String-Identity Note Attachment for Visual Vibrato and Slide Evidence

## Objective

Implement bounded Developer slice `CR-07B` in `tticom/score2gp`, as authorized by the merged architecture report `docs/design/cr07-bounded-embellishment-attachments-architecture.md`.

Attach extracted `VisualVibratoEvidence` and `VisualSlideEvidence` candidates from the PDF drawing extraction seam to target ScoreIR note techniques (`VibratoTechnique`, `SlideTechnique`) in `src/score2gp/tabraw.py` and `src/score2gp/build_ir.py`.

## Authorized Product Files

- `src/score2gp/tabraw.py`
- `src/score2gp/build_ir.py`
- `tests/test_cr07_embellishment_attachments.py`

No other product files in `src/` or `tests/` may be edited in this task. Do not edit `docs/design/cr07-bounded-embellishment-attachments-architecture.md` during this Developer implementation slice.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/next/0034-cr07b-vibrato-and-slide-note-attachment.md`, `docs/design/cr07-bounded-embellishment-attachments-architecture.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/cr07b-vibrato-and-slide-note-attachment` in `tticom/score2gp`.
6. Run `python scripts/agent_verify.py` in `score2gp` before making code modifications.

## Implementation Scope & Seam Contract

1. **`src/score2gp/tabraw.py`**:
   - Integrate `VisualVibratoEvidence` and `VisualSlideEvidence` candidate lists into candidate grouping and alignment data structures.

2. **`src/score2gp/build_ir.py`**:
   - Attach visual vibrato candidates to the note/chord event at the corresponding staff index within horizontal proximity. Propagate chordal vibrato to all notes in the target chord.
   - Attach visual slide candidates to sequential notes/events sharing the same string identity (or adjacent coordinates). Set `SlideTechnique` on the source note.

3. **`tests/test_cr07_embellishment_attachments.py`**:
   - Add integration tests verifying end-to-end attachment of visual vibrato and slide candidates into ScoreIR event objects.

## Validation Commands

1. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_cr07_embellishment_attachments.py`
2. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python scripts/agent_verify.py`

## Non-goals

- Span-based embellishments (palm muting, let ring) and audio/OMR pitch resolution changes are deferred.
