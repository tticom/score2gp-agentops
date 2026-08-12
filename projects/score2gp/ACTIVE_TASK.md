# Active Task

**Task**: Task 98 — Musical Timeline Replacement (CRP-10)
**Status**: PROMOTED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/crp-10-musical-timeline-replacement`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0053-musical-timeline-replacement.md`

## Context

Task 97 (CRP-09) implemented topology-bound evidence fusion across notation and TAB staves (`PairedStaffEvidenceFusion` and `PairedStaffFusionEngine`) in `src/score2gp/notation_omr/evidence.py`.
Task 98 (CRP-10) is the tenth stage of the Conversion Recovery Programme. It replaces unbounded single-measure aggregation with topologically locked bar timelines, establishing one owner of timing truth (metre, tuplets, voices, rests, onsets, durations, and bar capacity invariants).

## Goal

Implement `tests/test_musical_timeline_replacement.py` and refine `src/score2gp/notation_omr/timeline.py` and `pipeline.py` to enforce metre, tuplets, voices, rests, onsets, durations, and bar capacity invariants under a single owner of timing truth.

## Allowed Files

- `src/score2gp/notation_omr/timeline.py`
- `src/score2gp/notation_omr/pipeline.py`
- `tests/test_musical_timeline_replacement.py`

## Non-goals

- Do not perform scaling, truncation, padding, deduplication, or auto-partition hacks to hide missing timing evidence.
- Do not pass reference `.gp` files to the timeline pipeline.
- Do not introduce fixture-specific coordinate bounds or hash checks.

## Acceptance

- `pytest tests/test_musical_timeline_replacement.py` passes cleanly and verifies musical timeline reconstruction, bar capacity invariants, and triplet timing.
- `python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-6.pdf` preserves 4/4 triplet timing without synthetic scaling or partition hacks.
- `python3 scripts/agent_verify.py` passes with zero regression.
