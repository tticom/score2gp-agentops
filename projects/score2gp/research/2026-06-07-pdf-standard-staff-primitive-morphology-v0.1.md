# Standard-Staff Primitive Morphology Metadata Research v0.1

## Product state inspected
- Product commit: `0a775ed`
- PR #189 status: Merged (`true`)
- Date: 2026-06-07

## Existing diagnostics schema
The existing diagnostics payload is returned by `extract_notation_diagnostics_dict()` and structured using Pydantic models in `src/score2gp/pdf_staff_geometry.py`:

1. `PdfStaffNotationGeometryDiagnostics`:
   - `staves`: `list[NotationStaffDiagnostics]`
   - `status`: `str | None = "success"`

2. `NotationStaffDiagnostics`:
   - `staff`: `NotationStaffGeometry`
   - `primitives`: `LocalPrimitivesSummary`

3. `NotationStaffGeometry`:
   - `page_index`: `int`
   - `system_index`: `int`
   - `staff_index`: `int`
   - `x0`: `float`
   - `y0`: `float`
   - `x1`: `float`
   - `y1`: `float`
   - `line_y_coords`: `list[float]`

4. `LocalPrimitivesSummary`:
   - `line_count`: `int`
   - `curve_count`: `int`
   - `rect_count`: `int`
   - `text_span_count_by_font`: `dict[str, int]`

## Existing coordinate/bounding-box behaviour
The bounding box of a standard notation staff is determined by the horizontal segments that form the 5-line staff group:
- `x0`: minimum `x0`/`x1` across the 5 lines.
- `x1`: maximum `x0`/`x1` across the 5 lines.
- `y0`: minimum Y coordinate of the 5 lines.
- `y1`: maximum Y coordinate of the 5 lines.

When extracting primitive summaries (lines, curves, rectangles, text spans), the coordinates are padded vertically to capture overlapping symbols:
- `y0_padded = y0 - 20.0`
- `y1_padded = y1 + 20.0`

Primitives are counted if their bounding boxes intersect this padded staff zone: `[x0, y0_padded, x1, y1_padded]`.

## 4-tuple readiness assessment
- **page_index**: Fully supported (extracted dynamically page-by-page starting at index 1).
- **system_index**: Fully supported (determined by vertical sorting of staff groups on each page).
- **staff_index**: Hardcoded to 1. There is no multi-staff system clustering or standard/TAB system pairing implemented for standard staves.
- **local_bar_index**: **Not available**. Standard notation staves are not currently segmented into bars, and standard-staff diagnostics do not parse or align with barlines.
- **Verdict**: **Not ready for 4-tuple bar-local bucketing**. The implementation must remain staff-level only. Bar-local morphology bucketing is explicitly deferred.

## Proposed morphology taxonomy

| Category | Meaning | Safe to serialize? | Non-goal boundary |
|---|---|---|---|
| `staff_line_horizontal` | Horizontal segments whose Y-coordinates match one of the 5 staff lines. | Yes (integer count) | Never interpret as musical lines or pitches. |
| `non_staff_horizontal` | Horizontal segments inside the staff zone that do not match the 5 staff lines (e.g. ledger lines). | Yes (integer count) | Never infer note pitch, ledger line number, or duration. |
| `vertical_stroke_candidate` | Vertical line segments inside the staff zone (could represent stems or barlines). | Yes (integer count) | Never classify as stems, barlines, or standard note markings. |
| `diagonal_stroke_candidate` | Slanted/diagonal line segments inside the staff zone. | Yes (integer count) | Never classify as beams, glissandi, or ties. |
| `rectangle_candidate` | Rectangle primitives (`re` items) inside the staff zone. | Yes (integer count) | Never interpret as rests or noteheads. |
| `curve_candidate` | Bezier or other curve primitives (`c` items) inside the staff zone. | Yes (integer count) | Never interpret as noteheads, slurs, ties, or flags. |
| `text_span_by_font` | Text spans inside the staff zone, grouped by font name. | Yes (font name and integer count) | Never serialize raw character texts or unicode characters. |
| `out_of_zone_ignored` | Primitives and text spans on the page that do not fall into any padded staff zone. | Yes (integer count at page level) | Never dump coordinates of noise. |

## Proposed JSON compatibility extension
To preserve compatibility with existing diagnostics consumers, the detailed morphology counts must be placed in a new, optional Pydantic model `NotationStaffMorphology` added as a field under `NotationStaffDiagnostics`.

```python
class NotationStaffMorphology(BaseModel):
    model_config = ConfigDict(frozen=True)

    staff_line_horizontal: int
    non_staff_horizontal: int
    vertical_stroke_candidate: int
    diagonal_stroke_candidate: int
    rectangle_candidate: int
    curve_candidate: int
    text_span_by_font: dict[str, int]
    out_of_zone_ignored: int
```

