# Active Task

**Task**: FS-06A: Notation OMR Modularisation Architecture
**Authorised Role**: Architect, Tier B refactor architecture
**Repository**: tticom/score2gp and tticom/score2gp-agentops

## Status

PR_OPEN

## Context

The Project Director has expedited refactor planning because whole_note_recogniser.py now owns materially broader notation, geometry, duration, timeline, and diagnostic behaviour than its name describes. FS-06A is architecture-only. It must make the following implementation work safe, small, and behaviour-preserving; it must not rename or move product code.

## Execution Model

Execute only the versioned prompt selected by projects/score2gp/prompts/NEXT.md.
That prompt is the authoritative execution and publication contract for this task.

## Boundaries

Use committed product source and public tests only. Do not modify product code, tests, fixtures, schemas, CLI behaviour, generated files, or private inputs.

The report must:
- map all imports, public calls, and CLI paths touching whole_note_recogniser.py;
- group responsibilities into cohesive modules under score2gp.notation_omr;
- retain whole_note_recogniser.py as a compatibility shim for the first migration;
- specify a sequence of independently reviewable implementation PRs;
- define per-step compatibility and test requirements;
- name one smallest first implementation PR with exact files and measurable done criteria.

Avoid cosmetic renaming, large moves, and behaviour changes. No proposed step may depend on Lessons 3 to 7, fixed PDF coordinates, or private fixtures.

## Handoff

Write projects/score2gp/reports/2026-07-23-fs06a-notation-omr-modularisation-architecture.md. Include source map, target package ownership, migration sequence, compatibility contract, test plan, and the first implementation task.

Update this task to PR_OPEN and publish exactly one Agy PR as required by the versioned prompt.
