# Archived Active Plan: PDF-Only Tab-to-GP MVP

**Archived:** 2026-08-19

**Reason:** Superseded by the native PDF-to-GP and Audiveris retirement
programme. Historical PR #176 milestones and layout-inferred-rhythm success
criteria are no longer active product direction.

## Historical text

The plan aimed to establish a direct PDF-to-GP pathway for born-digital guitar
TAB without a mandatory MusicXML/MXL timing sidecar.

Its recorded baseline was PDF TAB extraction, visual grouping diagnostics, GP
writing, validation, and a then-draft PDF-only implementation under product PR
#176. Lesson 3 diagnostics reported 512 candidates, 461 playable fret
candidates assigned to systems/bars/strings, 23 systems, and 64 bar boxes. The
recorded blocker was partial grouping and missing timing/rhythm mapping.

The historical MVP accepted a structurally valid GP package with mostly
equivalent notes/frets/strings and deterministic layout-inferred rhythm. It
required refusal for missing or ambiguous grouping, exclusion of text judged
non-playable, and protection of private fixtures.

Historical milestones were:

1. Establish the active plan.
2. Review draft product PR #176.
3. Prove the pathway on a public generated fixture.
4. Run Lesson 3 page-one private smoke.
5. Run Lesson 3 full-score private smoke.
6. Improve naive density-grid rhythm.
7. Expand techniques and layout after basic notes/measures/strings/frets.

Historical non-goals included scanned PDFs, arbitrary handwritten layouts,
perfect rhythm/tempo, Audiveris dependency, and using private reference GP
files as generation inputs.

## Retained lessons

- Direct PDF-to-GP without a mandatory sidecar remains a product requirement.
- Private fixtures remain local and validation-only.
- Ambiguity must remain visible and must never be converted into fabricated
  certainty.

## Superseded lessons

- Geometry warnings now trigger diagnosis, reconstruction, and correction
  attempts before refusal.
- Text is semantic evidence to classify and associate, not content to discard
  merely because it is not a fret token.
- Structural package validity and “mostly equivalent” output are insufficient.
- Layout-inferred timing is not validated musical truth.
