# NPG-00R: Recognition Engine Ownership

**Date**: 2026-08-20
**Task**: NPG-00R

## 1. Context and Alternatives

During the execution of `note-candidate-recognition` on private fixtures (e.g., `Lesson-5.pdf`), the Audiveris OMR engine demonstrated catastrophic structural failure on modern born-digital instructional PDFs. It failed to recognize floating barlines, collapsed all 43 measures into one, caused capacity mismatch crashes, and missed structural text elements.

We compared alternatives:
1. **Audiveris (Current):** Fatally unsuited for parsing the irregular, sparse, hybrid tab/standard layouts found in modern born-digital instructional PDFs due to its reliance on strict classical score heuristics and raster-based OMR.
2. **Third-Party Vector Alternatives (e.g., PDFtoMusic Pro):** Highly capable of vector-based extraction, but commercial, proprietary, and highly brittle when processing "messy" or non-standard instructional layouts. It requires heavy manual tweaking, and there is no open-source equivalent of high quality.
3. **Owned Native Extraction Layer:** Building a bespoke vector-based recognition layer by expanding the existing `--pdf-only-tab` pipeline.

## 2. Decision

Score2GP will build and own the required recognition layer natively, fully retiring Audiveris and rejecting the adoption of third-party recognition objects. We will construct a bounded native extraction layer that processes vector-based structural signaling and layout resilience.

## 3. Explicit System Requirements

The native extraction layer must implement the following heuristic capabilities:
1. **Geometric Rhythm Extraction:** Parse the standard staff to extract rhythm (stems, beams, durations) and synchronize it with the Tablature staff.
2. **Layout Resilience & Irregular Rows:** The parser must cope seamlessly with a differing number of bars on a single row.
3. **Floating Barlines:** A vertical line detected anywhere within a system bounds must logically slice the timeline across all staves, regardless of whether it physically touches the staff lines.
4. **Vector-Based Structural Signaling:** Extract sections, phrases, and repeats natively from exact text coordinates and path stroke thicknesses.
5. **Sensible Defaults Definition:** We must define sensible default values for thresholds (e.g. Chord Proximity Threshold, Stroke Thickness Threshold, Section Marker Y-Offset).

## 4. Sequenced Task Boundary

The decision implies updates to the NPG implementation plan, integrating the aforementioned layout resilience and vector extraction heuristics into the `NPG-03` and `NPG-04` task sequence blocks without implementing product behavior at this stage.
