# MXS-05 — Commercial Desktop OMR Evaluation Report

## 1. Executive Summary

- **Task**: `MXS-05: Evaluate Commercial Desktop OMR as Assisted Sidecar Producers`
- **Role**: Architect / Researcher (`tticom-gov` / Codex)
- **Primary Finding**: All four evaluated commercial desktop OMR systems (**ScanScore**, **SmartScore**, **PhotoScore**, and **PlayScore 2**) lack native headless Linux CLI automation, rendering 100% automated sidecar generation (`viable_automated`) **impossible** without desktop GUI emulation.
- **Assisted Viability**: **PhotoScore Ultimate** and **ScanScore** represent viable **assisted** sidecar producers (`viable_assisted`), where a human operator performs GUI recognition and manual timing correction before exporting MusicXML for Score2GP consumption.
- **Cost & License Guard**: No software purchases or recurring subscriptions will be authorized without explicit maintainer approval.

---

## 2. Commercial OMR Evaluation Matrix

| Commercial Tool | Platform Support | MusicXML Export | TAB Recognition | Headless Linux CLI / SDK | License / Price Model | Feasibility Classification | Exact Blocker / Technical Limitation |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: | :--- |
| **PhotoScore Ultimate** | Windows, macOS | Yes | Yes (Explicit) | No | Proprietary ($249 USD) | **`viable_assisted`** | GUI-only; requires Windows/macOS desktop & manual export. |
| **ScanScore** | Windows, macOS | Yes | Partial | No | Proprietary ($39–$149 USD) | **`viable_assisted`** | GUI-only; flags incomplete bars for manual correction. |
| **SmartScore Pro** | Windows, macOS | Yes | Partial | No | Proprietary ($199–$399 USD) | **`viable_assisted`** | GUI-only; no Linux CLI. |
| **PlayScore 2** | iOS, Android, Windows | Yes | No | No | Subscription ($29.99/yr) | **`viable_assisted`** | Mobile/desktop GUI; subscription required for MusicXML. |

---

## 3. Detailed Technical Findings

1. **Absence of Headless Linux Automation**:
   * None of the commercial OMR vendors supply a native Linux ELF executable or command-line SDK (`viable_automated`).
   * Automated execution inside Ubuntu WSL would require complex GUI display wrappers (e.g. Wine/X11 or Virtual Machines), which introduces non-deterministic environment risks.

2. **Tablature & Measure-Duration Handling**:
   * **PhotoScore Ultimate** is the only commercial tool with explicit printed guitar TAB recognition models.
   * **ScanScore** includes built-in validation that flags incomplete/overcomplete measures in GUI before allowing MusicXML export, making it a strong candidate for assisted sidecar production.

3. **Assisted Sidecar Workflow Model**:
   * In an **assisted sidecar workflow** (Outcome B), a human operator:
     1. Ingests the PDF into PhotoScore or ScanScore on a desktop.
     2. Resolves measure-duration warnings in the GUI editor.
     3. Exports `.musicxml` / `.mxl` into Score2GP's sidecar directory.
     4. Score2GP ingests the sidecar via `score2gp convert --musicxml` for 100% deterministic Guitar Pro generation.

---

## 4. Next Governance & Research Action

* **Outcome of MXS-05**: Commercial desktop OMR tools classified as **`viable_assisted`** (no automated Linux CLI).
* **Next Tasks**:
  - **MXS-06 (Evaluate Cloud/API Routes Behind a Privacy Gate)**: Audit cloud APIs (e.g. Soundslice Data API) for MusicXML export terms, privacy, and rate limits.
  - **MXS-07 (Measure Assisted Manual Entry Control)**: Measure active human entry time as the baseline control.
