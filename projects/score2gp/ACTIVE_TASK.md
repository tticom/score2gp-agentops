# Active Task

**Task**: CR-05: Repair Structural Layout and Titles Architecture
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect / Diagnostic Engineer
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr05-structural-layout-and-titles-architecture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0026-cr05-structural-layout-and-titles-architecture.md`

## Context

CR-05 is authorized to proceed as bounded Architect research in `tticom/score2gp`. The maintainer accepts current product `origin/main`, including commit `f3cf042c96defdaf09c3353f16f9dbcb38e542d3`, as the baseline for CR-05 research without requiring historical reconstruction of earlier task records.

## Goal

Investigate and define the generic, testable architecture for separating double/final barline classification, system/page layout, and phrase-title anchoring in score2gp PDF conversion. Produce a Developer-ready rule and public regression plan in `tticom/score2gp` if evidence supports continuation.

## Allowed Files

- `docs/design/cr05-structural-layout-and-titles-architecture.md` (in `score2gp`)

## Non-goals

- No edits to product source code in `score2gp` during this Architect phase.
- No edits or creation of AgentOps candidate prompts, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/NEXT.md`, or governance run records in `score2gp-agentops` during the Architect research run.
- Recommended follow-up candidates must be recorded inside the durable architecture report. After the product architecture PR is reviewed and merged, a separate `tticom-gov` governance cycle may promote the selected candidate in AgentOps.

## Acceptance

Comprehensive product architecture report written in `docs/design/cr05-structural-layout-and-titles-architecture.md` with exact geometric layout classification rules, double/final barline decoupling, title anchoring logic, falsification evidence, and public test contracts. Stop after publishing one product architecture PR in `tticom/score2gp` for independent Codex review.
