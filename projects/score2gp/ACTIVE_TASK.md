# Active Task

**Task**: FS-07: Independent Review of CLI Facade Migration
**Authorised Role**: Reviewer
**Repository**: tticom/score2gp

## Status

AGY_EXECUTION_AUTHORISED

## Context

Product PR #381 completed and merged the behaviour-preserving
`score2gp.notation_omr` extraction. Product PR #382 migrates the five
production CLI recognition imports from the legacy compatibility shim to
`score2gp.notation_omr.pipeline`.

The exact review head is `bea32ac`.

## Execution Model

Execute only the versioned prompt selected by
`projects/score2gp/prompts/NEXT.md`.

## Boundaries

Review product PR #382 at exact head `bea32ac`. Do not implement unrelated
changes, merge, force-push, delete branches, or remove the compatibility shim.

## Handoff

Publish a concise independent review with verification evidence. If clean,
mark it ready for external human merge. Do not merge it.
