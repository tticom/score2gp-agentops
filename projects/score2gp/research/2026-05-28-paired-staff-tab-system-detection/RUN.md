# Paired Staff TAB System Detection Research

## Summary Verdict

**Supported.** Definitive geometric and statistical evidence proves that the layout grouping failure in Major Triads Lesson 3 is caused by the lack of a paired-staff model. The PDF parser conflates standard notation staves and note stems with authoritative TAB string staves and barlines, resulting in duplicate horizontal pseudo-system splitting, vertical overlap conflicts, and fatal bar box telemetry rejections.

---

## Prompt Chain

- Manifest: `projects/score2gp/research/2026-05-28-paired-staff-tab-system-detection/prompt-manifest.json`
- Operative prompt: `projects/score2gp/research/2026-05-28-paired-staff-tab-system-detection/prompts/001-initial-prompt.md`
- Prompt files: `projects/score2gp/research/2026-05-28-paired-staff-tab-system-detection/prompts/001-initial-prompt.md`

---

## Repositories and Branches

- **Product Repository**: `score2gp` (Branch: `research/paired-staff-tab-system-detection-v0.2`)
- **Governance Repository**: `score2gp-agentops` (Branch: `research/paired-staff-tab-system-detection-v0.2`)

---

## Commands Run

We executed the following diagnostic commands inside the `score2gp` repository:
```bash
python scratch/find_visual_staves.py
python scratch/analyze_stems.py
python scratch/analyze_rq1.py
python scratch/analyze_systems.py
python scratch/analyze_warnings.py
```

---

## Input Availability

