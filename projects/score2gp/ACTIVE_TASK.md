# Active Task

**Task**: CR-04A: False-Rest Candidate and Per-Voice Capacity Gate
**Authorised Role**: Architect
**Repository**: tticom/score2gp-agentops
**Product Repository**: tticom/score2gp
**Product Base**: ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f

## Status

OBSERVABILITY_GAP

## Context

CR-04A evidence analysis of `Lesson-5.pdf` established that the false rest candidate is a **half rest** (1920 ticks), disproving the `quarter_rest_recogniser.py` hypothesis. Furthermore, `timeline_preview` is a read-only CLI diagnostic that does not gate active conversion (`build_ir` / `notation_bridge`).

This pass is classified as `OBSERVABILITY_GAP`. No product code changes or Developer implementation prompts are authorized until candidate provenance, primitive source, and active conversion refusal points are instrumented.

## Execution Model

Execute only the versioned prompt selected by
`projects/score2gp/prompts/NEXT.md`.

## Boundaries

Do not modify product code. Do not claim the Lesson-5 mismatch fixed. Record sanitized facts in governance report.

## Handoff

Publish governance PR #364 containing the updated `OBSERVABILITY_GAP` architecture report. Stop for Codex review. Do not begin product implementation or merge.
