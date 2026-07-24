# Active Task

**Task**: CR-04A: False-Rest Candidate and Per-Voice Capacity Gate
**Authorised Role**: Architect
**Repository**: tticom/score2gp-agentops
**Product Repository**: tticom/score2gp
**Product Base**: ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f

## Status

ACTIVE

## Context

CR-03D is complete: product PR #383 merged at
`ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`.

CR-04A must identify the generic cause of the Lesson-5 false-rest candidate and
define a per-voice measure-capacity rule that refuses overfull output safely.
The cause and correct injection point are not yet proven, so this first pass is
evidence and architecture only.

## Execution Model

Execute only the versioned prompt selected by
`projects/score2gp/prompts/NEXT.md`.

## Boundaries

Do not modify product code. Use committed public evidence first; private
fixtures may be inspected only under the existing artifact policy. Do not
claim the Lesson-5 mismatch fixed. Produce a bounded Developer requirement
packet or an explicit observability-gap report.

## Handoff

Publish one governance PR containing the evidence report and, when supported,
the exact Developer prompt. Stop for Codex review. Do not begin implementation
or merge.
