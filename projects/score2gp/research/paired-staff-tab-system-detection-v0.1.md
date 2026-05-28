# ScoreToGP Research Report: Paired-Staff TAB System Detection (v0.1)

- **Repository**: `score2gp-agentops` and `score2gp`
- **Branch**: `research/paired-staff-tab-system-detection-v0.1`

---

## Summary Verdict

Paired-staff conflation is **supported** by definitive geometric and statistical evidence. The current PDF grouping engine fails to distinguish standard notation staves from guitar tablature (TAB) staves, leading to duplicate, competing, and fragmented pseudo-systems that split unified score rows and cause fatal downstream overlaps.

---

## Visual vs Detected System Matrix

By comparing the visually apparent score rows in `Lesson-3.pdf` against the systems inferred in `work/roundtrip_eval_clean_normalizer_v4/extracted.tabraw.json`, we find a severe inflation of system counts caused by horizontal line segment fragmentation and overlapping staff regions:

| Page | Visual TAB Rows | Inferred Systems | Overlapping Y-range Pairs | Overlapping X-range Pairs | Systems with < 6 Lines | Systems Covering Partial X-span |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Page 1** | 6 | 13 | 8 | 78 | 1 | 13 |
| **Page 2** | 6 | 13 | 7 | 78 | 0 | 13 |
| **Page 3** | 6 | 11 | 5 | 55 | 0 | 11 |
| **Page 4** | 3 | 6 | 3 | 15 | 0 | 6 |

### Analysis of the Matrix
1. **Horizontal Splitting**: Every single inferred system (43 total) has a horizontal width of less than 450.0 points, while the visual staff rows span from the left margin to the right margin (approx. 538 points, from `x=36.7` to `x=575.3`). Because `_tab_line_groups` loops through sorted horizontal lines and groups them based on local Y-coordinates without merging overlapping or collinear segments first, it splits single visual staff rows into separate left and right systems.
2. **Incomplete Systems**: On Page 1, `System Bar 1` is detected with only `5 lines` (`y_range=[145.507, 171.019]`), which represents a fragment of the 6-line TAB staff that missed its bottom string (`177.397`).

---

## Geometry Findings

### RQ1: Is the parser splitting one real TAB row into multiple pseudo-systems?
**Yes.** As shown in the matrix above, the parser is splitting single visual TAB rows horizontally across columns. For instance, on Page 1:
- `System Bar 2` covers `x_range=[36.709, 318.430]`, `y_range=[145.507, 177.397]`.
- `System Bar 3` covers `x_range=[232.809, 575.291]`, `y_range=[145.507, 177.397]`.

These two systems overlap horizontally from `232.8` to `318.4` and share the exact same Y-coordinates, meaning they are fragments of a single physical TAB row. Because they are treated as two distinct systems, they create vertical bar box overlaps and confuse measure/bar calculations.

### RQ2: Is the parser confusing notation-staff geometry with TAB-staff geometry?
**Yes.** The parser evaluates vertical lines within `y0 - 15.0` to `y1 + 15.0` of the TAB staff. Because standard notation is printed directly above the TAB staff (with a spacing of `~20.7` points), the note stems and beams from the standard staff are evaluated as candidate barlines.

On Page 1, our classification of vertical segments reveals:
- **Total vertical segments**: 177
- **Inside standard notation staff above (note stems/beams)**: 56
- **Inside TAB staff (rhythm stems)**: 36
- **Spanning both notation and TAB (true barlines)**: 6
- **Outside both**: 79

This means **56 standard notation note stems** and **36 TAB rhythm stems** are mistakenly processed as candidate barlines. While most are correctly rejected (generating 34 `pdf_barline_does_not_cross_staff` and 34 `pdf_barline_outside_staff_region` warnings), they create massive amounts of telemetry noise and lead to false positive barline matches in complex regions.

### RQ3: Are standard-notation staff lines being included in TAB system detection?
**No, but standard staves affect grouping indirectly.** 
- **Standard Notation Lines**: The five lines of the standard staff have a spacing of `8.504` points, and they do not form a "six-horizontal-lines" group. While they could theoretically be grouped as an incomplete 5-line system, they are not grouped because their horizontal segments are highly fragmented and broken in the vector drawings due to overlapping noteheads, ledger lines, and stems.
- **Incomplete TAB Systems**: The only 5-line system detected (`System Bar 1` on Page 1) is a 6-string TAB staff that missed its 6th string segment because it was already grouped or missing.
- **Conflation mechanism**: The critical issue is that because the detector identifies horizontal-line groups locally and does not first classify TAB-vs-notation staves, it splits one paired notation+TAB row into multiple partial TAB systems and processes notation-only barlines and stems.

---

## Failure Mechanism

The mechanical root-cause of the layout failure is:

> [!IMPORTANT]
> The detector identifies horizontal-line groups locally and does not first classify TAB-vs-notation staves, so it splits one paired notation+TAB row into multiple partial TAB systems.

Because the system grouping engine operates purely locally on individual horizontal segments and does not pre-classify five-line notation staves versus six-line guitar TAB staves, it creates horizontal column fragmentation, promotes partial TAB lines to incomplete systems, and allows vertical notation stems to compete as candidate barlines.

---

## Recommended Public Fixture

We recommend adding a synthetic fixture `fixtures/public/generated_paired_notation_tab_system.json` (or PDF) modeling a paired score row:

- **Structure**:
  - A standard 5-line notation staff above (Y-range: `[100, 134]`, gap: `8.5`).
  - A 6-line TAB staff below (Y-range: `[154, 186]`, gap: `6.4`).
  - True barlines spanning both staves at `x=36`, `x=300`, and `x=575`.
  - Notation-only note stems strictly inside `[100, 134]`.
  - TAB rhythm stems inside `[154, 186]`.
  - Fret numbers positioned on the TAB string lines.

- **Expected Assertions**:
  1. The detector must identify exactly **one** TAB staff row.
  2. The standard notation staff must **not** be counted as a TAB system.
  3. The TAB row must have exactly **six** string lines.
  4. Fret numbers must assign strictly to the six TAB strings.
  5. Notation-only stems and TAB rhythm stems must **not** be accepted as TAB barlines.
  6. Ambiguous/fragmented line groupings must refuse safely.

---

## Recommended Implementation Slice

We recommend the following implementation task:

> [!TIP]
> **Implementation Task**:
> 1. Refactor `_tab_line_groups` in `pdf.py` to first classify six-line groups (authoritative TAB staves) and strictly exclude five-line standard notation staves from TAB geometry.
> 2. Implement horizontal segment merging for collinear line segments at the same Y-coordinate before grouping to prevent left/right system splitting.
> 3. Update candidate barline filtering to match vertical lines strictly based on their intersection with the authoritative six-string TAB grid, ignoring notation-only note stems and TAB rhythm stems.
