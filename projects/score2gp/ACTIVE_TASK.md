# Active Task

**Task**: CR-04A: False-Rest Candidate and Per-Voice Capacity Gate (Current-Runtime Replay)
**Authorised Role**: Architect
**Repository**: tticom/score2gp-agentops
**Product Repository**: tticom/score2gp
**Product Base**: ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f

## Status

REPLAY_COMPLETED (DEFECT_NOT_REPRODUCED)

## Context

CR-04A current-runtime evidence replay of `Lesson-5.pdf` on product `main` (`ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`) established that the false 1920-tick half rest recorded in historical evidence is absent from current candidate recognition, filtered out by `notation_bridge.py`, and absent from generated `ScoreIR`. Emitted Bar 0 voice 1 durations are `[480, 480, 480, 2400]` ticks ($D_{\text{voice1}} = 3840$), with an anomalous 2400-tick final event labeled `eighth`. Obsolete half-rest suppression code is disauthorized.

## Execution Model

Execute only the versioned prompt selected by
`projects/score2gp/prompts/NEXT.md`.

## Boundaries

Do not modify product code. Obsolete half-rest suppression is disauthorized. Record
only sanitized facts, hashes, commands, exit status, and event summaries.

## Handoff

Replay report published in `projects/score2gp/reports/2026-07-24-cr04a-current-runtime-replay.md`. Open governance PR and stop for Codex review.
