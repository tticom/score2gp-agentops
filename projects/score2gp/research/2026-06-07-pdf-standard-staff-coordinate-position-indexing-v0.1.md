# Standard-Staff Coordinate Position Indexing Research v0.1

## Product state inspected
- Product commit: `2dcf4e4`
- PR #190 status: Merged (`true`)
- Date: 2026-06-07

## Existing staff geometry schema
The `NotationStaffGeometry` model in `src/score2gp/pdf_staff_geometry.py` represents the bounding box and line coordinates of a standard notation staff:
```python
class NotationStaffGeometry(BaseModel):
    model_config = ConfigDict(frozen=True)

    page_index: int = Field(ge=1)
    system_index: int = Field(ge=1)
    staff_index: int = Field(default=1, ge=1)
    x0: float
    y0: float
    x1: float
    y1: float
    line_y_coords: list[float]
```

## Existing morphology schema
The `NotationStaffMorphology` model in `src/score2gp/pdf_staff_geometry.py` records staff-level primitive morphology counts:
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
```

## Coordinate indexing problem
To analyze standard-staff vector drawings and text spans (e.g. for noteheads or notation symbols) in later stages, we need to map raw Y coordinates from the PDF coordinate space into discrete vertical locations on the staff (lines and spaces). 

Because PDFs can be scaled arbitrarily, we must normalize raw coordinates relative to the detected staff's dimensions.

## Proposed staff-space formula
Given the sorted vertical coordinates of the 5 staff lines:
```text
line_y_coords = [y0, y1, y2, y3, y4]
```
The spacing between adjacent lines is:
```text
gaps = [y1 - y0, y2 - y1, y3 - y2, y4 - y3]
```
The average line-to-line spacing is calculated as the median of the gaps to protect against drawing noise:
```text
staff_space = median(gaps)
half_staff_space = staff_space / 2
top_line_y = y0
```

## Proposed staff-position index formula
To index positions vertically:
- Let `0` be the top staff line (`y0`).
- Let `1` be the space below the top line.
- Let `2` be the second line, and so on, down to `8` (the bottom staff line, `y4`).

For a candidate Y coordinate:
```text
raw_staff_position = (candidate_y - top_line_y) / half_staff_space
nearest_staff_position_index = round(raw_staff_position)
snap_delta = abs(raw_staff_position - nearest_staff_position_index)
```

## Snap tolerance recommendation
The snap tolerance should be defined in normalized staff-position units rather than raw PDF points to automatically adapt to arbitrary page/staff scaling.

A tolerance of `0.25` normalized staff-position units is recommended:
- The distance between a line and an adjacent space is `1.0` normalized unit.
- A snap tolerance of `0.25` means coordinates must fall within the window `[-0.25, +0.25]` around the center of a line or space to snap successfully.
- This leaves a `0.5` unit "dead zone" in the middle, preventing ambiguous coordinates from snapping incorrectly.
- In the positive-control fixture (`staff_space = 8`, `half_staff_space = 4`), `0.25` units corresponds to `0.25 * 4 = 1.0` PDF point. For a larger scaled variant (`staff_space = 12`, `half_staff_space = 6`), it automatically scales to `1.5` PDF points.

## Ambiguous / unsnapped coordinate handling
If `snap_delta > tolerance`, the coordinate is considered unsnapped/ambiguous. The helper will return:
- `snapped: False`
- `nearest_staff_position_index` (as a fallback, but marked as unsnapped)

## Above-staff and below-staff coordinate handling
Ledger lines and spaces extend the geometric index naturally:
- Coordinates above the top line produce negative indexes (`index < 0`). For example, the space immediately above the top line is `-1`, and the first ledger line above the staff is `-2`.
- Coordinates below the bottom line produce indexes greater than 8 (`index > 8`).
- Handling remains purely mathematical and geometric, making no musical assumptions.

## What this must not mean
- **No pitch inference**: An index of `0` is the top line of the staff, not an F5 or G4. No clefs are interpreted.
- **No key or accidental inference**: No key signatures or accidentals are processed.
- **No notehead inference**: Noteheads are not parsed.
- **No timing or rhythm inference**: Coordinates do not map to durations, rests, voices, or beats.
- **No ScoreIR integration**: Index values are strictly diagnostic and are not compiled into musical events.

## Private-safe diagnostics schema options
To maintain privacy:
- No raw coordinate lists, text character strings, or PUA glyphs will be serialized.
- We can add `staff_space` as a float to the `NotationStaffGeometry` schema.

## Candidate implementation options

### Option A: Add staff-space summary only
Add only `staff_space: float` to the `NotationStaffGeometry` schema and serialize it.
- **Pros**: Smallest schema change.
- **Cons**: Does not implement the indexing normalization math.

### Option B: Add staff-position indexing helper with tests only (Recommended)
Add a pure helper function `snap_coordinate_to_staff_position` to `src/score2gp/pdf_geometry.py` with comprehensive unit tests, but do not change the serialized JSON payload.
- **Pros**: Implements and tests the mathematical indexing model, does not pollute JSON payloads with raw coordinate dumps, completely private-safe, ready for downstream geometry checks.
- **Cons**: Helper is internal-only in v0.1.

### Option C: Defer implementation
Do not add any helper or metadata at this stage.
- **Pros**: Zero effort.
- **Cons**: Delays vector alignment capabilities.

## Recommended next implementation
**Option B** is recommended. It cleanly implements the mathematical geometry helper and tests it against scaled and positive-control coordinates without serializing raw drawing data.

## Developer prompt
Below is the developer prompt for the follow-up implementation PR:

```text
Title: Add standard-staff coordinate snapping helper v0.1

