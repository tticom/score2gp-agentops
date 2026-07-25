# Active Task

**Task**: CR-04B: Explicit Tempo Override for PDF-Only TabRaw Conversion
**Authorised Role**: Developer (Tier B)
**Repository**: tticom/score2gp
**Product Repository**: tticom/score2gp
**Product Base**: ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f

## Status

ACTIVE — PRODUCT IMPLEMENTATION AUTHORISED BY PROMPT 0009

## Context

Current PDF-only TabRaw conversion defaults to 120 BPM through
`build_ir_from_tabraw_only(..., tempo_bpm=120.0)`. Real-world Lesson-5
evidence expects 70 BPM. The next smallest product capability is an explicit,
validated CLI tempo override that reaches the existing builder parameter while
preserving the current default when omitted.

## Execution Model

Execute only the versioned prompt selected by
`projects/score2gp/prompts/NEXT.md`.

## Acceptance

`score2gp convert --pdf-only-tab --tempo-bpm 70 ...` must emit ScoreIR tempo
70 through a public fixture test. Omitting the option must still emit 120.
Non-positive values must be refused. Full validation and artifact audit must
pass.

## Boundaries

Do not implement PDF tempo OCR/extraction, change duration padding, alter
MusicXML tempo behavior, use private fixtures as test dependencies, or broaden
conversion semantics beyond explicit PDF-only TabRaw tempo forwarding.

## Handoff

Execute prompt `0009-cr04b-explicit-pdf-only-tempo-override.md`. Publish one
product PR and stop for independent Codex review. Do not merge.
