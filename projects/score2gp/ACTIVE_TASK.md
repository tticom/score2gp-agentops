# Active Task

**Task**: CR-04C: Final-Event Duration Consistency Architecture
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect / Diagnostic Engineer
**Repository**: tticom/score2gp-agentops
**PR Branch**: `agy/cr04c-final-event-duration-consistency-architecture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0010-cr04c-final-event-duration-consistency-architecture.md`

## Context

Following product merge commit `f47194e57b551d4b571a04c0b7641fbe9c173f80` (CR-04B `--tempo-bpm` explicit CLI override) and PR #396 (`ea720c353af0926bede1980d55479db77c22aa58`), this task executes prompt `0010-cr04c-final-event-duration-consistency-architecture.md`.

## Goal

Resolve the smallest correct representation for PDF-only TabRaw final events whose padded `duration_ticks` disagree with their `notated_duration`, and turn that decision into a bounded, public-testable Developer authorization.

## Allowed Files

- `projects/score2gp/research/` (in `score2gp-agentops`)
- `projects/score2gp/reports/` (in `score2gp-agentops`)
- `projects/score2gp/prompts/next/` (in `score2gp-agentops`)
- `projects/score2gp/ACTIVE_TASK.md` (in `score2gp-agentops`)
- `projects/score2gp/prompts/NEXT.md` (in `score2gp-agentops`)

## Non-goals

No edits to product code in `score2gp` during this Architect phase.

## Acceptance

Comprehensive architecture and decision record written selecting exactly one smallest implementation path for final-event duration consistency.
