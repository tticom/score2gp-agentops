# REC-09 — TAB Token Evidence

Status: SKELETON — depends on REC-04 and REC-06
Role: Developer
Repository: `score2gp`

## Objective

Detect TAB glyph tokens and grouping alternatives before resolving fret values,
string ownership or final events.

## Required work

1. Emit source glyph observations and digit-class hypotheses separately.
2. Generate bounded multi-digit grouping alternatives with provenance.
3. Use scale-normalized spacing and staff context, not a global point gap.
4. Preserve unresolved alternatives for the graph assembler.
5. Do not assign bar, onset, duration or final fret ownership here.

## Acceptance and falsification

- Real-source cases distinguish `10`, adjacent `1 0`, and `7 10`.
- Values outside supported instrument policy remain hypotheses or Unsupported.
- No `gap <= constant` rule alone establishes a multi-digit fret.

## Validation

Promoted prompt must include provenance-linked real PDF extractions and REC-01
ordered-token evaluation; synthetic glyphs cannot satisfy acceptance.

