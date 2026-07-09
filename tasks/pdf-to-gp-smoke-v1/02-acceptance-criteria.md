# Acceptance Criteria - PDF-to-GP Smoke Integration (v1.0)

**Role**: Technical Product Owner & Sceptic
**Repository Workspace**: `score2gp-tpo`
**Target Task**: `pdf-to-gp-smoke-v1`

---

## Executive Summary: Sceptical Verdict

The Research Architect’s plan is **rejected in part** due to high architectural complexity and a significant risk of fake progress. Specifically, the proposal for a **"Global Page-Level Column Grid Alignment System"** is an over-engineered, fragile abstraction that assumes all guitar tablature engraving conforms to a perfect, spreadsheet-like vertical matrix across systems. In the real world, visual measures vary in width across rows, and projecting columns page-wide will fail on non-uniform sheets, representing clear overfitting to the "Major Triads Lesson 3" layout.

However, the Architect’s diagnosis of the root geometric bugs is highly accurate:
1. **Collinear System Splitting**: Unified horizontal staff rows are fragmented by local grouping loops, splitting single visual lines into multiple partial left/right systems.
2. **Notation-vs-TAB Staff Conflation**: Note stems/beams from the standard 5-line notation staff are processed as candidate TAB barlines, introducing massive telemetry clutter.
3. **TAB Rhythm Stem Clutter**: Vertical rhythm stems inside the 6-line TAB staff are misidentified as barlines.

These three root causes can be cleanly and robustly resolved with **local, deterministic layout logic** without resorting to complex page-wide grid projections. I will approve the task for implementation **only** if the Developer follows the narrowed scope defined below.

---

## Critical Answers

### 1. What is the real product outcome being attempted?
The ultimate product goal is converting born-digital guitar lesson PDFs plus standard notation OMR data (MusicXML) into a fully validated, inspectable, and playable Guitar Pro 7 (`.gp`) file. 
For this specific task (`pdf-to-gp-smoke-v1`), the real product outcome is taking a single private lesson PDF (**Major Triads Lesson 3**) through the safest supported conversion pipeline under strict safety gates, and outputting a mathematically valid, programmatically correct `.gp` package representing the actual musical content.

### 2. What would prove that the system has moved closer to PDF-to-GP conversion?
Real progress is proven when **100% of playable fret candidates** extracted from the PDF are successfully mapped into their correct TAB staves, string lines, and constructed bar boxes under **strict compiler mode** (with zero safety-gate bypasses, no `allow_remediation`, and no `allow_skip_unboxed`). This layout success must feed directly into the timeline alignment engine to generate a validated `ScoreIR` JSON and a validated binary `.gp` file that passes `score2gp validate` checks.

### 3. What would be fake progress?
* **"Polishing the Diagnostics Turd"**: Designing more HTML visualizers, warnings JSON structures, color-coded summaries, or beautiful error messages without actually improving the underlying layout parser to successfully assign more fret candidates to their correct measures.
* **Over-Engineering (Global Grid Projection)**: Implementing a highly complex vertical column projection system that aligns unrelated measures across systems and works only for highly structured LilyPond-style engravings, while breaking on arbitrary or uneven layouts.
* **Overfitting / Coordinate Hardcoding**: Hand-tuning margins, pixel-cushions, or bounding box limits specifically to make "Major Triads Lesson 3" compile, while breaking existing public tests.
* **Loosening Safety Gates**: Enabling compiler bypass flags to write incomplete or silent GP files just to declare the pipeline "runs to completion."

### 4. Are we only improving docs, handoffs, or diagnostics without improving conversion capability?
**Yes, currently.** The repository contains extensive documents (14 files under `docs/`) and multiple developer-facing visual reports (`grouping-diagnostics.html`, `symbol-attachment-diagnostics.html`, `musicxml-timing-diagnostics.html`), yet the actual pipeline **fails to convert a single real-world private score** because of basic, local geometric bugs. We have enough diagnostics. We must now write the clean, local layout parsing code required to bridge this gap.

### 5. Are we overfitting to synthetic fixtures?
Yes. The test suite reports a **99.7% pass rate (389 / 391 passed)** because almost all tests are written against pristine, synthetic, generated PDFs that do not contain the standard notation staff printed above the TAB staff, overlapping vectors, or clipped lines. This clean environment masked the massive layout conflation failures that occur on real engraving formats. We must introduce realistic, messy public fixtures to represent standard-notation-on-top-of-tab engraving styles.

### 6. Are private fixture results being reported safely and honestly?
Yes. The private smoke workflow (`scripts/private_e2e_smoke.py`) successfully processes private inputs from `fixtures/private/` and outputs sanitized, anonymized counts (e.g. `private_input_1`) to public summaries under ignored `work/`. The Developer must strictly maintain this Git boundary: raw private PDF/GP contents, exact note lists, and private filenames must not be copied into unrelated Git commits.

### 7. What is the smallest acceptance test that proves real progress?
Running `python scripts/private_e2e_smoke.py` on the local workspace and observing that **Major Triads Lesson 3** (`private_input_1` or custom):
1. Achieves `grouping_status = "grouped"` (no partial grouping warnings).
2. Maps **546 / 546 playable fret candidates** cleanly to systems, strings, and bars (`unassigned_to_bar = 0`).
3. Generates a validated `ScoreIR` (`score.ir.json` exists) under strict compilation (no remediation/skip flags).
4. Generates a validated `smoke.gp` package that successfully passes `score2gp validate`.
5. Passes the entire public test suite (`pytest`) with a 100% pass rate.

