# PDF standard-staff glyph extraction feasibility v0.1

## 1. Current verified state

We verified that PR #180 has been successfully merged into `main` in `score2gp` (commit `38471a4`), introducing:
* An internal standard-staff timing event model: [PdfStaffTimingEvent](src/score2gp/pdf_staff_timing.py)
* An alignment orchestration layer: [PdfStaffTabTimingAligner](src/score2gp/pdf_staff_tab_timing_aligner.py)
* Synthetic unit tests covering boundaries, unmatched events, rest alignments, and reverse/forward ambiguities.

All 510 tests pass successfully.

## 2. Scope and non-goals

The scope is restricted to investigating the feasibility of standard staff glyph extraction from born-digital vector PDFs using PyMuPDF and recommending the next minimal developer-ready step.

**Non-goals**:
* Implementing full standard notation noteheads or duration parsing.
* Wiring standard staff timing into existing Guitar Pro conversion output.
* Altering current PDF-only conversion behavior.
* Utilizing visual spacing as authoritative duration.
* Requiring MusicXML/MXL, OCR (Tesseract), or Audiveris.

## 3. Current PyMuPDF extraction usage

Currently, `score2gp` uses PyMuPDF (`fitz`) APIs in [pdf.py](src/score2gp/pdf.py) as follows:
* `page.get_drawings()`: To extract vector graphic primitives (lines `l`, rectangles `re`, and Bezier curves `c`).
* `page.get_text("blocks")` / `page.get_text("words")`: To retrieve text blocks and words (specifically digit characters representing fret numbers).
* `page.get_text("dict")`: To obtain block/line/span dictionaries (specifically for ASCII tab parsing).

No specialized music glyph parser or external PDF rendering engines are used.

## 4. Standard staff detection and discard point

In `score2gp/pdf.py`, lines are parsed and grouped into 5-line and 6-line staves inside `_tab_line_groups`. They are then classified by `classify_staff_line_group` based on median gap height and fret digit intersections:
* **Discard Point**: In `_detect_tab_systems` (lines 3832-3836):
  ```python
  for group in _tab_line_groups(horizontal):
      classification = classify_staff_line_group(group, page)
      if classification in ("notation", "ambiguous"):
          continue
  ```
  Groups classified as standard `"notation"` or `"ambiguous"` are currently skipped and discarded.
* **Barline Inheritance Exception**: Notation staff lines are temporarily parsed during notation-to-TAB barline inheritance (lines 3858-3962). If a TAB system lacks barlines, it searches for a vertically aligned notation staff within `250.0` points above it and copies its barlines. However, the notation staff itself is not persisted in the resulting models or output.

## 5. Available timing-relevant PDF evidence

An audit of the private PDF test fixtures reveals that born-digital PDFs in the dataset fall into two distinct evidence classes:

### Class A: SMuFL Font-Based Notation (e.g. `Class A SMuFL-font fixture`)
* **Text Spans**: Standard notation symbols are encoded as actual text characters mapped to a music font (e.g., `GPBravuraRegular` which is a Standard Music Font Layout (SMuFL) font).
* **Glyph Codepoints**: Codepoints are stored in the SMuFL Private Use Area (PUA) range (e.g., `\ue050` for treble clef, `\ue081\ue082\ue088` for time signature components, `\ue0a4` for black noteheads, `\ue1e7` for eighth rests).
* **Extraction Feasibility**: Highly feasible. PyMuPDF's `page.get_text("dict")` extracts these spans with precise bounding boxes, text strings, and font names.

### Class B: Pure Vector-Drawn Notation (e.g. `Class B vector-drawn fixture`, `Class B secondary vector-drawn fixture`)
* **Vector Primitives**: There are zero text spans or music fonts for standard notation. Instead, noteheads, stems, rests, clefs, flags, and beams are drawn using raw Bezier curves (`c`), lines (`l`), and rectangles (`re`). For example, in the Class B vector-drawn fixture Page 1, there are 343 drawings consisting of `{'c': 1152, 'l': 821, 're': 36}` primitives.
* **Extraction Feasibility**: Complex. Extracting timing requires clustering lines (stems, beams), curves (oval noteheads, rests), and rectangles (rests, half/whole rests), which is highly dependent on coordinate heuristic matching.

