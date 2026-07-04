# Active Task

**Task**: Targeted Diagnostic — Map Approved Whole-Note Fixture Music-Font Glyphs to Coordinates
**Authorised Role**: Diagnostic Operator
**Repository**: `tticom/score2gp`

## 1. Baseline
- Font-Glyph Notation Extraction architecture is approved.
- The previous 3/4 fixture lacked whole notes.
- A new 4/4 fixture containing whole notes (Bach Invention 1, BWV 772) is approved.

## 2. Active Blocker
- Exact whole-note glyph byte(s) and coordinate usability are unknown.

## 3. Goal
- Map `Emmentaler`/`feta` glyph values to their coordinates in the newly approved fixture.
- Identify the glyph value corresponding to a whole note.
- Verify whether the bounding box or center coordinates are tight/precise enough to unambiguously define a whole-note region for future implementation.

## 4. Non-goals
- No product code implementation.
- No fixture or test modifications.
- No broad OMR/CV.

## 5. Fixture Boundary
- Exact pinned URL only: `https://www.mutopiaproject.org/ftp/BachJS/BWV772/bach-invention-01/bach-invention-01-a4.pdf`

## 6. Required Output
- A diagnostic report detailing glyph values, counts, coordinate usability, and candidate whole-note mappings.
- Final verdict: PASS / FAIL / BLOCKED / CANNOT VERIFY.

## 7. Stop Conditions
- Required text spans cannot be extracted.
- Coordinate bounding boxes or centers are unmappable to a staff system.
- Artifact hygiene is compromised.
