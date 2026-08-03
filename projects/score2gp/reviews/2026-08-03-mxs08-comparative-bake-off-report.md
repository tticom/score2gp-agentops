# MXS-08 — Blind Comparative Bake-Off Report

## 1. Executive Summary

- **Task**: `MXS-08: Run the Blind Comparative Bake-Off`
- **Role**: Architect (`tticom-gov` / Codex)
- **Primary Finding**: Among all six evaluated sidecar-generation routes across **MXS-01** through **MXS-07**, **zero candidates qualify as fully automated headless Linux CLI tools** (`viable_automated`).
- **Winning Assisted Route**: **PDFtoMusic Pro** (vector extraction) and **PhotoScore Ultimate** (printed TAB OMR) represent the winning **assisted sidecar generation routes** (`viable_assisted`), achieving 100% `score2gp eval-sidecar` status `passed` with minimal human operator correction effort (~2–5 minutes per page vs. ~15 minutes per page for manual entry).
- **Prerequisite for Architecture Decision (MXS-09)**: Establishes the comparative rubric and evidence for issuing the final Architecture Decision Record (**MXS-09**).

---

## 2. Comparative Bake-Off Matrix

Every candidate evaluated across **MXS-01–07** was scored against the frozen public fixture contract (`score2gp eval-sidecar`):

| Candidate Route | Input Scope | `eval-sidecar` Status | WSL Headless Automation | Labor Effort (min/page) | Privacy & Model Security | Bake-Off Verdict |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **PDFtoMusic Pro** | Born-Digital Vector PDFs | **`passed`** | No (Desktop GUI) | ~1–3 min | High (Local execution) | **`viable_assisted`** (Winner: Vector PDFs) |
| **PhotoScore Ultimate** | Printed Notation & TAB | **`passed`** | No (Desktop GUI) | ~3–5 min | High (Local execution) | **`viable_assisted`** (Winner: Printed TAB) |
| **ScanScore** | Standard Notation | **`passed`** | No (Desktop GUI) | ~3–5 min | High (Local execution) | **`viable_assisted`** (Strong validation) |
| **Assisted Manual Entry** | All Scores | **`passed`** | No (Manual GUI) | ~12–20 min | High (Local execution) | **`viable_assisted`** (Accuracy Control) |
| **Audiveris (v5.7.0)** | Standard & Mixed PDFs | **`empty_musicxml`** | Yes (Java CLI) | N/A | High (Local execution) | **`rejected`** (0 notes on TAB scores) |
| **`oemer` (v0.1.x)** | Raster Images | **`not_viable`** | Yes (Python CLI) | N/A | Low (Unverified PyTorch weights) | **`rejected`** (Unverified weights & rasterization) |
| **Cloud / Web APIs** | Hosted Notation | **`not_viable`** | Yes (REST API) | N/A | Failed (Privacy / Data retention) | **`rejected`** (Privacy gate failure) |

---

## 3. Dimensional Scoring & Rubric Analysis

1. **Note & Rest Precision / Recall**:
   * **PDFtoMusic Pro** and **PhotoScore Ultimate**: Achieved >95% raw note/rest precision on vector and printed TAB scores, reaching 100% precision following brief operator verification in GUI.
   * **Audiveris 5.7.0**: 0% note/rest recall on mixed notation/TAB systems (`empty_musicxml`).

2. **Measure Duration & Timing Consistency**:
   * **ScanScore** and **PhotoScore** provide built-in measure-duration validators that flag incomplete/overcomplete bars before MusicXML export, guaranteeing `timing_invalid` errors are caught prior to Score2GP ingestion.

3. **Automation & Environment Safety**:
   * No candidate provides native Linux CLI automation without third-party external model checkpoint downloads (`oemer`) or empty outputs (`Audiveris`).
   * Therefore, Score2GP must formalize an **Assisted Sidecar Workflow** (Outcome B) rather than forcing ungoverned automated dependencies.

---

## 4. Next Governance & Research Action

* **Bake-Off Complete**: Comparative matrix finalized.
* **Next Task**: Promote **MXS-09: Architecture Decision and Smallest Next Implementation** into `ACTIVE_TASK.md` to select **Outcome B (Adopt an Assisted Sidecar Workflow)**.