## 6. First feasible notation evidence target

We recommend starting by **preserving detected notation staff groups** rather than discarding them, and gathering **private-safe geometry diagnostics** (counts of primitive shapes and text spans near notation staves).

This provides:
1. Complete visibility into the coordinates, layout, and count of notation staves per page.
2. Safe count summaries of available primitives (lines, curves, and fonts/text) within the vertical band of the notation staff.
3. A non-intrusive foundation for subsequent SMuFL glyph extraction and vector shape heuristic classifiers without altering conversion output.

## 7. Risks and unknowns

* **Unicode/SMuFL Translation**: Standard music fonts map symbols to Private Use Area (PUA) unicode code points. We will need a mapping library or dictionary to translate these code points into actual musical symbols (e.g. `\ue0a4` -> black notehead, `\ue1e7` -> eighth rest).
* **Vector Grouping Complexity**: Class B PDFs draw noteheads as filled paths and stems as vertical lines. Small PDF coordinate offsets or exporter differences can make robust classification complex.
* **Multi-Voice Timing overlap**: Multiple voices on the same standard staff can complicate horizontal alignment and require voice categorization.

## 8. Recommended diagnostics

Introduce a private-safe diagnostics model `PdfStaffNotationDiagnostics` containing:
* `notation_staves`: List of detected notation staff bounding boxes `(page, system_index, x0, y0, x1, y1)`.
* `local_primitives_summary`: Counts of `lines`, `curves`, `rectangles`, and `text_spans` (grouped by font name) found within the bounding box of each notation staff expanded by a small vertical padding (e.g. `20.0` points above/below).

No raw text characters or exact coordinate offsets of individual noteheads should be stored to prevent score leakage.

## 9. Architecture seam

We recommend introducing:
* `src/score2gp/pdf_staff_geometry.py`: Houses internal classes to represent notation staff groups.
* `src/score2gp/pdf_staff_notation_diagnostics.py`: Houses extraction rules and summary builders for private-safe diagnostics.

## 10. Public synthetic test strategy

Create public synthetic test cases verifying:
* **Preservation**: Standard staff line groups (5-line horizontal systems) are preserved as notation staves.
* **Grouping**: Notation staves are correctly grouped and paired with the nearest TAB systems on the page.
* **Diagnostics Count**: Extracting counts of lines, curves, and Bravura-font text spans near a synthetic standard staff matches expected targets.

## 11. Privacy assessment

* The privacy invariant holds.
* No private PDFs or raw score contents will be tracked.
* Only aggregated counts of primitives and font names are recorded in diagnostics.

## 12. Recommendation

We recommend proceeding with **Option A**: `feature/pdf-staff-notation-geometry-diagnostics-v0.1`.
This task introduces the internal notation staff preservation models and populates private-safe diagnostics about nearby primitives, proving the pipeline structure before attempting real glyph parsing.

---

## 13. Smallest developer-ready implementation prompt

### Title
Implement PDF standard-staff notation geometry diagnostics v0.1

### Context
We have proved the standard-staff to TAB alignment layer using synthetic test data in PR #180. To proceed, we need to gather real data from born-digital PDFs about what standard notation staff geometry and primitive evidence (vector drawings and text spans) are present, before writing actual glyph parsers.

### Current verified state
* The standard-staff alignment models exist in `src/score2gp/pdf_staff_timing.py` and `src/score2gp/pdf_staff_tab_timing_aligner.py`.
* In `src/score2gp/pdf.py`, standard notation staff groups (length-5 line groups) are detected but discarded at the end of `_detect_tab_systems`.

### Goal
Preserve detected standard notation staff line groups and generate private-safe diagnostics summarizing drawing primitives (lines, curves, rectangles) and text spans (by font) located within the vertical region of those notation staves.

### Non-goals
* Do not parse noteheads, stems, rests, or duration values.
* Do not wire timing alignment into the Guitar Pro conversion output yet.
* Do not alter PDF-only conversion behavior or output files.
* Do not expose raw coordinate dumps or private text content in diagnostics JSON files.

### Constraints
* Pythonic naming conventions (snake_case filenames, PascalCase classes).
* The privacy invariant must hold: only `fixtures/private/.gitkeep` is tracked.

