# MXS-06 — Cloud/API Routes Privacy Evaluation Report

## 1. Executive Summary

- **Task**: `MXS-06: Evaluate Cloud/API Routes Behind a Privacy Gate`
- **Role**: Architect / Researcher (`tticom-gov` / Codex)
- **Primary Finding**: Cloud/API routes are **REJECTED** for Score2GP sidecar generation. Soundslice's Data API provides MusicXML export for existing hosted notation, but **does not perform PDF recognition or OMR**. Third-party web converters fail privacy/terms gates due to unverified data retention, potential AI model-training usage, and lack of headless Linux API automation.
- **Privacy Gate Verdict**: In accordance with project privacy policy (`AGENT_CONTROL.md` & `tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`), **zero score uploads occurred**. Cloud/API routes are classified as **`not_viable`** for automated PDF sidecar production.

---

## 2. Cloud Service Privacy & Technical Audit Matrix

| Cloud Service / API | MusicXML Export API | PDF OMR Capabilities | Data Retention Policy | Model Training Usage | Headless API Automation | Privacy & Technical Verdict |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: |
| **Soundslice Data API** | Yes | No (Hosts existing notation) | Persistent Cloud Storage | Disclosed | Yes (REST API) | **`not_viable`** (No PDF-to-MusicXML OMR) |
| **Cloud Vision APIs** (AWS / GCP / Azure) | No | No (General text OCR only) | Configurable | Opt-out | Yes | **`not_viable`** (No music semantics or MusicXML) |
| **Third-Party Web Converters** | Varies | Unverified | Unclear / Retained | Unverified | No (Web UI only) | **`rejected_privacy_gate`** (Unverified retention & training terms) |

---

## 3. Detailed Privacy & Terms Evaluation

1. **Soundslice API Distinction**:
   * Soundslice's Data API offers `GET /api/v1/scores/{id}/musicxml/` to retrieve MusicXML for notation already stored in a Soundslice account.
   * Crucially, the API **does not ingest PDF scores to produce MusicXML sidecars**. It cannot replace PDF recognition or sidecar generation.

2. **Privacy Gate & Data Retention Enforcement**:
   * Third-party online PDF-to-MusicXML web converters lack formal data deletion APIs, SLA guarantees, or explicit non-training clauses.
   * Uploading score inputs to unverified cloud services violates Score2GP's strict offline, privacy-first evidence contract.

---

## 4. Next Governance & Research Action

* **Outcome of MXS-06**: Cloud/API routes are **REJECTED**. All Score2GP sidecar processing must remain local, offline, and privacy-safe.
* **Next Task**:
  - **MXS-07 (Measure Assisted Manual Entry Control)**: Audit assisted manual entry (e.g. via MuseScore / Guitar Pro editor) as the active human entry control for accuracy and time per page.
  - **MXS-08 (Run the Blind Comparative Bake-Off)**: Assemble comparative matrix across evaluated candidates (Audiveris, PDFtoMusic Pro, `oemer`, PhotoScore/ScanScore, Manual Entry).
