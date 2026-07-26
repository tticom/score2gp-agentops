# Active Task

**Task**: CR-04D4: Consolidate PDF-Only Tab Test Fixtures
**Authorised Role**: Developer (Tier B)
**Repository**: tticom/score2gp-agentops
**Product Repository**: tticom/score2gp
**Product Prerequisite**: merged PR #388 at product merge
`cea235d83e72e608b841e5d6d55b631077fa1833`

## Status

ACTIVE — FOURTH CR-04D REFACTOR LOOP AUTHORISED BY PROMPT 0015

## Context

CR-04D1 through CR-04D3 are merged. The D3 characterization work exposed
substantial repeated `TabCandidate`, `BoundingBox`, and TabRaw-file setup in
the focused PDF-only tests. Only CR-04D4 is active, and it is test-only.

## Execution Model

Execute only the versioned prompt selected by
`projects/score2gp/prompts/NEXT.md`. Prompt 0016 remains an inactive wireframe
and requires predecessor merge plus source revalidation before promotion.

## Handoff

Execute `0015-cr04d4-consolidate-pdf-tab-test-fixtures-wireframe.md`. Publish
one test-only product PR and stop for independent review. Do not merge or
begin CR-04D5.
