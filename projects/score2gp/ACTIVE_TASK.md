# Active Task

**Task**: Task 93 — Sidecar Bake-Off & 4/4 Triplet Discriminator (CRP-05)
**Status**: MERGED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/crp-05-sidecar-bake-off`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0048-timing-complete-sidecar-bakeoff.md`

## Context

Task 92 (CRP-04) enforced process-level reference isolation in `scripts/private_e2e_smoke.py` and established `tests/test_real_source_oracles.py`.
Task 93 (CRP-05) is the fifth stage of the Conversion Recovery Programme. It evaluates Audiveris batch sidecar output vs Score2GP internal topology-first timing adapter on `src/score2gp/notation_omr/timeline.py` using `Lesson-6.pdf` 4/4 triplets as the mandatory discriminator.

## Goal

Implement `tests/test_sidecar_bakeoff.py` and refine `src/score2gp/notation_omr/timeline.py` to evaluate sidecar OMR options against `Lesson-6.pdf` 4/4 triplets with balanced measure capacities, selecting Outcome A (Score2GP internal topology-first timing adapter) or Outcome B (sidecar hybrid).

## Allowed Files

- `src/score2gp/notation_omr/timeline.py`
- `tests/test_sidecar_bakeoff.py`

## Non-goals

- Do not add unverified third-party production dependencies.
- Do not pass reference `.gp` files to the sidecar generator process.
- Do not introduce fixture-specific coordinate bounds or hash checks.

## Acceptance

- `pytest tests/test_sidecar_bakeoff.py` passes cleanly and evaluates `Lesson-6.pdf` 4/4 triplet timing without dropping measure capacity.
- `python3 scripts/agent_verify.py` passes with zero regression.
