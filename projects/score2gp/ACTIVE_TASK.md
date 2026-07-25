# Active Task

**Task**: CR-04C: Final-Event Duration Consistency Implementation
**Authorised Role**: Developer (Tier B)
**Repository**: tticom/score2gp-agentops
**Product Repository**: tticom/score2gp
**Product Base**: f47194e57b551d4b571a04c0b7641fbe9c173f80

## Status

ACTIVE — PRODUCT IMPLEMENTATION AUTHORISED BY PROMPT 0011

## Context

CR-04C architecture resolved the PDF-only TabRaw final-event duration-padding
inconsistency. Option A was selected: final note duration is set to
`grid_spacing` (matching `notated_duration`), and remaining measure capacity is
represented by deterministic, truthfully notated rest events. Prompt 0011
authorises the bounded product implementation and over-capacity refusal.

## Execution Model

Execute only the versioned prompt selected by
`projects/score2gp/prompts/NEXT.md`.

## Handoff

Execute prompt
`0011-cr04c-final-event-duration-consistency-implementation.md`. Publish one
product PR and stop for independent Codex review. Do not merge.
