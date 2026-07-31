# Active Task

**Task**: CR-04A: Current-Runtime Lesson-5 Evidence Replay
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect / Diagnostic Engineer
**Repository**: tticom/score2gp-agentops
**PR Branch**: `agy/cr04a-current-runtime-evidence-replay`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0008-cr04a-current-runtime-evidence-replay.md`

## Context

Following the completion of the CR-04A architecture pass (`2026-07-24-cr04a-architecture.md`), the historical Lesson-5 false rest defect was classified as `OBSERVABILITY_GAP`. This task executes the current-runtime Lesson-5 evidence replay to determine whether the false half rest persists on current `main`.

## Goal

Determine whether the false 1920-tick half rest recorded by the historical Lesson-5 ledger still enters the current conversion path at product main `ea720c353af0926bede1980d55479db77c22aa58`. Produce the smallest next decision from current evidence.

## Allowed Files

- `projects/score2gp/reports/2026-07-24-cr04a-current-runtime-replay.md` (in `score2gp-agentops`)
- `projects/score2gp/prompts/next/` (in `score2gp-agentops`)
- `projects/score2gp/ACTIVE_TASK.md` (in `score2gp-agentops`)
- `projects/score2gp/prompts/NEXT.md` (in `score2gp-agentops`)

## Non-goals

No edits to product code in `score2gp` during this Architect phase.

## Acceptance

Runtime replay report written with exact sanitized candidate extraction facts, bridge outcomes, decision gate classification, and synchronized NEXT prompts.