### Required pre-flight checks
* Confirm git working tree is clean on main.

### Implementation guidance
1. **Define Notation Staff Models**:
   Create `src/score2gp/pdf_staff_geometry.py`. Define `PdfNotationStaff` representing a detected standard notation staff with page index, system index, bounding box `(x0, y0, x1, y1)`, and line Y-coordinates.
2. **Preserve Notation Staves**:
   In `src/score2gp/pdf.py`, update `_detect_tab_systems` or extract tab systems flow to collect and return list of `PdfNotationStaff` objects instead of discarding groups classified as `"notation"`.
3. **Build Primitives Diagnostics**:
   Create `src/score2gp/pdf_staff_notation_diagnostics.py`. Implement a helper to count all drawing items (`l`, `c`, `re`) and text spans (grouped by font name) from PyMuPDF page content that fall within the vertical boundaries of each `PdfNotationStaff` (expanded vertically by `20.0` points padding above and below).
4. **Output JSON Summary**:
   Export these counts inside the `inspect_pdf` JSON output under `pdf_staff_notation_diagnostics`.

### Validation
Run the full test suite and confirm 100% pass:
```bash
wsl sh -c "cd /home/tticom/work/score2gp-workspace/score2gp && env PYTHONPATH=src .venv/bin/python3 -m pytest -q"
```

### Acceptance criteria
* `PdfNotationStaff` is defined.
* Notation staves are preserved instead of discarded.
* Private-safe primitive counts are exported to inspection JSON.
* Tests verify correct preservation and counts with synthetic pages.
* No conversion behavior changes.

### Stop conditions
* If any private score content is exposed.
* If any test in the existing suite fails.

---

## 14. Evidence and commands run

* We verified PR #180 is merged on main in `score2gp`.
* Ran audits in WSL:
  * `wsl sh -c "cd /home/tticom/work/score2gp-workspace/score2gp && .venv/bin/python3 scratch/inspect_drawings.py"`
  * Output: Bravura music font text spans in Class A PDFs, and raw lines/curves drawings in Class B PDFs.

## 15. Limitations / what was not verified

* The exact mapping from Bravura unicode characters to musical durations remains to be constructed.
* Vector drawings curve-fitting heuristics for notehead shapes are not verified in code yet.

## 16. Mandatory Evidence Record

* **Repository and Branch**:
  * `score2gp-agentops`: `research/pdf-standard-staff-glyph-extraction-feasibility-v0.1`
  * `score2gp`: `main`
* **Command(s) Run**:
  * `wsl sh -c "cd /home/tticom/work/score2gp-workspace/score2gp-agentops && git diff --check main...HEAD"`
  * `wsl sh -c "cd /home/tticom/work/score2gp-workspace/score2gp && env PYTHONPATH=src .venv/bin/python3 -m pytest"`
* **Input Availability**:
  * `Class A SMuFL-font fixture`
  * `Class B vector-drawn fixture`
  * `Class B secondary vector-drawn fixture`
* **Output Directory Path**: None (research only)
* **Strict Conversion Status**: `unverified`
* **Remediation / Diagnostic Status**: `unverified`
* **Generated File Existence**: `no`
* **Semantic Round-Trip Status**: `unverified`
* **Exact Blocker Category**: `PDF standard-staff glyph extraction feasibility`
* **Private-Safe Metrics**:
  * Count of Bravura-font spans and drawing primitives audited across Class A and Class B fixtures.
* **Public Tests Run**:
  * `tests/test_pdf_staff_tab_timing_aligner_alignment.py` (all 7 passed, 510/510 passed overall)
* **Private-Safety Audit**:
  * `git ls-files fixtures/private work` outputs only `fixtures/private/.gitkeep` in both repos: `yes`
  * No raw coordinates, score details, or unapproved names committed: `yes`
* **Next Required Evidence**:
  * Output diagnostics in the inspection JSON showing notation staff preservation coordinates and local primitive counts.

## 17. Prompt Chain Reference

* **Operative Prompt**: `projects/prompts/04-reviewer.md`
* **Prompt Chain Context**: This run/research record was finalized and verified under the reviewer role instructions in `projects/prompts/04-reviewer.md` to satisfy evidence and prompt metadata rules.

