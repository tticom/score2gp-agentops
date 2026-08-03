# Architecture Decision Record (ADR) — MXS-09: MusicXML Sidecar Generation Alternatives

## 1. Context & Problem Statement

Score2GP relies on a MusicXML sidecar to supply semantic musical timing, time signatures, key signatures, and score structure when converting PDFs to Guitar Pro files (`score2gp convert --musicxml`).

Historically, Audiveris 5.7.0 was used as the default sidecar generator. However, task **FS-03E** and evaluation **MXS-02** established that Audiveris 5.7.0 emits 100% empty MusicXML (`empty_musicxml`, 0 notes, 0 rests) on mixed notation/TAB scores because it lacks 6-line guitar-tablature grammar models and TAB clef classifiers.

Conversely, task **FS-03F** proved that when Score2GP receives a valid, non-empty MusicXML sidecar (`generated_tiny_tab.musicxml`), the conversion pipeline executes cleanly, yielding **8 valid ScoreIR events** and **6 matched playable TAB candidates** for `gp-write`.

To resolve the sidecar generation gap, the project authorized the [MusicXML Sidecar Generation Alternatives Research Plan](file:///home/tticom-codex/work/score2gp-workspace/score2gp-agentops/projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md) (**MXS-00** through **MXS-08**).

---

## 2. Decision Outcome

**Selected Architecture Outcome**: **Outcome B — Adopt an Assisted Sidecar Workflow**.

The project formally adopts an **Assisted Sidecar Ingestion & Validation Architecture** using **PDFtoMusic Pro** (for born-digital vector PDFs) and **PhotoScore Ultimate / ScanScore** (for printed/scanned notation and TAB scores) as primary assisted sidecar generators.

---

## 3. Rationale & Evaluation Summary

Based on the empirical bake-off matrix (**MXS-08**):

1. **Rejection of Outcome A (`viable_automated`)**:
   * No candidate qualifies as a fully automated, headless Linux CLI tool.
   * Audiveris 5.7.0 emits 0 notes on mixed TAB scores (`empty_musicxml`).
   * `oemer` requires downloading ~250MB of unverified external PyTorch weights, adds multi-gigabyte dependencies, forces 300 DPI image rasterization of pristine vector PDFs, and lacks TAB staves grammar.
   * Cloud APIs fail privacy gates (unverified data retention / training terms, lack of PDF OMR APIs).

2. **Justification for Outcome B (`viable_assisted`)**:
   * **100% Public Corpus Vector Material**: Task **MXS-01** proved 100% of approved public score inputs are born-digital `vector_notation` PDFs.
   * **High Accuracy & Reduced Labor**: PDFtoMusic Pro (vector extraction) and PhotoScore Ultimate (printed TAB OMR) achieve 100% `score2gp eval-sidecar` status `passed` following brief operator GUI verification, reducing human labor from ~15 minutes per page (manual entry) down to ~2–5 minutes per page.
   * **Deterministic Conversion Pipeline**: Once a valid sidecar passes `score2gp eval-sidecar`, Score2GP's internal conversion pipeline (`score2gp convert --musicxml`) remains 100% deterministic and reproducible.

---

## 4. Operational & Governance Boundary

1. **Operator Validation Boundary**:
   * Every assisted sidecar must be validated using `score2gp eval-sidecar --sidecar <file> [--pdf <pdf>] --json`.
   * Sidecars returning `empty_musicxml`, `timing_invalid`, or `handoff_refused` must be corrected in the desktop GUI editor before ingestion by `score2gp convert`.

2. **Sidecar Provenance Manifest**:
   * Every assisted sidecar ingested by Score2GP must be accompanied by a machine-readable provenance manifest recording:
     - `generator_tool`: `pdftomusic_pro` | `photoscore_ultimate` | `scanscore` | `musescore_manual`
     - `generator_version`: Exact software version string
     - `operator_id`: Identity of human operator
     - `operator_labor_minutes`: Active human entry/correction time
     - `sidecar_sha256`: SHA-256 hash of the `.musicxml` / `.mxl` file
     - `pdf_sha256`: SHA-256 hash of the input PDF score
     - `eval_status`: Must equal `"passed"`

3. **Cost & Licensing Guard**:
   * No software purchases or recurring cloud subscriptions will be made without explicit maintainer authorization.

---

## 5. Smallest Next Implementation Task

* **Task ID**: **MXS-10 — Formalize Assisted Sidecar Ingestion & Provenance Manifest Contract**
* **Owning Repository**: `tticom/score2gp`
* **Assigned Role**: Developer (`tticom-automation`)
* **Scope**: Add `--sidecar-manifest` CLI support to `score2gp convert`, validate sidecar SHA-256 hashes against `SidecarEvaluationResult`, and record sidecar provenance in generated conversion reports.
