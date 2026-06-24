# Architect Report: Standard-Notation Structural Layout Inference Viability

## Context
Standard-notation PDF-only extraction is currently blocked by a lack of structural layout inference. While Score2GP can extract quarter rests and standard staff geometries, it relies entirely on a MusicXML sidecar for systems, barlines, measure boundaries, and polyphony mapping. This report evaluates whether deterministic structural layout inference can be extracted natively from vector geometry to eventually unblock PDF-only conversion.

## Facts
- **Sidecar Limitation**: `2026-06-23-musicxml-sidecar-limitation.md` records that standard-notation layout inference (systems, barlines, structural grouping) is not built, and explicitly requires a MusicXML sidecar.
- **Current Staff Detection**: `src/score2gp/pdf_staff_detection.py` (`_detect_notation_staff_groups`) deterministically extracts 5-line standard staves.
- **Current System Connectors**: `src/score2gp/pdf_staff_notation_diagnostics.py` (`_find_system_connector_between_groups`) deterministically detects system grouping via `leading_barline`, `bracket_curve`, and `brace_curve` primitives.
- **Missing Internal Barlines**: Standard notation lacks internal measure boundary (barline) extraction. `pdf_staff_notation_diagnostics.py` extracts leading system connectors but not standard internal barlines.
- **Missing Polyphony**: There is no code for grouping standard notation notes into distinct polyphonic voices without MusicXML `voice` properties.
- **Tab Barline Precedent**: Score2GP already extracts measure boundaries for tablature (`pdf_layout_vector_tab_with_barlines` in `pdf.py`).

## Inferences
- Because 5-line staff bounds and leading system connectors are already deterministically extracted, the vertical grouping of staves into systems is geometrically viable.
- Because a standard barline is a vertical stroke connecting the top and bottom lines of a staff, it is geometrically similar to a chord stem, making deterministic internal measure boundary extraction ambiguous without further heuristics.
- Because polyphony relies on complex stem direction, horizontal offset, and rests logic, voice mapping is mathematically underdetermined from primitive geometry alone without extensive heuristics or ML.

## Hypotheses
- **Narrow Layout Skeleton Hypothesis**: We can extract a complete "Layout Skeleton" (systems, staves, measure barlines) deterministically from standard-notation vector PDFs without attempting to solve polyphony or semantic note association. It is hypothesized that internal measure barlines can be cleanly distinguished from note stems.
- **Fixture set**: Existing tracked public fixtures `tests/fixtures/pdf/generated_standard_staff_quarter_note.pdf` and `tests/fixtures/pdf/generated_standard_staff_multi_staff.pdf`.
- **Metric**: Accurate extraction of the number of systems, staves per system, and barlines per staff.
- **Expected result**: The geometry layer correctly groups all 5-line staves into systems and identifies all vertical strokes intersecting the staff bounds as barlines.
- **Pass threshold**: 100% correct system/measure grid extraction on the bounded fixture set.
- **Fail threshold**: Any missed barline or incorrect system grouping on clean vector PDFs.
- **Stop/pivot condition**: If internal barlines are rendered as overlapping disconnected fragments in standard vector output, making deterministic geometric extraction unviable without raster vision.

## Unknowns
- Whether complex orchestral brackets/braces interfere with leading barline detection in edge cases.
- Whether standard notation barlines in standard vector fixtures consistently intersect exactly the top and bottom staff lines.

## Required Structural Primitives Assessment
| Primitive | Current Capability | Missing | Deterministic Viability |
| :--- | :--- | :--- | :--- |
| 5-line staff grouping | Supported (`pdf_staff_detection.py`) | None | Viable (proven) |
| Staff-to-system grouping | Partial (`SystemConnectorDiagnostics`) | Full system bounding box | Viable |
| Internal Barline detection | Missing for notation | Barline extraction | Hypothesis (ambiguous vs stems) |
| Measure boundary grid | Missing for notation | Measure x0/x1 logic | Hypothesis |
| Polyphony / Voice mapping | Missing | Semantic voice grouping | **Not Viable** deterministically |
| Clef/Key/Time anchors | Missing for PDF-only | Geometric anchors | Hypothesis (clef partial, key/time unknown) |

## Outcome Decision
**Outcome B**: Deterministic layout inference is not viable as first framed (if it includes polyphony and semantic voice mapping), but a narrower non-ML approach may be viable.

The narrower approach is a **Structural Layout Grid**: extracting systems, staves, and internal barlines. Because internal barline extraction is currently an unproven hypothesis, Developer implementation is explicitly NOT authorised. We must first build a diagnostic to prove viability. Polyphony and semantic note association must remain excluded.

## Required Future Diagnostic implementation
- **Hypothesis**: Standard-notation internal barlines and system bounds can be deterministically extracted from vector PDFs.
- **Fixture set**: Existing public standard-notation vector fixtures (e.g. `generated_standard_staff_multi_staff.pdf`).
- **Metric**: System count, staff count per system, and barline count per staff.
- **Pass threshold**: Perfect match on the layout grid for vector fixtures.
- **Stop/pivot condition**: Fragmented/inconsistent barline vectors.
- **Files likely to change**: `pdf_staff_notation_diagnostics.py`, `pdf_staff_geometry.py`.
- **Product behaviour to preserve**: Tab-only timing policy must remain unaffected.
- **Artifact constraints**: No private PDFs or generated artifacts committed.

## Developer implementation authorised
No. Reviewer architecture verification must approve this narrowed scope first.
