# Automation Evidence Handoff: NPG-00R (Recognition Engine Ownership)

**Date**: 2026-08-20
**Task**: NPG-00R - Decide recognition-engine ownership and Audiveris suitability
**Role**: Automation/Developer Handoff to Architect

## 1. Audiveris Suitability & Structural Failures
During recent execution (commit: dea02687eb1cd02da7baf138a0c3db1b07a786a7, tool: Audiveris v5.3) of `note-candidate-recognition` and `generate-sidecar` on instructional private fixtures (specifically `Lesson-5.pdf`), the Audiveris OMR engine demonstrated catastrophic structural failure:
- **Floating Barlines**: Audiveris failed to recognize vertical barlines that did not perfectly enclose the 5-line staff bounding boxes (a common instructional format).
- **Measure Collapsing**: As a result of missing barlines, it collapsed all 43 measures into a single giant "Measure 1".
- **Capacity Mismatch Crash**: The strict validation layer subsequently crashed because Measure 1 vastly exceeded standard beat capacity.
- **Missing Structural Elements**: It completely missed dynamic text annotations like section markers, phrases, and repeats because it relies on rigid classical score heuristics rather than parsing raw PDF text.

**Automation Conclusion**: Audiveris is fundamentally a raster-based OMR engine designed for historical sheet music scans. It is fatally unsuited for parsing the irregular, sparse, hybrid tab/standard layouts found in modern born-digital instructional PDFs.

## 2. Third-Party Vector Alternatives (Research on PDFtoMusic Pro)
We conducted a market scan for a 3rd-party software object that performs native vector-based sheet music extraction:
- **Myriad PDFtoMusic Pro** (https://www.myriad-online.com/en/products/pdftomusicpro.htm) is the commercial industry standard for this. It explicitly refuses to parse scanned images.
- **Extraction Method**: It extracts raw PDF vector paths and font metadata. Because notation fonts vary wildly (using private Unicode ranges), it runs shape recognition on the *vector curves themselves* (e.g., identifying a path as a treble clef based on its geometry, then caching that shape).
- **Heuristic Layout Resilience**: It distinguishes between repeat signs and regular barlines by analyzing the *stroke thickness* of the vertical lines (a thick line + thin line + dots = repeat).
- **Expert Mode / Complete Control**: It acknowledges that irregular formats break heuristics. It provides users with tunable parameters (e.g., maximum horizontal distance before notes are considered consecutive vs. a chord).

**Automation Conclusion**: The open-source market (reviewed tools including Oemer: https://github.com/BreezeWhite/oemer and PDF2Muse: https://github.com/Divergent-AI/PDF2Muse) does not have a high-quality equivalent to PDFtoMusic Pro. *(Note: Market claims are reported/unproven until independently checked by the Architect).* While PDFtoMusic Pro (unproven claim) proves that vector-based extraction works perfectly, community reviews indicate it is highly brittle when processing "messy" or non-standard instructional layouts, requiring heavy manual tweaking.

## 3. Recommendations for the Score2GP Native Extraction Layer
If the Architect decides we must own this codebase by expanding our `--pdf-only-tab` pipeline, we must implement the following heuristic capabilities:
1. **Geometric Rhythm Extraction**: The standard staff must be parsed to extract rhythm (stems, beams, durations), which is then synchronized with the Tablature staff.
2. **Layout Resilience & Irregular Rows**: The parser must cope seamlessly with a differing number of bars on a single row (e.g., 3 bars on row 1, 4 on row 2, 1 on row 3).
3. **Floating Barlines**: A vertical line detected anywhere within a system bounds must logically slice the timeline across all staves, regardless of whether it physically touches the staff lines.
4. **Vector-Based Structural Signaling**: We must extract sections, phrases, and repeats natively from exact text coordinates and path stroke thicknesses.

### Open Questions & Sensible Defaults
As noted by human supervision, exposing heuristic thresholds requires that we define **sensible defaults**. Working out what is "sensible" will require dedicated thought and empirical testing across the private fixtures.
- **Chord Proximity Threshold**: What is the default maximum X-coordinate distance between two notes before they are considered consecutive rather than a chord?
- **Stroke Thickness Threshold**: What vector line thickness mathematically separates a standard barline from a repeat bounding line?
- **Section Marker Y-Offset**: What is the sensible default vertical distance (in pixels or PDF points) above a staff to classify bold text as a section marker vs. standard lyrics?

*End of Handoff Evidence. Awaiting Architect Decision on engine ownership and bounded successor task sequence.*
