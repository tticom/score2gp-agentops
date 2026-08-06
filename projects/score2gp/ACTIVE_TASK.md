# Active Task

**Task**: CR-05: Structural Layout and Titles Architecture
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect
**Repository**: tticom/score2gp-agentops
**PR Branch**: `agy/cr05-structural-layout-and-titles-architecture-v2`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0026-cr05-structural-layout-and-titles-architecture.md`

## Context

Task `CR-04A` (Current-Runtime Lesson-5 Evidence Replay) completed and resolved via PR #476 (`b00ff37149cace385c656df60161050f16dfe98d`). The project now promotes task `CR-05` from `APPROVED_TASK_QUEUE.md` under the Visual Output Correctness Series to investigate structural layout, barlines, and title ownership classification.

## Goal

Determine a generic, testable architecture for independently classifying barlines (ordinary, double, final), system and page layout breaks, and phrase or piece titles and their system/measure ownership without modifying product source code.

## Allowed Files

- `projects/score2gp/reports/2026-08-06-cr05-structural-layout-architecture.md`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- Architect investigation task only; no product source code changes in the Architect phase.

## Acceptance

Produce the CR-05 architecture report, update `ACTIVE_TASK.md`, and publish one governance pull request on branch `agy/cr05-structural-layout-and-titles-architecture-v2` in `tticom/score2gp-agentops` for independent Codex review.
