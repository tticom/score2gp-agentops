# Active Task

**Task**: CR-04A: False-Rest and Per-Voice Capacity Architecture
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect / Diagnostic Engineer
**Repository**: tticom/score2gp-agentops
**PR Branch**: `agy/cr04a-false-rest-capacity-architecture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0007-cr04a-false-rest-capacity-architecture.md`

## Context

Following the merge of PR #396 (`ea720c353af0926bede1980d55479db77c22aa58`, product main commit `f3cf042c96defdaf09c3353f16f9dbcb38e542d3`), task PDFTAB-DUR-07 (Slice 4 Regression Audit & System Hardening) is complete. The next item in the maintainer-approved Visual Output Correctness Recovery Series is CR-04A (False-rest candidate and per-voice capacity gate).

## Goal

Locate the first committed-evidence divergence that creates the Lesson-5 false-rest candidate, and define a deterministic per-voice measure-capacity gate. Produce a Developer-ready rule and public regression plan.

## Allowed Files

- `projects/score2gp/reports/2026-07-24-cr04a-architecture.md` (in `score2gp-agentops`)
- `projects/score2gp/prompts/next/` (in `score2gp-agentops`)
- `projects/score2gp/ACTIVE_TASK.md` (in `score2gp-agentops`)
- `projects/score2gp/prompts/NEXT.md` (in `score2gp-agentops`)

## Non-goals

No edits to product code in `score2gp` during this Architect phase.

## Acceptance

Comprehensive architecture report written with exact capacity calculation rules, false-rest rejection criteria, and public test contracts.
