# Active Task

**Task**: CR-05: Repair Structural Layout and Titles Architecture
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect / Diagnostic Engineer
**Repository**: tticom/score2gp-agentops
**PR Branch**: `agy/cr05-structural-layout-and-titles-architecture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0026-cr05-structural-layout-and-titles-architecture.md`

## Context

Following the completion and resolution of CR-04 (False-rest candidate, explicit tempo override, and final-event duration consistency), the next maintainer-authorized task in the Visual Output Correctness Recovery Series is CR-05 (Repair Structural Layout and Titles).

## Goal

Investigate and define the rule packet for separating double/final barline classification, system/page layout, and phrase-title anchoring in score2gp PDF conversion. Produce a Developer-ready rule and public regression plan.

## Allowed Files

- `projects/score2gp/reports/2026-08-01-cr05-architecture.md` (in `score2gp-agentops`)
- `projects/score2gp/prompts/next/` (in `score2gp-agentops`)
- `projects/score2gp/ACTIVE_TASK.md` (in `score2gp-agentops`)
- `projects/score2gp/prompts/NEXT.md` (in `score2gp-agentops`)

## Non-goals

No edits to product code in `score2gp` during this Architect phase.

## Acceptance

Comprehensive architecture report written with exact geometric layout classification rules, double/final barline decoupling, title anchoring logic, and public test contracts.
