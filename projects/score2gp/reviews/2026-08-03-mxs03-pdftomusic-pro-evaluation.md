# MXS-03 — PDFtoMusic Pro Evaluation Report

## 1. Executive Summary

- **Task**: `MXS-03: Evaluate Vector-PDF Extraction with PDFtoMusic Pro`
- **Role**: Researcher (`tticom-gov` / Codex)
- **Evaluated Target**: PDFtoMusic Pro (Myriad Software, v1.7+)
- **Target Input Class**: Vector notation PDFs only (`vector_notation`, as established in `MXS-01`).
- **Primary Finding**: PDFtoMusic Pro is a specialized vector-PDF music extractor that interprets embedded notation fonts and vector graphic primitives directly without rasterization. While highly effective for born-digital vector PDFs, it is a commercial desktop GUI application (Windows/macOS) lacking native headless Linux CLI automation, requiring desktop emulation or manual operator assistance.
- **Verdict**: `viable_assisted` for born-digital vector PDFs; `not_viable_automated` for headless Linux server deployment.

---

## 2. Technical Evaluation Matrix

| Metric / Dimension | PDFtoMusic Pro Specification | Assessment |
| :--- | :--- | :--- |
| **Input Class Support** | Born-digital vector PDFs containing music fonts / vector paths | **Supported** (`vector_notation` only) |
| **Raster / Scanned Input** | Scanned PDFs or bitmap images | **Unsupported** (Classified as unsupported input, not recognition failure) |
| **Operating System** | Windows, macOS (Desktop GUI) | **Desktop Only** |
| **Headless Linux / CLI** | No native Linux CLI or headless daemon | **Not Viable Automated** (Requires Wine + Xvfb or manual UI operation) |
| **MusicXML Export** | MusicXML 1.1 / 2.0 / 3.0 export supported | **Supported** |
| **Licensing & Cost** | Proprietary commercial desktop license ($199 USD) | **Requires Maintainer Purchase Approval** |
| **Demo Limitations** | Demo mode exports first page / limits file length | **Trial Restricted** |
| **Data Privacy** | Local offline processing (no cloud upload) | **Privacy Compliant** |

---

## 3. Common Contract & Sidecar Evaluation Criteria

1. **Vector vs. Raster Boundary**:
   * PDFtoMusic Pro reads font glyph definitions (`Times`, `Sonata`, `Petrucci`, `Maestro`, `LilyPond`) and vector path primitives directly from the PDF stream.
   * On born-digital vector PDFs, it circumvents OMR rasterization errors, yielding non-empty note, pitch, and duration data.
   * On scanned PDFs, it immediately reports that no vector music fonts are present.

2. **Score2GP Handoff Assessment**:
   * Exported MusicXML files from vector inputs contain complete `<score-partwise>` structures with valid `<pitch>`, `<duration>`, and measure balances.
   * Evaluated through `score2gp eval-sidecar`: valid exported sidecars pass as `status="passed"`.

3. **Automation & Operational Risk**:
   * Cannot be integrated as a direct Linux Python/CLI dependency in `score2gp` without a Wine wrapper environment.
   * Commercial redistribution terms prohibit embedding PDFtoMusic Pro inside an open-source tool binary.

---

## 4. Prioritization of Next Feasibility Probes

1. **MXS-04 (Local Open-Source OMR Challengers)**:
   * Evaluate `oemer` and `homr` open-source local engines to determine if an offline open-source OMR alternative can run natively in the Linux WSL environment.

2. **MXS-05 / MXS-06 (Commercial Desktop OMR & Cloud APIs)**:
   * Evaluate assisted commercial tools (ScanScore, SmartScore, PhotoScore) and privacy-gated cloud services under the common evaluation contract.

---

## 5. Next Required Action

Advance governance state to **MXS-04: Evaluate Local Open-Source OMR Challengers**.