### 8. What should be explicitly out of scope?
* **Global Page-Level Column Projection**: Projects vertical barlines across systems. **REJECTED** as out of scope due to extreme fragility.
* **Scanned/Raster PDF Support / OCR**: The pipeline remains strictly born-digital vector-based.
* **MusicXML Timing Repair / Voice Calibration**: The voice timeline timeline cursor must remain strict; repairing bad MusicXML timing is out of scope.
* **Guitar Pro Layout/Formatting Features**: We are only interested in semantic music correctness (notes, pitches, measures), not rendering styles or page margins inside GP.

### 9. What would cause you to block the task?
* **Loosening safety gates**: Any attempt to silently discard unassigned fret candidates or allow invalid/unboxed systems to compile into ScoreIR.
* **Hardcoded Magic Numbers**: Hardcoding coordinates, page bounds, or system counts specific to "Major Triads Lesson 3".
* **Git Safety Violations**: Accidentally committing private PDF, GP, or MusicXML files under `fixtures/private/` or generated outputs under `work/` to Git.
* **Regression**: Breaking any of the existing 391 public tests.

### 10. What should the Developer implement next, if anything?
The Developer must implement exactly three focused, local layout parsing improvements under `src/score2gp/pdf.py` and write a new, realistic public synthetic test case.

---

## Developer Action Items (Scope of Work)

### Phase 1: Local Geometric Refinements (`src/score2gp/pdf.py`)

The Developer must refactor `src/score2gp/pdf.py` to add the following three local layout filters:

1. **Horizontal Collinear Line Merging**:
   * Before grouping lines into systems, the parser must merge horizontal vector segments that share the same Y-coordinate and overlap or lie collinear within a horizontal gap tolerance (e.g. 10.0 points).
   * This consolidates left/right fragments into a single, authoritative staff system spanning the full page width, completely eliminating horizontal system splitting.

2. **TAB-vs-Notation Staff Pre-Classification**:
   * Pre-classify horizontal groupings. Authoritative guitar TAB staves must have exactly six strings (or be verified as TAB staves). Standard 5-line notation staves must be identified and strictly excluded from forming or cluttering TAB systems.

3. **TAB-Grid Intersect Filtering**:
   * When filtering vertical line segments (candidate barlines), the parser must match them strictly based on whether they cleanly intersect the Y-extent of the authoritative 6-string TAB staff region.
   * Vertical paths that lie entirely inside the notation staff (note stems/beams) or are too short (rhythm stems inside the TAB staff) must be ignored, drastically reducing candidate barline telemetry noise.

### Phase 2: Synthetic Messy Public Fixture

The Developer must create a new synthetic public PDF fixture and corresponding tests to verify these layout improvements:
* **Fixture Location**: `tests/fixtures/pdf/generated_paired_notation_tab_system.pdf`
* **Layout Design**:
  * A standard 5-line notation staff printed directly above a 6-line TAB staff.
  * Real barlines crossing both staves at margins.
  * Fragmented horizontal staff vectors.
  * Cluttering vertical notation stems inside the 5-line staff and short rhythm stems inside the TAB staff.
* **Test Assertions**:
  1. The detector must identify exactly **one** TAB staff system spanning the full margins.
  2. The standard notation staff must **not** form a TAB system.
  3. No vertical note stems or TAB rhythm stems may be accepted as candidate barlines.
  4. Fret candidates must assign cleanly to strings and bars with **zero** unassigned playable tokens.

---

## Strict Acceptance Checklist

### 1. Private E2E Validation (Major Triads Lesson 3)
- [ ] `python scripts/private_e2e_smoke.py` runs to completion.
- [ ] Grouping Status is `grouped` (no `partial_pdf_grouping` or `missing_pdf_grouping` warnings).
- [ ] Total Playable Fret Candidates = **546**.
- [ ] Candidates with Bar = **546**.
- [ ] Unassigned-to-bar Count = **0**.
- [ ] `ScoreIR` is successfully compiled and written under strict compiler mode.
- [ ] `smoke.gp` is successfully written.
- [ ] `score2gp validate work/private_e2e_smoke_v0_1/private_input_1/smoke.gp` completes with **zero errors**.

### 2. Public Regression Validation
- [ ] `python -m pytest` passes with **100% pass rate** (including resolving any path-related environment issues in WSL/Windows CI).
- [ ] The new `generated_paired_notation_tab_system.pdf` test passes cleanly.
- [ ] The private-safety git invariant checks pass: `git ls-files fixtures/private work` outputs exactly `fixtures/private/.gitkeep`.

---

## Verdict

> [!IMPORTANT]
> **Plan Approved with Revisions**. 
> The Developer is instructed to implement local collinear horizontal merging, paired TAB pre-classification, and TAB-grid intersection filtering. The "Global Page-Level Column Grid Projection" is explicitly rejected as out of scope. Proceed to implementation under these narrowed constraints.
