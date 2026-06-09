# TAB Notation Reference Image Analysis

Date: 2026-06-09
Author: AI Agent
Input source: `/home/tticom/work/score2gp-workspace/private-inputs/tab-notation-reference-images/2026-06-09`
Privacy classification: PRIVATE / REFERENCE ONLY

## Purpose
This document provides a derived architecture and research note capturing the visual notation features, recognition requirements, risks, and proposed future task sequence for TAB notation recognition. This analysis is based entirely on 64 private TAB notation reference images provided by the human maintainer.

## Input Handling and Privacy
The input images are strictly private. No image data, screenshots, or base64 encodings are included in this document. All images are retained in the private directory and are not copied into the Git repository. Findings are summarised using anonymised image IDs (e.g., `image-001`).

## Image Set Summary
A total of 64 reference images were analysed. These contain varied examples of guitar TAB notation ranging from simple numeric indicators to dense technical and expressive markings.

## Observed TAB Layout Features
- TAB staff structure: The images show staves with multiple horizontal lines representing strings. Some images show standard 6-string staves, while others may contain variable string counts.
- String spacing: The spacing between string lines varies across the image set.
- System labels: Some images contain "TAB" labels at the start of systems.

## Observed Text and Number Features
- Fret numbers: Single-digit and multi-digit fret numbers are observed, often placed directly on or straddling the staff lines.
- Stacked numbers: Numbers are frequently stacked vertically to represent chords.
- Lyrics and annotations: Various images contain text annotations, finger numbering (p, i, m, a), hand labelling, and capo notation labels.

## Observed Technique Markings
The image filenames and visual contents indicate a wide variety of specific techniques:
- Bends and releases (including pre-bends, quarter-tone bends, and repicked bends).
- Harmonics (natural, artificial, pinched, tapped, touched).
- Muting techniques (palm muting, fret-hand muting).
- Picking and striking (down/up picking, tremolo picking, pick rakes, pick scrapes, divebombs).
- Slurs (hammer-ons, pull-offs, slides).
- Vibrato and whammy bar markings (gargle, scoop/doop, violining).
- Note trills and arpeggiated chords.
- Tapping (pick-hand tapping, general tapping).

## Observed Rhythm and Timing Features
- Rhythm notation: Many TABs show rhythmic stems, beams, and flags extending from the fret numbers or placed below/above the staff.
- Duration and rests: Symbols indicating rhythmic duration and rest periods are observed.

## Observed Navigation / Repeat Features
- Repeats and navigation: Repeat bars, multiple endings, and navigation markers are observed in the broader layout structure.

## Ambiguities and Recognition Risks
- Collision cases: Fret numbers frequently touch or overlap with staff lines, making isolation difficult. Multi-digit numbers may cross line gaps.
- Overlapping markings: Technique markings (like slides or bends) often overlap with the fret numbers or staff lines.
- Font variations: Some text features use stylized or irregular fonts.
- Semantic grouping: Determining which technique marking applies to which fret number relies heavily on precise geometric clustering and alignment.

## Evidence Needed From Diagnostics
- Need text-span evidence preserving numeric glyph bounding boxes near TAB lines.
- Need a TAB staff line detector that preserves string-line y positions.
- Need diagnostics for symbol curves/arrows near numeric fret markers before technique classification.
- Need diagnostics for horizontal and vertical lines crossing text spans (to differentiate between stems and staff lines).
- Need public synthetic fixtures for numeric fret placement before using private references.

## Requirements Implications
- A strict geometric grouping stage is required before any semantic interpretation.
- The recogniser must support candidate structures that tolerate overlapping bounds.
- Font metadata must be preserved for text elements to disambiguate technique letters from lyrics or annotations.
- Geometry-based clustering around x-coordinates is necessary to associate rhythmic stems with fret numbers.

## Proposed Task Sequence
1. Research note only from private images. (Current)
2. Public synthetic fixture design for TAB primitives.
3. TAB staff-line diagnostics.
4. TAB numeric text-span diagnostics.
5. Geometry-only fret-number candidate boundary.
6. Technique-mark diagnostics only.
7. Candidate model review.
8. Extraction skeletons.
9. Only later: semantic interpretation, if evidence supports it.

## Explicit Non-Goals
- Do not implement full TAB parser.
- Do not infer pitch and duration from all images at this stage.
- Do not convert these images to ScoreIR.
- Do not add private screenshots as fixtures.

## Open Questions
- What is the acceptable tolerance for bounding box overlap when determining if a technique curve belongs to a specific fret number?
- Can we reliably distinguish between '0' (fret zero) and 'O' (open string / harmonic symbol) based purely on font metadata and geometry?
- How should multi-staff systems (e.g. standard notation + TAB) be handled if connectors are ambiguous?

## Traceability Notes
- image-001 to image-022: Technique specific examples, including bends, harmonics, tapping, and muting.
- image-023 to image-054: General TAB layout screenshots demonstrating fret numbers, rhythm stems, and overlaps.
- image-055 to image-064: Advanced expressive markings like slides, tremolo, vibrato, and finger directions.
