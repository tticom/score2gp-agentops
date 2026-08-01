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

CR-05 is authorized to proceed as bounded Architect research. The maintainer accepts current product `origin/main`, including commit `f3cf042c96defdaf09c3353f16f9dbcb38e542d3`, as the baseline for CR-05 research without requiring historical reconstruction of earlier task records.

## Goal

Investigate and define the generic, testable architecture for separating double/final barline classification, system/page layout, and phrase-title anchoring in score2gp PDF conversion. Produce a Developer-ready rule and public regression plan if evidence supports continuation.

## Allowed Files

- `projects/score2gp/reports/2026-08-01-cr05-architecture.md` (in `score2gp-agentops`)
- `projects/score2gp/prompts/next/` (in `score2gp-agentops`, candidate prompt only when evidence supports continuation)

## Non-goals

- No edits to product code in `score2gp` during this Architect phase.
- The Architect must NOT modify `projects/score2gp/ACTIVE_TASK.md` or `projects/score2gp/prompts/NEXT.md` during the CR-05 research run. Candidate prompts are not executable authorization until promoted by governance `got`.

## Acceptance

Comprehensive architecture report written with exact geometric layout classification rules, double/final barline decoupling, title anchoring logic, falsification evidence, and public test contracts. Stop after publishing one AgentOps architecture PR for independent Codex review.
