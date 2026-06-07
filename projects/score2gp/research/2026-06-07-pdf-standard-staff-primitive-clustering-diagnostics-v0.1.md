# PDF Standard-Staff Primitive Clustering Diagnostics v0.1

## Summary

This research defines a safe, geometry-only architecture for staff-local primitive clustering diagnostics in born-digital PDFs. The goal is to geometrically group staff-local primitives (lines, curves, text spans) into localized left-to-right clusters without crossing the boundary into musical semantics like pitch, rhythm, or symbol classification.

## Baseline and evidence inspected

- Product PR #191 is merged, which provides the pure math helper `compute_staff_position_index(...)` in `src/score2gp/pdf_geometry.py`.
- Current morphology diagnostics in `pdf_staff_geometry.py` only provide aggregate counts of primitives (lines, curves, rects, text spans) across the entire staff bounding box.
- The `ScoreIR` and timing logic pipelines are successfully isolated from `pdf_staff_notation_diagnostics.py`.

## Problem

Global staff-level morphology counts do not capture horizontal spatial density. To evaluate alignment strategies between TAB and standard notation geometrically, we need an "x-density map" showing where clusters of primitives occur along the X-axis. However, grouping primitives risks accidentally building a symbol classifier (inferring noteheads, clefs, stems) which violates the core project rules separating geometric diagnostics from notation interpretation.

## X-axis clustering tolerance analysis

To group primitives horizontally, a tolerance based on the normalized `staff_space` is required.
- **0.25 * staff_space**: Too tight. May artificially split primitives belonging to the same vertical alignment group (e.g., a dot slightly separated from a line).
- **0.5 * staff_space**: Balanced default. Likely to safely group horizontally contiguous ink while keeping distinct neighboring spatial clusters separate.
- **0.75 * staff_space**: May start grouping very tightly spaced but distinct symbols.
- **1.0 * staff_space**: Too wide. Will merge distinct adjacent clusters in dense passages.

**Recommendation:** Use `0.5 * staff_space` as the provisional default tolerance for x-axis clustering, ensuring distinct neighboring primitives are kept in separate spatial clusters.

## Safe definition of a staff-local primitive cluster

A staff-local primitive cluster is a bounded group of PDF drawing/text primitives that:
- belongs to one detected standard staff region,
- has a finite, relative bounding box,
- is grouped only by geometric proximity or horizontal overlap,
- is ordered by x-position from left-to-right,
- exposes aggregate morphology counts and normalized geometry for the localized area,
- does not identify the musical meaning or rhythmic duration of the grouped content.

## Included primitive types

Clusters should group only the geometry families already present safely in staff morphology diagnostics:
- curve-like primitives,
- short line segments (horizontal, vertical, diagonal),
- compact filled/outlined shapes (rectangle candidates),
- text-like primitives / text spans by font.

## Vertical stroke inclusion logic

A `vertical_stroke_candidate` should be included in an `x_aligned_cluster` based purely on geometry. Inclusion criteria:
- X center distance from the cluster center normalized by `staff_space`.
- X-range overlap after `staff_space` expansion.
- Y-range intersection after `staff_space` expansion.
- Minimum normalized vertical height.

Do not refer to these candidates as `stem` objects except in explicit boundary/refusal language.

## Explicitly excluded primitive types or meanings

Do not introduce, infer, or attempt to classify symbol categories such as:
- clef,
- accidental,
- notehead,
- rest,
- beam,
- stem,
- flag,
- dot,
- tie,
- slur,
- time signature,
- key signature.

## Staff-local bounding model

Each cluster has a relative bounding box (`x_min`, `x_max`, `y_min`, `y_max`). These coordinates must be relative to the staff bounding box or normalized, avoiding raw absolute page coordinates that could expose layout-specific details.

## Left-to-right ordering model

Clusters must be ordered strictly by geometric `x_min` or their centroid's X-coordinate. The `x_order` index simply reflects geometric sequence from left to right. It implies absolutely no rhythmic or temporal sequence.

## Cluster identity and stability

Clusters should be assigned a deterministic `cluster_index` based on their `x_order`. Re-running the diagnostics on the same un-warped input PDF must produce the exact same cluster count and ordering.

## Use of staff-position indexing

Can `compute_staff_position_index(...)` be safely used for cluster centroid diagnostics?
**Yes, but strictly for normalized geometry-only placement.**
It may be used to calculate a `centroid_staff_position_index` to describe the geometric center of the cluster. It must not be interpreted as pitch, clef-relative note name, ledger semantics, or voice.

## Aggregate-only diagnostics schema recommendation

For v0.1, the schema should bias heavily toward aggregate fields. Any per-cluster detailed coordinate arrays should be explicitly deferred or kept optional for a later version unless absolutely necessary.

```json
{
  "staff_index": 1,
  "x_aligned_cluster_count": 12,
  "max_primitives_per_x_aligned_cluster": 5,
  "clusters_with_vertical_stroke_candidate": 8,
  "max_cluster_vertical_span_staff_spaces": 4.5,
  "cluster_primitive_count_summary": {
    "lines_total": 24,
    "curves_total": 36,
    "rects_total": 0,
    "text_spans_total": 4
  }
}
```

