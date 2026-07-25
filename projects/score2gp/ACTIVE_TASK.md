# Active Task

**Task**: CR-04C: Final-Event Duration Consistency Architecture Decision
**Authorised Role**: Architect (Tier B)
**Repository**: tticom/score2gp-agentops
**Product Repository**: tticom/score2gp
**Product Base**: f47194e57b551d4b571a04c0b7641fbe9c173f80

## Status

COMPLETED — ARCHITECTURE RESOLVED (PROMPT 0011 AUTHORIZED FOR DEVELOPER IMPLEMENTATION)

## Context

CR-04C Architecture decision resolved the PDF-only TabRaw final-event duration padding inconsistency.
Option A was selected: final note duration is set to `grid_spacing` (matching `notated_duration`), and any remaining measure capacity $R = 3840 - \text{current\_onset}$ is represented as rest event(s) (`is_rest=True`) with matching `duration_ticks` and valid `notated_duration`.

## Execution Model

Execute only the versioned prompt selected by
`projects/score2gp/prompts/NEXT.md`.

## Handoff

ADR written to `projects/score2gp/research/2026-07-25-cr04c-final-event-duration-architecture-decision.md`. Prompt 0011 created and set as current in `prompts/NEXT.md`. Open governance PR and stop for independent Codex review. Do not merge.
