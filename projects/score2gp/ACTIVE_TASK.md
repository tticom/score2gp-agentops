# Active Task

**Task**: CR-04A: False-Rest Candidate and Per-Voice Capacity Gate
**Authorised Role**: Architect
**Repository**: tticom/score2gp-agentops
**Product Repository**: tticom/score2gp
**Product Base**: ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f

## Status

ACTIVE

## Context

CR-04A evidence analysis of `Lesson-5.pdf` established that the false rest candidate is a **half rest** (1920 ticks), disproving the `quarter_rest_recogniser.py` hypothesis. Furthermore, `timeline_preview` is a read-only CLI diagnostic that does not gate active conversion (`build_ir` / `notation_bridge`).

The architecture pass identified an `OBSERVABILITY_GAP`. The next bounded task
must replay the approved Lesson-5 input on current product `main` with runtime
provenance before any instrumentation or implementation is authorized.

## Execution Model

Execute only the versioned prompt selected by
`projects/score2gp/prompts/NEXT.md`.

## Boundaries

Do not modify product code. Do not claim the Lesson-5 mismatch fixed. Record
only sanitized facts, hashes, commands, exit status, and event summaries.

## Handoff

Execute prompt `0008-cr04a-current-runtime-evidence-replay.md`. Publish the
bounded evidence handoff and stop for Codex review. Do not begin product implementation or merge.