Then `NotationStaffDiagnostics` is updated to:
```python
class NotationStaffDiagnostics(BaseModel):
    model_config = ConfigDict(frozen=True)

    staff: NotationStaffGeometry
    primitives: LocalPrimitivesSummary
    morphology: NotationStaffMorphology | None = None
```

This ensures:
- Existing root keys (`staves`, `status`) remain identical.
- No existing fields are removed or renamed.
- Parsing legacy payloads without `morphology` remains fully compatible.

## Privacy and redaction rules
- **No raw text**: Never serialize characters, text strings, or lyrics.
- **No PUA glyphs**: Never serialize private-use-area unicode code points or character codes.
- **No private filenames or paths**: Never log or serialize absolute paths, home directories, or private fixture names.
- **No raw coordinates**: Do not dump coordinates of individual strokes, curves, or text blocks beyond the rounded staff bounding box boundaries already exported.

## Test strategy
1. **Mock Unit Tests**: Add test cases to `tests/test_pdf_staff_geometry_diagnostics.py` verifying that `build_notation_diagnostics` accurately categorizes line segment directions (horizontal vs vertical vs diagonal), identifies staff lines from non-staff lines, and records morphology counts correctly.
2. **Integration Tests**: Verify that `extract_notation_diagnostics_dict()` includes the new `morphology` field in its serialized JSON when present.
3. **Regression Tests**: Ensure the positive-control test `test_inspect_pdf_positive_control_notation_staff_detected` and all existing tests continue to pass.

## Candidate implementation options

### Option A: Staff-level morphology counts only (Recommended)
Add the optional `morphology` field to `NotationStaffDiagnostics`, populate it during diagnostics construction, and keep standard-staff diagnostics scoped at the system/staff level.
- **Pros**: Clean, fully safe, preserves compatibility, avoids creating half-baked bar-local buckets.
- **Cons**: Does not categorize primitives by measure.

### Option B: Optional 4-tuple morphology counts
Attempt to pair standard staves with barlines to produce a synthetic `local_bar_index` and partition primitive morphology by bar.
- **Pros**: Organizes primitives by bar.
- **Cons**: High risk of breaking because standard-staff bar parsing is not yet implemented or tested. Violates the core rule of not wiring diagnostics into timing/ScoreIR.

### Option C: Defer implementation
Do not add any morphology diagnostics at this stage.
- **Pros**: Zero effort.
- **Cons**: Delays capability of classifying born-digital notation density.

## Recommended next implementation
**Option A** is the recommended next task. It provides detailed morphology classifications safely and cleanly at the staff level without altering any timing or barline logic.

## Developer prompt
Below is the developer prompt for the follow-up implementation PR:

```text
Title: Add standard-staff primitive morphology diagnostics v0.1

Goal:
Extend standard-staff diagnostics with primitive morphology counts at the staff level, preserving backwards-compatible JSON schema structure.

Instructions:
1. Define a new Pydantic model `NotationStaffMorphology` in `src/score2gp/pdf_staff_geometry.py` with:
   - `staff_line_horizontal`: int
   - `non_staff_horizontal`: int
   - `vertical_stroke_candidate`: int
   - `diagonal_stroke_candidate`: int
   - `rectangle_candidate`: int
   - `curve_candidate`: int
   - `text_span_by_font`: dict[str, int]
   - `out_of_zone_ignored`: int

2. Add `morphology: NotationStaffMorphology | None = None` to `NotationStaffDiagnostics`.

3. Update `build_notation_diagnostics` in `src/score2gp/pdf_staff_notation_diagnostics.py` to calculate these morphology counts:
   - Classify horizontal drawing lines inside the padded staff zone as `staff_line_horizontal` if they align vertically (within tolerance of 1.0) with one of the `line_y_coords`. Otherwise, classify them as `non_staff_horizontal`.
   - Classify drawing lines as `vertical_stroke_candidate` if their absolute change in X is <= 1.0 and absolute change in Y is >= 5.0.
   - Classify drawing lines as `diagonal_stroke_candidate` if they are neither horizontal nor vertical.
   - Count curves as `curve_candidate` and rectangles as `rectangle_candidate`.
   - Count text spans inside the zone by font name in `text_span_by_font`.
   - Count all drawing segments and text spans on the page that do not fall within *any* detected padded staff zone under `out_of_zone_ignored` (recorded identically for all staves on the page, or divided accordingly).

4. Ensure no raw text content or coordinates are serialized.

5. Update unit tests in `tests/test_pdf_staff_geometry_diagnostics.py` to assert correct categorization and count validation. Verify all tests pass.
```

## Stop conditions
- Implementation requires standard-staff barline pairing or timing logic modifications.
- Tests fail due to schema incompatibility.
- Raw text content or private paths are exposed.

## Privacy/artifact checks
- No private PDF names, home paths, or private data are committed.
- Large untracked directories/files are ignored.