## What must not be serialized

The diagnostics payload must avoid:
- raw absolute page coordinates,
- private filenames or local paths,
- raw text content or extracted lyrics,
- raw glyph names,
- ScoreIR event references or IDs,
- extracted pitch, timing, or rhythmic metadata.

## Test strategy

Use public synthetic fixtures only.
1. Empty staff region produces zero clusters.
2. Staff-local primitives are grouped by geometric proximity.
3. Clusters are ordered left-to-right deterministically.
4. Cluster indexes are stable for the same input.
5. Primitive counts are aggregate-only.
6. Staff-position index is used only for centroid geometry.
7. No pitch/clef/rhythm/notehead names appear in diagnostics schemas.
8. Import-boundary tests verify `ScoreIR`/timing/TAB modules do not import the new cluster modules.

## Import-boundary and architecture risks

- **Symbol classification creep:** Primitive clustering may accidentally evolve into symbol classification if developers try to optimize groupings for "notes" vs "clefs". Strict naming (e.g., `cluster`, `centroid`) prevents this.
- **Rhythmic confusion:** Cluster `x_order` may be mistaken for rhythmic order. The schema documentation must clarify that visual spacing is not authoritative rhythm evidence.
- **Pitch confusion:** `centroid_staff_position_index` may be mistaken for pitch.
- **Leakage:** Diagnostics imports may leak into product conversion paths.

## Recommendation

`Safe to implement with constraints`

## Terminology safety review

The following semantic boundaries are strictly observed:
- `compact_shape_candidate` is used instead of `notehead` or `notehead_candidate`.
- `vertical_stroke_candidate` is used instead of `stem`.
- `x_aligned_cluster` is used instead of `chord`, `beat`, or `onset`.
- Forbidden semantic terms (e.g., notehead, pitch, duration, rhythm, stem, chord, beat, onset, ScoreIR event) appear only in explicit boundary/refusal language.

## Exact Developer prompt if safe

Title: Implement standard-staff primitive clustering diagnostics v0.1

Repository:
`tticom/score2gp`

Branch:
`feature/pdf-standard-staff-primitive-clustering-diagnostics-v0.1`

Owner role:
Developer implementing Architect recommendation from `tticom/score2gp-agentops`.

Context:
The governance research `2026-06-07-pdf-standard-staff-primitive-clustering-diagnostics-v0.1.md` has approved staff-local left-to-right primitive clustering diagnostics.

Goal:
Implement a geometry-only clustering helper `cluster_x_aligned_primitives(...)` that groups primitives located within a standard staff into `x_aligned_cluster` lists ordered left-to-right. Calculate their aggregate morphology counts. Focus on the aggregate diagnostics schema first (e.g. `x_aligned_cluster_count`).

Non-goals:
Do not infer pitch, clef, notehead, rhythm, duration, voice, beat, onset, stem, chord, ScoreIR, or playback semantics. Do not propose full per-cluster coordinate arrays for v0.1. Do not modify `ScoreIR`, TAB alignment, or timing generation.

Likely files:
- `src/score2gp/pdf_staff_geometry.py` (to update schemas)
- `src/score2gp/pdf_staff_notation_diagnostics.py` (to implement the geometric clustering algorithm)
- `tests/test_pdf_staff_geometry_diagnostics.py` (to add tests)

Exact boundaries:
Add the aggregate fields (e.g., `x_aligned_cluster_count`) to the existing diagnostics schema. Keep it fully backward compatible. Do not include detailed per-cluster coordinates.

Expected tests:
Add unit tests using public synthetic fixtures to prove `x_aligned_cluster` groups are formed deterministically and that no symbol semantics leak into the output.

Validation commands:
`pytest tests/test_pdf_staff_geometry_diagnostics.py`
`pytest`

Privacy checks:
Do not commit private PDFs, generated diagnostics, screenshots, or local absolute paths.

Stop conditions:
Stop if you need private PDFs to test, or if the clustering logic requires inferring pitch, rhythm, chords, or musical timing.

Reporting format:
Provide a standard implementation summary with "Verdict", "Files changed", and "Validation performed".

## Stop conditions for implementation
Stop and report instead of continuing if:
- The design cannot avoid pitch/rhythm/notehead/clef/timing/ScoreIR implications.
- The research suggests product implementation would require schema changes larger than a small reviewable PR.
- The research reveals diagnostics imports already leaking into ScoreIR/build/timing/TAB modules.
- Privacy checks show private or generated artifacts are tracked.

## Validation performed
- Verified PR #67 is merged.
- Read-only grep checks performed to confirm clean isolation of `StaffPositionIndex` and `pdf_staff_notation_diagnostics.py`.
- No product code modified.

## Privacy review
- No private PDFs, filenames, absolute paths, raw text contents, or raw coordinate dumps are used. Synthetic schema uses abstract variable names.
