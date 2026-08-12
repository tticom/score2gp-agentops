# Active Task

**Task**: Task 99 — Biomechanical Fretboard Position Optimizer & TAB Token Ownership (CRP-11)
**Status**: MERGED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/crp-11-tab-token-and-fretboard-ownership`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0054-tab-token-and-fretboard-ownership.md`

## Context

Task 98 (CRP-10) implemented topologically locked bar timelines (`TopologicallyLockedBarTimeline` and `resolve_tuplet_duration`) in `src/score2gp/notation_omr/timeline.py`.
Task 99 (CRP-11) is the eleventh stage of the Conversion Recovery Programme. It recognizes context-aware fret tokens and string ownership, separating observed visual TAB digits from inferred fretboard positions using biomechanical hand-position optimization.

## Goal

Implement `tests/test_tab_token_and_fretboard_ownership.py` and refine `src/score2gp/notation_omr/position_optimizer.py` and `pipeline.py` to optimize fretboard assignments and enforce string/fret ownership invariants.

## Allowed Files

- `src/score2gp/notation_omr/position_optimizer.py`
- `src/score2gp/notation_omr/pipeline.py`
- `tests/test_tab_token_and_fretboard_ownership.py`

## Non-goals

- Do not synthesize open strings or guess unevidenced TAB frets.
- Do not pass reference `.gp` files to the position optimizer.
- Do not introduce fixture-specific coordinate bounds or hash checks.

## Acceptance

- `pytest tests/test_tab_token_and_fretboard_ownership.py` passes cleanly and verifies fretboard position optimization, string ownership, and observed/inferred distinction.
- `python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf` preserves visual TAB string and fret candidates.
- `python3 scripts/agent_verify.py` passes with zero regression.
