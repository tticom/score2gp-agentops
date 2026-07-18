# Active Task

**Task**: CR-04A: False-rest candidate and per-voice capacity gate - Architect Phase
**Authorised Role**: Architect
**Repository**: `tticom/score2gp` (product) and `tticom/score2gp-agentops` (governance)

## Status

APPROVED

## Task Authorised

Yes, Tier 1 architecture phase authorized.

## Permissions and Boundaries

- Do not modify product code/tests or create product branches in this phase.
- Investigate and locate the source of the Lesson-5 false-rest generation.
- Design a per-voice balance gate: every emitted MusicXML measure must balance independently per voice. A measure with an extra rest or overfull voice must refuse rather than report strict success.
- Outline the exact required changes in `projects/score2gp/reports/2026-07-18-cr-04a-architect-report.md`.
- No OMR orchestration or deterministic MusicXML emission is to be implemented.

## Completion Evidence

1. An Architect report defining the false-rest root cause and the per-voice capacity gate algorithm.
2. An independent Reviewer approval of the architecture report.

## Unattended Continuation

This task opts into the Visual Output Correctness Recovery Programme's
Unattended Consecutive Loop Protocol. After review, rework, or guarded merge,
agents must continue to the next required role or eligible task without routine
maintainer confirmation. Before a genuine stop, they must commit the required
human-focused end-of-run report in AgentOps.
