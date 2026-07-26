# Active Task

**Task**: CR-04D1: Extract PDF-Only Tab Measure-Duration Policy
**Authorised Role**: Developer (Tier B)
**Repository**: tticom/score2gp-agentops
**Product Repository**: tticom/score2gp
**Product Prerequisite**: merged PR #385 containing
`3715dbdb54c8387c77ab770430998c6160bf07d4`

## Status

ACTIVE — FIRST CR-04D REFACTOR LOOP AUTHORISED BY PROMPT 0012

## Context

CR-04C is merged. Its duration/capacity/rest policy is protected but embedded
in `build_ir_from_tabraw_only()`. CR-04D records five one-boundary-per-PR steps.
Only Step 1 is active.

## Execution Model

Execute only the versioned prompt selected by
`projects/score2gp/prompts/NEXT.md`. Prompts 0013-0016 are inactive wireframes
and require predecessor merge plus source revalidation before promotion.

## Handoff

Execute `0012-cr04d1-extract-pdf-tab-measure-duration-policy.md`. Publish one
product PR and stop for independent review. Do not merge or begin CR-04D2.
