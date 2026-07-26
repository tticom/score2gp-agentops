# Active Task

**Task**: CR-04D2: Extract PDF-Only Tab Event Construction
**Authorised Role**: Developer (Tier B)
**Repository**: tticom/score2gp-agentops
**Product Repository**: tticom/score2gp
**Product Prerequisite**: merged PR #386 at product merge
`56eddc2d9132763d271f45cfbc399d44696bdd9d`

## Status

ACTIVE — SECOND CR-04D REFACTOR LOOP AUTHORISED BY PROMPT 0013

## Context

CR-04D1 is merged. Duration policy now lives in
`pdf_tab_measure_timing.py`; subgroup-to-`Event` construction remains embedded
in `build_ir_from_tabraw_only()`. Only CR-04D2 is active.

## Execution Model

Execute only the versioned prompt selected by
`projects/score2gp/prompts/NEXT.md`. Prompts 0014-0016 are inactive wireframes
and require predecessor merge plus source revalidation before promotion.

## Handoff

Execute `0013-cr04d2-extract-pdf-tab-event-construction-wireframe.md`. Publish
one product PR and stop for independent review. Do not merge or begin CR-04D3.
