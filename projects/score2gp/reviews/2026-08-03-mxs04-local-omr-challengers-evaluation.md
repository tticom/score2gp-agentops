# MXS-04 — Local Open-Source OMR Challengers Evaluation Report

## 1. Executive Summary

- **Task**: `MXS-04: Evaluate Local Open-Source OMR Challengers`
- **Role**: Architect / Researcher (`tticom-gov` / Codex)
- **Primary Target Evaluated**: `oemer` (End-to-end open-source OMR system, MIT License, repository: `https://github.com/BreezeWhite/oemer`).
- **Primary Finding**: `oemer` is **NOT VIABLE** as a production sidecar generator for Score2GP. It requires image rasterization of vector PDFs, pulls ~250MB of unverified external PyTorch checkpoint weights at runtime, adds multi-gigabyte PyTorch/Torchvision dependencies, and lacks 6-line guitar tablature grammar models.
- **Stop/Pivot Triggered**: In accordance with the research plan stop criteria (`projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`), because `oemer` relies on unverified external weights, multi-gigabyte dependencies, and fails on TAB staves, it is rejected from product integration consideration. The research plan advances to **MXS-05 (Commercial Desktop OMR Probes)** and **MXS-06 (Privacy-Gated Cloud API Probes)**.

---

## 2. Evaluation Contract Matrix (`score2gp eval-sidecar`)

| Candidate System | License & Provenance | Input Type Required | External Weight Dependency | `score2gp eval-sidecar` Verdict | Technical / Refusal Reason |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **`oemer` (v0.1.x)** | MIT (`BreezeWhite/oemer`) | Raster Image (PNG/JPG) | Yes (~250MB PyTorch Checkpoints) | **`not_viable`** | Requires PDF rasterization; missing TAB staff grammar; heavy PyTorch footprint. |
| **`Audiveris 5.7.0`** | AGPLv3 (Java Desktop) | Vector / Raster PDF | No (Rule-based + Tesseract) | **`empty_musicxml`** | 0 notes/rests on mixed TAB scores (evaluated in `MXS-02`). |

---

## 3. Detailed Feasibility Assessment

1. **Model & Weight Provenance**:
   * `oemer` downloads unverified PyTorch checkpoint weights from GitHub Releases on initial execution.
   * Governance policy prohibits adding unverified external model weights or non-deterministic ML inference to core product dependencies.

2. **Image Rasterization Requirement**:
   * `oemer` cannot ingest vector PDFs directly; it requires converting PDFs into 300 DPI PNG images via `pdf2image` + `poppler`.
   * For born-digital PDFs (which represent 100% of the public corpus per **MXS-01**), rasterization discards exact vector paths, text spans, and font bounding boxes.

3. **Tablature & System Layout Limitations**:
   * `oemer` UNet segmentation models are trained exclusively on standard 5-line notation staves.
   * When presented with a mixed 5-line notation + 6-line TAB system, `oemer` fails to segment TAB staff lines or map fret numbers to pitch/duration events.

---

## 4. Next Governance & Research Action

* **Outcome of MXS-04**: Local ML-based OMR engines (`oemer`) are **REJECTED** for product dependency.
* **Next Task**: Promote **MXS-05: Evaluate Commercial Desktop OMR** and **MXS-06: Evaluate Cloud/API Routes Behind a Privacy Gate** into `ACTIVE_TASK.md`.
