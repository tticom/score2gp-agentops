# 0013 - CR-04D2 Extract PDF-Only Tab Event Construction (Wireframe)

## Status

INACTIVE WIREFRAME. Not executable while Prompt 0012 is active or unmerged.

## Intended Objective

Extract conversion of one grouped PDF-only TabRaw subgroup into a note or
explicit-rest `Event`, preserving every observable field.

## Promotion Preconditions

CR-04D1 is externally merged; its SHA is recorded; source confirms a cohesive
boundary; and the promoted prompt names an exact allowlist and current tests.

## Intended Boundary and Evidence

Inputs include candidates, bar/event indexes, onset, duration descriptor, and
editable annotation context. Output is one `Event` with no hidden mutation.
Preserve IDs, notes, pitches, provenance, confidence, text, rest handling,
timing, and exceptions. Do not change grouping, duration policy, bar completion,
warnings, schemas, or GP serialization.

Characterise note, chord, explicit-rest, duplicate-string, editable first-event
text, and provenance cases; run existing PDF-only, chord, CLI, GP, and full
verification tests.

If extraction requires grouping, diagnostics, public-type, or duration-policy
changes, return to governance. Publish one PR and stop before CR-04D3.
