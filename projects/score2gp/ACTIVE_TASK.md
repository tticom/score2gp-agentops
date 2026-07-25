# Active Task

**Task**: CR-04C: Final-Event Duration Consistency Architecture Decision
**Authorised Role**: Architect (Tier B)
**Repository**: tticom/score2gp
**Product Repository**: tticom/score2gp
**Product Base**: f47194e57b551d4b571a04c0b7641fbe9c173f80

## Status

ACTIVE — BOUNDED ARCHITECTURE WORK AUTHORISED BY PROMPT 0010

## Context

Real-world Lesson-5 evidence and direct code inspection show that PDF-only
TabRaw conversion can emit a final event with `duration_ticks == 2400` while
retaining `notated_duration.value == "eighth"` (480 ticks). The correct
representation is not yet decided: shorten the event and add rest capacity,
split/tie the duration, or encode another supported notated duration structure.
Architecture must resolve this before product implementation.

## Execution Model

Execute only the versioned prompt selected by
`projects/score2gp/prompts/NEXT.md`.

## Acceptance

Produce a source-backed decision for the smallest correct ScoreIR and GP
representation. Prove the current mismatch with a tracked public fixture or
minimal synthetic TabRaw input, inspect serialization and validation behavior,
and specify measurable implementation tests plus stop/pivot criteria.

## Boundaries

Do not edit product code, choose a representation without checking ScoreIR and
GP serialization contracts, use private fixtures as test dependencies, alter
tempo handling, or broaden scope beyond the PDF-only TabRaw final-event
duration mismatch.

## Handoff

Execute prompt `0010-cr04c-final-event-duration-consistency-architecture.md`.
Publish one governance PR containing the decision and next bounded Developer
authorization, then stop for independent Codex review. Do not merge or edit
the product repository.
