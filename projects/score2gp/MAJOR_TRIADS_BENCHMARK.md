# Major Triads Lesson 3 Benchmark

This document defines the **Major Triads Lesson 3** private benchmark, which serves as the next serious correctness rung on our benchmark ladder.

## Benchmark Properties

- **Source Origin**: Born-digital Guitar Pro (GP) file, printed directly from its GP parent to ensure pristine, digital-native vector geometry.
- **Musical Complexity**: Straight major triad note runs with a regular, highly consistent rhythm.
- **Expressive Burden**: Minimal or no expressive techniques (no noisy pitch bends, slides, vibratos, tremolo picking, or complex ornament burdens) compared to noisy real-world stress files (e.g., Ross Campbell or Derek Trucks).
- **Benchmark Intent**: Represents the **expected minimum real-world capability** for basic PDF-to-GP round-trip conversion. Any parser or geometry pipeline must be able to convert this rung flawlessly before attempting complex expressivity layers.

---

## Staged Benchmark Results Schema

Reviewer and implementation agents must collect, verify, and document the following private-safe metrics on this benchmark:

### 1. Extraction & Layout Geometry Metrics
- **Page Count**: Total pages in the input PDF.
- **Detected Systems**: Number of visual systems identified across all pages.
- **Detected Bar Boxes**: Count of constructed bar bounding boxes.
- **Detected String Lines**: Count of horizontal staff lines identified.
- **Playable Candidates**: Number of text symbols parsed as playable fret digits.
- **Playable Candidates with System**: Playable frets successfully assigned to a system.
- **Playable Candidates with Bar**: Playable frets successfully assigned to a bar.
- **Playable Candidates with String**: Playable frets successfully assigned to a string.

### 2. Strict Build-IR Status
- **Strict Grouping Status**: `missing` / `partial` / `complete` (strict safety-gate status).
- **ScoreIR Written**: `yes` / `no`.
- **GP Written**: `yes` / `no`.
- **Primary Blocker Category**: Blocker code if strict build-ir failed (e.g. `partial_pdf_grouping`).
- **Grouping Warning Codes**: Specific warning codes that prevented compilation.

### 3. Semantic Round-Trip Metrics
- **Oracle Note Count**: Total guitar track notes parsed from the original GP7 file.
- **Recovered Note Count**: Total notes recovered in the generated ScoreIR.
- **String Match Rate**: Percentage of recovered notes with matching string assignments.
- **Fret Match Rate**: Percentage of recovered notes with matching fret digit values.
- **Full Match Rate**: Percentage of recovered notes with matching string + fret values.
- **Poor Bars**: Count of measures labeled as "poor" quality.
- **Unknown Bars**: Count of measures labeled as "unknown" quality.
