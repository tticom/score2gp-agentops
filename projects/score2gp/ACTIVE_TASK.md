# Active Task

**Task**: CR-04C: Final-Event Duration Consistency Implementation
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer / Pipeline Integrator
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr04c-final-event-duration-consistency-implementation`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0011-cr04c-final-event-duration-consistency-implementation.md`

## Context

Following the completion of the CR-04C architecture pass (`projects/score2gp/research/2026-07-25-cr04c-final-event-duration-architecture-decision.md`), Option A (grid-sized notes + greedy rest decomposition + over-capacity refusal) was selected and approved. This task implements the Developer solution in `build_ir_from_tabraw_only()`.

## Goal

Implement Option A in `src/score2gp/build_ir.py`: set every candidate note event's duration to `grid_spacing` (480 ticks), greedily decompose remaining measure capacity $R = 3840 - \text{current\_onset}$ into un-dotted rest events, and raise `BuildIrInputRiskError(category="pdf_only_tab_measure_overcapacity")` if measure capacity is exceeded.

## Allowed Files

- `src/score2gp/build_ir.py` (in `score2gp`)
- `tests/test_pdf_only_tab.py` (in `score2gp`)
- `tests/test_build_ir.py` (in `score2gp`)

## Non-goals

No edits to MusicXML sidecar timing alignment, tempo handling, GP schema, or unrelated conversion code.

## Acceptance

Test-first implementation complete in `src/score2gp/build_ir.py`. Tests for $N=4$ single rest, $N=3$ multi-rest remainder, $N=1$ multi-rest remainder, and over-capacity refusal pass. Full pytest suite and `agent_verify.py` pass with overall status `PASS`.
