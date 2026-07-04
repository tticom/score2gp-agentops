# Whole-Note Fixture-Boundary Decision

**Date**: 2026-07-04  
**Context**: The targeted Font-Glyph Notation Extraction diagnostic against the Mutopia A4 BWV-120 fixture successfully verified the architecture mechanically, but mathematically could not verify the whole-note glyph mapping because the 3/4 time signature of BWV-120 precludes the presence of whole notes. A new fixture that actually contains whole notes is required to complete the diagnostic phase.

## Approved Candidate Fixture
- **Title**: Invention 1, BWV 772
- **Composer**: Johann Sebastian Bach
- **Source**: Mutopia Project
- **Source page URL**: https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=1418
- **Exact pinned PDF URL**: `https://www.mutopiaproject.org/ftp/BachJS/BWV772/bach-invention-01/bach-invention-01-a4.pdf`
- **Format**: A4 PDF
- **Licence/provenance**: Creative Commons Attribution-ShareAlike 3.0
- **Whole-note evidence**: The piece is in 4/4 (Common Time), enabling 4-beat whole notes. The final chord of the piece consists of 5 notes. An initial diagnostic confirmed a group of 5 identical Emmentaler-20 glyphs at the exact end of the score, providing strong evidence of a whole-note chord.
- **Suitability**: The fixture uses the identical `Emmentaler` font stack previously tested and verified by PyMuPDF extraction, ensuring that the diagnostic can proceed without new font-handling variables.
- **Excluded variants**: Letter format variants and any unpinned URLs or private files are excluded.

## Decision
**Verdict**: Outcome A — Approve exactly one pinned fixture for controlled diagnostic use.

### Supervisor licence/provenance decision
- The fixture is CC BY-SA 3.0, not public domain.
- CC BY-SA 3.0 is accepted only for temporary local read-only diagnostic use.
- No redistribution of the PDF is permitted.
- No committed PDF is permitted.
- No committed score-derived artifacts (excerpts, rendered images, JSON reports, screenshots, datasets, etc.) are permitted.
- Attribution/licence/provenance is recorded herein.
- Any future distributed score-derived artifacts require a fresh Supervisor/licence review.

### Approved Use
- Controlled, read-only targeted diagnostic to map music-font glyphs to whole-note coordinates.

### Forbidden Use
- Developer implementation.
- Product testing/fixtures.
- Broad OMR/CV.
- Usage of unpinned URLs or private local PDFs.

### Required Next Task
Targeted Diagnostic — Map Approved Whole-Note Fixture Music-Font Glyphs to Coordinates.

**Required next review:** Reviewer diagnostic evidence verification after diagnostic.
