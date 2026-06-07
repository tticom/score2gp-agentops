# Research: Standard-Staff Left-Margin Font/Text Density Diagnostics v0.1

## Context

The `score2gp` project is incrementally building a safe, geometry-first path for understanding born-digital PDF standard notation without crossing into musical inference too early.

Product PR #192 introduced staff-local, left-to-right primitive X-aligned clustering.

The next priority is geometry-only left-margin text/font/ink-density diagnostics.
By inspecting the geometric density and font distribution within the left margin of a staff, we can measure left-margin visual/text density without semantically decoding or parsing any values.

This research defines a private-safe schema and strategy for extracting left-margin text/font and curve density.

## Terminology and semantic boundary

Forbidden terms may appear only in refusal/boundary language, not schema names, implementation goals, or inferred meanings.

The implementation and schema MUST NOT infer or name:
- Pitch
- Clefs
- Time signatures
- Key signatures
- Rhythms
- Durations
- Musical symbols

All output is constrained to neutral geometric counts (e.g. `curve_candidate_count`, `vertical_stroke_candidate_count`).

## What is a Staff-Local Left Margin?

The "left margin" is defined purely geometrically relative to the detected standard staff bounds.
A safe heuristic is a bounded region starting at the staff's `x0` coordinate and extending rightward by a multiple of the calculated `staff_space`. 

* **Provisional Boundary:** `margin_x_limit = staff_geom.x0 + (10.0 * staff_space)`
* To prevent wide, cross-staff items (e.g., full-staff lines or sweeping slurs) from being dragged into the margin simply because their `x0` is small, margin inclusion MUST be based strictly on `center_x`.
* Any primitive whose `center_x` falls within `[staff_geom.x0, margin_x_limit]` is considered inside the left margin.

## What Geometry Primitives Are Included?

The goal is to measure left-margin visual/text density.
* `text_span`: Tracked by aggregate counts and distinct font usage without recording raw font names, preserving privacy boundaries.
* `curve_candidate`: Tracked by count to quantify curve-like primitives.
* `vertical_stroke_candidate`: Tracked by count to quantify vertical-stroke-like primitives within the margin.
* `rectangle_candidate`: Tracked by count.

## Private-Safe Schema Addition

A new field should be added to `NotationStaffDiagnostics`:
`left_margin: StaffLeftMarginAggregateDiagnostics | None`

```python
from pydantic import BaseModel, ConfigDict, Field

class StaffLeftMarginAggregateDiagnostics(BaseModel):
    model_config = ConfigDict(frozen=True)

    margin_x_threshold_staff_spaces: float = Field(ge=0.0)
    text_span_count: int = Field(ge=0)
    distinct_font_count: int = Field(ge=0)
    max_text_spans_for_single_font: int = Field(ge=0)
    curve_candidate_count: int = Field(ge=0)
    vertical_stroke_candidate_count: int = Field(ge=0)
    rectangle_candidate_count: int = Field(ge=0)
```
Raw font names are omitted to ensure robust private safety; we only log structural metadata.

## What Must Not Be Serialized

To maintain strict privacy and semantic boundaries, the following must **not** be serialized:
- Raw text content (e.g., "G", "4/4", "b", "#").
- Raw font names (e.g., "Maestro", "Arial").
- Semantic labels (e.g., "clef", "time_signature", "key_signature").
- Precise coordinate arrays or bounding boxes of the individual primitives.
- Private filenames, screenshots, or local absolute paths.

## Tests That Prove the Behavior

1. **Margin Filtering Test**: Primitives whose `center_x` is at `x0 + 5.0 * staff_space` are counted in the margin diagnostics; primitives at `x0 + 15.0 * staff_space` are excluded.
2. **Invalid Staff Space Fallback**: If `staff_space <= 0.0` or `< 2` staff lines exist, `left_margin` evaluates to `None` safely.
3. **Aggregate Accuracy**: Font counts aggregate `text_span_count`, `distinct_font_count`, and `max_text_spans_for_single_font` accurately based exclusively on items inside the margin.
4. **Semantic Gate Check**: The serialized schema does not emit forbidden terms.

## Exact Developer Prompt

```text
Title: Implement standard-staff left-margin font/text density diagnostics v0.1

Repository:
tticom/score2gp

Branch:
feature/pdf-standard-staff-left-margin-font-density-v0.1

Owner role:
Developer.

Context:
Governance PR #69 defined the geometry-only standard-staff left-margin font and text density diagnostics. We need to implement this schema safely without inferring music semantics (clefs, keys, time signatures).

Requirements:
1. Add `StaffLeftMarginAggregateDiagnostics` to `pdf_staff_geometry.py`. Include `text_span_count`, `distinct_font_count`, `max_text_spans_for_single_font`, `curve_candidate_count`, `vertical_stroke_candidate_count`, and `rectangle_candidate_count`. Use `Field(ge=0)`.
2. Add a `left_margin` field to `NotationStaffDiagnostics`.
3. In `build_notation_diagnostics(...)`, calculate a `margin_x_limit = staff_geom.x0 + (10.0 * staff_space)`.
4. Filter primitives to those whose `center_x` <= `margin_x_limit` AND `center_x` >= `staff_geom.x0`.
5. Aggregate the counts for these margin primitives.
6. If `staff_space <= 0.0`, safely set `left_margin = None`.
7. Add pure geometry tests verifying correct spatial filtering based on `center_x`.
8. Do not emit or record any raw string text, semantic labels, raw font names, or coordinates.

Validation commands:
env PYTHONPATH=src .venv/bin/python3 -m pytest tests/test_pdf_staff_geometry_diagnostics.py -v
env PYTHONPATH=src .venv/bin/python3 -m pytest tests/test_pdf_staff_left_margin_diagnostics.py -v
env PYTHONPATH=src .venv/bin/python3 -m pytest
env PYTHONPATH=src .venv/bin/python3 -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
git diff --check

Privacy checks:
git status --short
git ls-files fixtures/private work
git ls-files | grep -E "fixtures/private|work/|/home/|/mnt/|private_input|private_input_custom|\.pdf|\.gp|\.gpif|\.musicxml|\.mxl|diagnostics\.json|score\.ir\.json" || true
find . -path "./.git" -prune -o -type f -size +10M -print

Reporting format:
Verdict: Complete / Stopped Early
Branch:
PR:
Files changed:
Schema additions:
Tests added:
Validation results:
Privacy checks:
Git status:
Known limitations:
Next recommended task:
```
