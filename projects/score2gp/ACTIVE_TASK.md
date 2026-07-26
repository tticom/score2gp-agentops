# Active Task

**Task**: CR-04D5: PDF-Only Tab Measure-Assembly Compatibility Closure
**Authorised Role**: Developer (Tier B)
**Repository**: tticom/score2gp-agentops
**Product Repository**: tticom/score2gp
**Product Prerequisite**: merged PR #389 at product merge
`a8250ea8a1b71f8b64081ee6cf6408dd77398509`

## Status

ACTIVE — FINAL CR-04D CLOSURE LOOP AUTHORISED BY PROMPT 0016

## Context

CR-04D1 through CR-04D4 are merged. Revalidation found five obsolete D1/D2
helper imports and the obsolete `_STRING_TO_BASE_PITCH` constant in
`build_ir.py`. The extracted production boundary is otherwise intact.
CR-04D5 is a compatibility-and-documentation closure, not another extraction.

## Execution Model

Execute only the versioned prompt selected by
`projects/score2gp/prompts/NEXT.md`. No later refactor prompt is active.

## Handoff

Execute `0016-cr04d5-measure-assembly-compatibility-closure-wireframe.md`.
Publish one bounded product PR and stop for independent review. Do not merge
the PR, begin another refactor, or treat the recorded next candidate as
authorised work.
