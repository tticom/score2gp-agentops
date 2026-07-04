# Active Task

**Task**: Architect Research — Mutopia A4 Whole-Note Representation and Alternative Detection Viability
**Authorised Role**: Architect
**Repository**: `tticom/score2gp-agentops`

## 1. Baseline
- The controlled diagnostic result failed: vector-path whole-note heuristic produced 0 candidates.

## 2. Active Blocker
- Vector-path whole-note heuristic produced 0 candidates for the Mutopia A4 fixture.

## 3. Goal
- Determine the representation of whole notes (or relevant symbols) in the fixture.
- Determine whether a viable alternative detection approach exists.

## 4. Non-goals
- No implementation.
- No product changes.
- No OMR/CV implementation.
- No fixture expansion.

## 5. Fixture Boundary
- Exact pinned A4 URL only: `https://www.mutopiaproject.org/ftp/BachJS/BWVAnh120/BWV-120/BWV-120-a4.pdf`

## 6. Required Evidence
- PDF object/content stream inspection if available through safe tools.
- Whether relevant symbols appear as text/font glyphs, vector drawings, raster image content, or unknown.
- Whether whole-note-specific detection can be bounded without broad OMR/CV.
- Risks of false positives/false negatives.
- Proposed diagnostic or implementation path only if evidence supports it.

## 7. Required Output
Architect must choose exactly one outcome:
- **Outcome A**: text/font-based detection appears viable for the approved fixture and should proceed to Reviewer architecture verification.
- **Outcome B**: text/font-based detection is not viable, but another bounded non-implementation approach appears viable and should proceed to Reviewer architecture verification.
- **Outcome C**: no viable approach found; no Developer work authorised.

## 8. Stop Conditions
- Representation cannot be determined.
- Evidence requires product implementation to inspect.
- Fixture boundary cannot be maintained.
- Approach would require broad OMR/CV implementation.
- No decision-useful evidence can be produced.
