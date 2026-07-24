# Active Task

**Task**: CR-03D: Local Tuplet-Group Evidence and Meter Resolution Retry
**Authorised Role**: Developer
**Repository**: tticom/score2gp

## Status

AGY_EXECUTION_AUTHORISED

## Context

FS-06/FS-07 are complete. Product `main` is clean at
`dacb0e53e47a366c557d2bba78851b77145874fb`, with notation recognition now
owned by `score2gp.notation_omr`.

CR-03D resumes the independently approved CR-03A architecture from the clean,
post-refactor base. It implements only deterministic local 3:2 eighth-note
triplet evidence and fail-closed ambiguity reporting. It must not revive the
reverted prototype or write new logic into `whole_note_recogniser.py`.

## Execution Model

Execute only the versioned prompt selected by
`projects/score2gp/prompts/NEXT.md`.

## Boundaries

Use committed product source and public synthetic tests only. No private
artifacts, fixture-specific coordinates, global note-count fallbacks, reference
GP influence, unrelated meter repairs, or compatibility-shim implementation.

## Handoff

Publish exactly one product PR and stop for independent review. Do not merge it.
