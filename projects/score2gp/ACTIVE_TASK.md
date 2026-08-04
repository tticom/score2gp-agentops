# Active Task

**Task**: CR-05: Repair Structural Layout and Titles Architecture
**Status**: PROMOTED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr05-structural-layout-and-titles-architecture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0026-cr05-structural-layout-and-titles-architecture.md`

## Context

Task `MXS-10` completed and merged via PR #401 (`5987aa0fe45859435067db14439cfb5598a2b704`). The project now promotes backlog task `CR-05` to determine a generic, testable architecture for independently classifying ordinary, double, and final barlines, system/page layout breaks, and phrase/piece title ownership.

## Goal

Determine a generic, testable architecture in `tticom/score2gp` for independently classifying barlines, layout breaks, and title ownership without implying system breaks from barline types. Write the architectural design report at `docs/design/cr05-structural-layout-and-titles-architecture.md`.

## Allowed Files

- `docs/design/cr05-structural-layout-and-titles-architecture.md`

## Non-goals

- No product source code modifications in `src/` or `tests/`.
- No modifications to governance files in `score2gp-agentops`.

## Acceptance

Publish one product architecture PR on branch `agy/cr05-structural-layout-and-titles-architecture` in `tticom/score2gp` containing `docs/design/cr05-structural-layout-and-titles-architecture.md` for independent Codex review.
