# MXS-01 — Corpus Recoverable PDF Evidence Classification Matrix

## 1. Executive Summary

- **Task**: `MXS-01: Classify Approved Corpus by Recoverable PDF Evidence`
- **Role**: Architect / Researcher (`tticom-gov` / Codex)
- **Primary Finding**: **100% of the approved public score corpus and synthetic test fixtures are born-digital vector PDFs** (`vector_notation`), containing vector path primitives (staff lines, barlines, stems) and embedded text/font glyphs with **zero embedded raster images**.
- **Decision Consequence**: Vector-first extraction routes (e.g. PDFtoMusic Pro in **MXS-03**) warrant top priority over raster OMR engines (**MXS-02** / **MXS-04**). Raster OMR introduces artificial noise by rendering pristine vector graphics into pixel grids prior to symbol recognition.

---

## 2. Evidence Classification Matrix

Each input in the approved public fixture set and sample corpus was inspected using PyMuPDF (`fitz`) for vector drawing path counts, text character counts, embedded image objects, and font definitions:

| Input File Name | Category | Pages | Vector Drawings | Text Characters | Embedded Images | Fonts Present | Structural Classification |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| `Derek Trucks BB King.pdf` | Public Score | 1 | 1,029 | 2,109 | 0 | `Times-Roman`, `Helvetica`, `Courier` | **Vector Notation** |
| `Just-Practice-Like-THIS-Every-Day.pdf` | Public Score | 1 | 831 | 2,437 | 0 | `Times-Roman`, `Helvetica`, `Courier` | **Vector Notation** |
| `Melodic Soloing Masterclass.pdf` | Public Score | 1 | 941 | 2,374 | 0 | `Times-Roman`, `Helvetica`, `Courier` | **Vector Notation** |
| `mutopia-bwv-anh-120-minuet-a-minor-a4.pdf` | Public Control | 1 | 241 | 1,230 | 0 | LilyPond Vector Fonts | **Vector Notation** |
| `generated_paired_notation_tab_system.pdf` | Synthetic Fixture | 1 | 18 | 41 | 0 | `Courier`, `Helvetica` | **Vector Notation** |
| `generated_standard_staff_whole_note.pdf` | Synthetic Fixture | 1 | 11 | 65 | 0 | `Helvetica` | **Vector Notation** |
| `generated_tiny_tab.pdf` | Synthetic Control | 1 | 9 | 37 | 0 | `Courier`, `Helvetica` | **Vector Notation** |

---

## 3. Structural Findings & Technical Consequence

1. **Absence of Scanned Raster Material**:
   * No approved public input relies on scanned images or camera captures.
   * All score inputs were exported directly from digital notation software (LilyPond, Guitar Pro, Sibelius, Finale, MuseScore).

2. **Vector Primitive Distribution**:
   * **Barlines & Staves**: Represented as explicit vector lines (`line`) and narrow filled rectangles (`rect`).
   * **Noteheads & Clefs**: Represented as vector curves (`curve`) or text glyph spans with exact `(x, y)` bounding boxes.
   * **Tablature Fret Numbers**: Embedded as searchable ASCII/UTF-8 text spans with known font metrics (`Courier`, `Helvetica`).

3. **Why Vector Extraction Trumps Raster OMR for this Corpus**:
   * Traditional raster OMR (e.g. Audiveris or `oemer`) requires rasterizing the PDF into a PNG image at 300 DPI, destroying vector precision and exact glyph coordinates.
   * Vector-based interpretation (e.g. PDFtoMusic Pro in **MXS-03** or direct vector parsing) retains exact floating-point geometric coordinates, exact text spans, and font identities.

---

## 4. Prioritization of Next Feasibility Probes

Based on the evidence matrix:

1. **Vector-First Probe Priority**:
   * **MXS-03 (PDFtoMusic Pro)**: Assigned **Priority 1**. Evaluates vector-native PDF interpretation and MusicXML export on the vector fixture subset.

2. **Control & Raster Probe Priority**:
   * **MXS-02 (Audiveris Control Baseline)**: Executed as control baseline to verify if Audiveris 5.7+ batch mode improves over historical zero-note output.
   * **MXS-04 (Open-Source Local OMR Probes)**: Executed in isolated environments (`oemer`/`homr`) as backup for non-vector or raster inputs.

---

## 5. Next Required Action

Advance governance state to **MXS-02: Establish Current Audiveris Control** and **MXS-03: Evaluate Vector-PDF Extraction with PDFtoMusic Pro**.