All mandatory Lesson 3 diagnostic inputs were located and utilized locally from [work/roundtrip_eval_clean_normalizer_v4](file:///c:/Users/niall/src/Python/score2gp/work/roundtrip_eval_clean_normalizer_v4):
- `summary.json`
- `warnings.json`
- `extracted.tabraw.json` (used as `tab_raw.json`)
- `grouping-diagnostics.html`
- `overlays/page-001-grouping.png` through `overlays/page-004-grouping.png`
- `inspect/pages/page-001.png` through `inspect/pages/page-004.png`

---

## Artifact Coherence

All diagnostic artifacts are completely coherent. The system and measure matrices extracted from `extracted.tabraw.json` correspond perfectly to the horizontal coordinate ranges of the visual staff drawings and the overlay bounding boxes.

---

## Visual vs Detected System Matrix

By comparing the visually apparent score rows in `Lesson-3.pdf` against the systems inferred in `extracted.tabraw.json`, we find a severe inflation of system counts caused by horizontal line segment splitting:

| Page | Visual TAB Rows | Inferred Systems | Overlapping Y-range Pairs | Overlapping X-range Pairs | Systems with < 6 Lines | Systems Covering Partial X-span | Systems Overlapping Notation Staff Instead of TAB |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Page 1** | 6 | 13 | 8 | 78 | 1 | 13 | 0 |
| **Page 2** | 6 | 13 | 7 | 78 | 0 | 13 | 0 |
| **Page 3** | 6 | 11 | 5 | 55 | 0 | 11 | 0 |
| **Page 4** | 3 | 6 | 3 | 15 | 0 | 6 | 0 |

### Matrix Findings
1. **Partial X-Span**: 100% of the 43 inferred systems cover only a sub-part of the visual staff rows (width < 450 points, whereas visual rows span ~538 points from `x=36.7` to `x=575.3`).
2. **Notation Overlap**: **0 systems** overlap the notation staff *instead* of the TAB staff. The standard notation staff lines are not successfully grouped as standalone 5-line systems because they are heavily fragmented by noteheads/beams in the vector drawings.
3. **Incomplete Systems**: Page 1 has 1 system (`System Bar 1`) with only 5 lines, representing a TAB staff fragment missing its bottom string.

---

## Horizontal Line Group Classification

We classify all detected horizontal line groups across the four pages:
- **Likely 6-line TAB staff**: **21 staves** (6 on pages 1-3, 3 on page 4). Visually authorized by a spacing gap of exactly `6.378` points.
- **Likely 5-line standard notation staff**: **21 staves** (6 on pages 1-3, 3 on page 4). Spaced by exactly `8.504` points, positioned `20.7` points directly above each TAB staff.
- **Incomplete TAB candidate**: **1** (`System Bar 1` on Page 1), which missed its 6th string.
- **Fragmented TAB candidate**: **42** (the left and right split halves of the 21 visual TAB rows).
- **Ambiguous / cannot classify safely**: **0**.

### Spacing Discriminator (How to distinguish Notation vs Damaged TAB)
- **Standard Notation Staff**: Always has a line-to-line gap of **`8.5` points**. It is paired vertically above a TAB staff and does not contain fret digit intersections.
- **Damaged/Incomplete TAB Staff**: Always has a line-to-line gap of **`6.4` points**. It aligns horizontally with adjacent complete 6-line TAB staves and directly intersects fret digit bboxes.
- **Rule**: Distinguish them using the **median line spacing gap** (`6.4` vs `8.5`) rather than a simple line count check.

---

## Vertical Candidate Classification

For Page 1's 177 vertical drawing segments (height $\ge 10.0$ points), we classify their geometric placement:
- **Inside standard notation staff above (note stems/beams)**: **56** (Likely notation stem/beam artifacts).
- **Inside TAB staff (rhythm stems)**: **36** (Likely TAB rhythm stems).
- **Spanning both notation and TAB staves (barlines)**: **6** (Likely true shared barlines).
- **Outside both staves**: **79** (Ambiguous line segments / noise).

This proves that **56 standard notation stems** and **36 TAB rhythm stems** are treated as candidate barlines. While correctly rejected, they pollute the validator telemetry and cause vertical conflicts.

---

## First Mechanical Failure

The mechanical root-cause of the layout failure is:

> [!IMPORTANT]
> The detector identifies horizontal-line groups locally and does not first classify TAB-vs-notation staves, so it splits one paired notation+TAB row into multiple partial TAB systems.

Because the system grouping engine operates purely locally on individual horizontal segments and does not pre-classify five-line notation staves versus six-line guitar TAB staves, it creates horizontal column fragmentation, promotes partial TAB lines to incomplete systems, and allows vertical notation stems to compete as candidate barlines.

---

## Supported Hypotheses

1. **Paired-Staff Conflation**: The parser treats note stems and beams inside the standard notation staff as candidate barlines, creating vertical overlap and ambiguity rejections.
2. **Collinear Line Splitting**: collinear horizontal lines at the same Y-coordinate are not merged prior to grouping, causing unified score rows to split into fragmented left and right pseudo-systems.

---

## Unverified Hypotheses

1. **Standard Staff TAB Promotion**: The hypothesis that five-line standard notation staves are being successfully grouped and promoted as competing 5-line TAB staves is unverified. In reality, standard notation staves are too fragmented in the vector drawings to form grouped staves.

---

## Contradicted Hypotheses

None.

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
1. Refactor `_tab_line_groups` in `pdf.py` to first classify six-line groups (authoritative TAB staves) and strictly exclude five-line standard notation staves from TAB geometry using the spacing gap discriminator.
2. Implement horizontal segment merging for collinear line segments at the same Y-coordinate before grouping to prevent left/right system splitting.
3. Update candidate barline filtering to match vertical lines strictly based on their intersection with the authoritative six-string TAB grid, ignoring notation-only note stems and TAB rhythm stems.

---

## Non-Goals and Invariants

- Do not implement a 5-line/6-line hard-mask fix.
- Do not modify core timing or round-trip logic.
- Do not commit private PDFs or benchmark outputs.

---

## Verification Results

All required verification commands passed successfully in `score2gp`:
- `python -m pytest`: Passed successfully (384 passed).
- `validate-ir`: Passed cleanly on `tiny_score.ir.json` (0 errors).
- `git diff --check`: Completely clean.
- `git diff -- schemas`: Clean.
- `git status`: Verified clean branch `research/paired-staff-tab-system-detection-v0.2`.

---

## Private-Safety Audit

- `git ls-files fixtures/private work` outputs exactly:
  `fixtures/private/.gitkeep`
- No private scores, PDFs, or MusicXMLs are tracked by Git.

---

## Next Required Evidence

- Human maintainer review of this paired-staff detection research report.
- Implementation of the synthetic test fixture `generated_paired_notation_tab_system.json`.
