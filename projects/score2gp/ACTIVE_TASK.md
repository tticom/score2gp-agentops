# Active Task

**Task**: CR-04D3: Extract PDF-Only Tab Bar Assembly
**Authorised Role**: Developer (Tier B)
**Repository**: tticom/score2gp-agentops
**Product Repository**: tticom/score2gp
**Product Prerequisite**: merged PR #387 at product merge
`36b3016...`

## Status

ACTIVE — THIRD CR-04D REFACTOR LOOP AUTHORISED BY PROMPT 0014

## Context

CR-04D1 (`pdf_tab_measure_timing.py`) and CR-04D2 (`pdf_tab_event_factory.py`) are merged into product `main`. Per-source-bar assembly and orchestration remain embedded in `build_ir_from_tabraw_only()`. Only CR-04D3 is active.

## Execution Model

Execute only the versioned prompt selected by `projects/score2gp/prompts/NEXT.md`. Prompts 0015-0016 are inactive wireframes and require predecessor merge plus source revalidation before promotion.

## Handoff

Execute `0014-cr04d3-extract-pdf-tab-bar-assembly-wireframe.md`. Publish one product PR and stop for independent review. Do not merge or begin CR-04D4.
