# Active Task

**Task**: FS-06B: Shared Evidence and Staff Geometry Extraction
**Authorised Role**: Developer
**Repository**: tticom/score2gp

## Status

AGY_EXECUTION_AUTHORISED

## Context

FS-06A is complete. FS-06B starts the behaviour-preserving migration with the shared evidence helper and independent staff-geometry functions. It is a refactor only: output, data structures, CLI contracts, and existing imports must remain stable.

## Execution Model

Execute only the versioned prompt selected by projects/score2gp/prompts/NEXT.md.
That prompt is the authoritative execution and publication contract for this task.

## Boundaries

Use committed product source and public tests only. Modify only the files explicitly allowed by the versioned prompt. Do not change observable behaviour, CLI contracts, generated artefacts, fixtures, schemas, or private inputs.

## Handoff

Publish exactly one product PR as required by the versioned prompt. Do not merge it.