Goal:
Implement a pure coordinate-to-staff-position snapping helper in `src/score2gp/pdf_geometry.py` and cover it with unit tests.

Instructions:
1. In `src/score2gp/pdf_geometry.py`, define a helper function:
   ```python
   def snap_coordinate_to_staff_position(
       candidate_y: float,
       line_y_coords: list[float],
       tolerance: float = 0.25
   ) -> tuple[float, int, float, bool]:
       """
       Convert a raw Y coordinate near a 5-line standard staff into normalized
       staff-position units, returning:
         (raw_staff_position, nearest_staff_position_index, snap_delta, snapped)
       """
       if len(line_y_coords) != 5:
           raise ValueError("Standard staff must have exactly 5 lines.")
       
       sorted_ys = sorted(line_y_coords)
       gaps = [sorted_ys[i+1] - sorted_ys[i] for i in range(4)]
       
       # Calculate median gap
       gaps.sort()
       staff_space = (gaps[1] + gaps[2]) / 2.0 if len(gaps) % 2 == 0 else gaps[len(gaps) // 2]
       half_staff_space = staff_space / 2.0
       top_line_y = sorted_ys[0]
       
       raw_staff_position = (candidate_y - top_line_y) / half_staff_space
       nearest_index = round(raw_staff_position)
       snap_delta = abs(raw_staff_position - nearest_index)
       snapped = snap_delta <= tolerance
       
       return raw_staff_position, nearest_index, snap_delta, snapped
   ```

2. Add comprehensive unit tests in `tests/test_pdf_staff_geometry_diagnostics.py` verifying:
   - Snapping on line and space coordinates using the positive-control staff lines `[100.0, 108.0, 116.0, 124.0, 132.0]`.
   - Handling of scaled coordinates (e.g. line spacing = 12.0).
   - Behavior of negative indexes above the top line (e.g. Y = 96.0 -> index -1, snapped).
   - Behavior of indexes below the bottom line (e.g. Y = 136.0 -> index 9, snapped).
   - Behavior of unsnapped coordinates in the dead zones (e.g. Y = 102.5 -> raw = 0.625, index 1, snapped=False).

3. Verify that all 525 tests in the repository remain green.
```

## Stop conditions
- Helper relies on clefs, pitches, timing, or ScoreIR.
- Helper serialization dumps raw coordinates.

## Privacy/artifact checks
- No private filenames or paths are committed.
- Large untracked directories/files are ignored.
