# 0027 - CR-05A PDF-Tab Barline Style Classification Seam

## Objective

Implement bounded Developer slice `CR-05A` on the PDF-tab conversion seam in `tticom/score2gp`, as authorized by the merged product architecture report `docs/design/cr05-structural-layout-and-titles-architecture.md`.

Classify PDF-tab barline candidate details into explicit, typed barline styles (`"regular"`, `"double"`, `"final"`, `"ambiguous"`, `"unclassified_stroke"`) while preserving 100% backward-compatible float `valid_barlines` arrays, `_TabSystem.barlines`, and system layout bounds.

## Authorized Product Files

- `src/score2gp/pdf_geometry.py`
- `src/score2gp/pdf.py`
- `src/score2gp/report.py`
- `tests/test_cr05_barline_style_classification.py`

No other product files in `src/` or `tests/` may be edited in this task. Do not edit `docs/design/cr05-structural-layout-and-titles-architecture.md` during this Developer implementation slice.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/next/0027-cr05a-pdf-tab-barline-style-classification.md`, `docs/design/cr05-structural-layout-and-titles-architecture.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/cr05a-pdf-tab-barline-style-classification` in `tticom/score2gp`.
6. Run `python scripts/agent_verify.py` in `score2gp` before making code modifications.

## Implementation Scope & Seam Contract

1. **`src/score2gp/pdf_geometry.py`**:
   - Extend `_LineSegment` with `primitive_kind: Literal["line", "rect_edge", "mixed"] | None`, `primitive_id: str | None`, `stroke_width: float | None`, and `source_rect_width: float | None` fields.
   - Update `_drawing_segments()` and segment merge helpers to preserve primitive metadata from PyMuPDF `page.get_drawings()`.

2. **`src/score2gp/pdf.py`**:
   - Update `filter_tab_barline_candidates()` to populate optional `barline_style: Literal["regular", "double", "final", "ambiguous", "unclassified_stroke"] | None` and `cluster_size: int | None` in candidate details dictionaries.
   - **Fail-Closed Mixed Provenance Rule**: Any candidate with `primitive_kind == "mixed"` must fail closed to `barline_style = "ambiguous"`, `final_decision = "rejected"`, `rejection_reason = "pdf_barline_mixed_primitive_provenance"`, whether evaluating as a single segment or within a cluster.
   - **Rectangle-Width Classification Rules**:
     - Narrow filled rectangles ($W_{rect} \le 4.0$ pt, e.g. $4.0 - \epsilon$): Candidates sharing the same non-null `primitive_id` (originating from two edges of a single narrow rectangle primitive) produce `barline_style = "regular"`, `cluster_size = 1`. Representative $x = \text{round}(rect.x1, 3)$ is added to `valid_barlines`.
     - Ambiguous rectangle width ($4.0 < W_{rect} \le 12.0$ pt, e.g. $4.0 + \epsilon$ and $12.0 - \epsilon$): Set `barline_style = "ambiguous"`, `final_decision = "rejected"`, `rejection_reason = "pdf_barline_ambiguous_rect_width"`.
     - Wide decorative rectangle fills ($W_{rect} > 12.0$ pt, e.g. $12.0 + \epsilon$): Set `barline_style = "ambiguous"`, `final_decision = "rejected"`, `rejection_reason = "pdf_barline_decorative_fill_or_wide_rect"`.
   - **Line & Independent Stroke Rules**:
     - For 1-stroke non-mixed candidates: set `barline_style = "regular"`, `cluster_size = 1`.
     - For 2-stroke clusters ($|x_1 - x_2| \le 12.0$ pt) from different `primitive_id` values or independent line primitives: set `barline_style = "double"`, `cluster_size = 2`.
     - If `primitive_id` is `None` (legacy caller), default to `barline_style = "double"`, `cluster_size = 2` for 2-stroke clusters.
   - For initially rejected strokes: set `barline_style = "unclassified_stroke"`, `cluster_size = None`.
   - For 3+ stroke edge clusters: retain edge representative in `valid_barlines` for backward compatibility, but set `barline_style = "ambiguous"`, `cluster_size = len(cluster)` on detail dicts.
   - Pass candidate detail dictionaries through `_TabSystem` to `report.py` diagnostics.

3. **`src/score2gp/report.py`**:
   - Update candidate detail HTML rendering to display `barline_style` and `cluster_size` metadata when present, ensuring legacy details without these fields render cleanly without errors.

4. **`tests/test_cr05_barline_style_classification.py`**:
   - Add public regression test suite covering:
     - `test_cr05a_same_drawing_multiple_lines_double_barline`
     - `test_cr05a_filled_rect_canonicalization_pipeline`
     - `test_cr05a_rectangle_width_threshold_rejections` (testing $W_{rect} \le 4.0$ pt canonicalization, $4.0 < W_{rect} \le 12.0$ pt ambiguity, and $W_{rect} > 12.0$ pt decorative rejection with $4.0/12.0 \pm \epsilon$ controls)
     - `test_cr05a_mixed_primitive_merge_fail_closed` (testing single merged `mixed` candidates fail closed to `ambiguous`)
     - `test_cr05a_null_primitive_id_fail_closed`
     - `test_cr05a_edge_triple_cluster_style_ambiguous`
     - `test_cr05a_report_html_rendering_barline_style` (testing HTML report rendering for populated and legacy candidate details)

## Validation Commands

1. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_pdf.py::test_double_barline_ambiguity_resolution`
2. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_cr05_barline_style_classification.py`
3. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python scripts/agent_verify.py`

## Non-goals

- No title classification or title ownership code changes in `CR-05A`.
- No system layout break refactoring in `CR-05A`.
- No changes to product `build_ir.py` conversion logic in `CR-05A`.
- Final-barline (thick-thin) classification is deferred until vector stroke-width oracle evidence is added.
