# MXS-02 — Audiveris Control Baseline Evaluation Report

## 1. Executive Summary

- **Task**: `MXS-02: Establish the Current Audiveris Control`
- **Role**: Researcher (`tticom-gov` / Codex)
- **Primary Finding**: Audiveris 5.7.0 batch transcription (`-batch -transcribe -export`) achieves 100% note recognition on single standard-staff control PDFs (`generated_standard_staff_whole_note.pdf`), but **produces zero `note` and zero `rest` elements (100% empty MusicXML)** on mixed notation/TAB fixtures (`generated_paired_notation_tab_system.pdf` and `generated_paired_notation_tab_system_double_barline.pdf`).
- **Stop/Pivot Triggered**: In accordance with the research plan contract (`projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`), because Audiveris yields `empty_musicxml` on all mixed notation/TAB fixtures, **no Audiveris integration work will be undertaken**. The research plan immediately pivots to **MXS-03 (PDFtoMusic Pro vector extraction)** and **MXS-04 (Local OMR challengers like `oemer`)**.

---

## 2. Evaluation Contract Matrix (`score2gp eval-sidecar`)

Each Audiveris 5.7.0 exported MusicXML sidecar was evaluated using the candidate-neutral evaluation harness (`score2gp eval-sidecar --sidecar <mxl> [--pdf <pdf>] --json`):

| Fixture Name | Input PDF Class | Audiveris Part / Measure Count | Audiveris Note / Rest Count | `score2gp eval-sidecar` Status | Refusal / Classification Reason | ScoreIR Event Count |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: |
| `generated_standard_staff_whole_note.pdf` | Standard Staff Control | 1 Part, 1 Measure | 1 Note, 0 Rests | **`passed`** | `None` (Valid C5 Whole Note) | 1 Event |
| `generated_paired_notation_tab_system.pdf` | Paired Notation/TAB | 2 Parts, 2 Measures | 0 Notes, 0 Rests | **`empty_musicxml`** | `zero_notes_and_rests` | 0 Events |
| `generated_paired_notation_tab_system_double_barline.pdf` | Structural Mixed Variant | 2 Parts, 2 Measures | 0 Notes, 0 Rests | **`empty_musicxml`** | `zero_notes_and_rests` | 0 Events |
| `generated_tiny_tab.pdf` | Known-Good Control | 1 Part, 1 Measure | 6 Notes, 0 Rests | **`passed`** | `None` (Reference Oracle) | 2 Events |

---

## 3. Log Analysis & Upstream Diagnostic Root Cause

Sanitized Audiveris execution logs reveal the exact upstream failure mode:

1. **Dual-Staff Scale & Grid Detection**:
   Audiveris correctly detects two line-clusters (Staff #1 standard 5-line staff, Staff #2 6-line TAB staff).
2. **Clef Recognition Warnings**:
   `ClefBuilder: Clef recognition warning: Staff#1 no recognized header clef, Staff#2 no recognized header clef.`
3. **Measure Fixer Timing Failure**:
   `MeasureFixer: System#1 No target duration for measures local IDs [1, 2], please check time signatures.`
4. **Zero-Note Output Mechanism**:
   Because Audiveris's OMR glyph classifier does not possess a TAB clef or 6-line guitar-tablature grammar model, it drops all notehead and fret candidates on Staff #2 and fails to resolve pitch/duration steps for Staff #1, emitting valid XML `<part>` and `<measure>` containers with **zero `<note>` or `<rest>` elements**.

---

## 4. Determinism & Provenance Check

- **Two-Run Determinism**: 100% deterministic (XML score structure, note counts, and refusal reasons identical across two clean runs).
- **Runtime Environment**: Ubuntu 24.04 LTS x86_64, Audiveris 5.7.0 (`/opt/audiveris/bin/Audiveris`).
- **Invocation**: `Audiveris -batch -transcribe -export -output <dir> -- <pdf>`

---

## 5. Next Governance & Research Action

* **Outcome of Audiveris Evaluation**: Audiveris is **NOT VIABLE** as an automated sidecar generator for mixed notation/TAB scores.
* **Next Task**: Promote **MXS-03: Evaluate Vector-PDF Extraction with PDFtoMusic Pro** and **MXS-04: Evaluate Local Open-Source OMR Challengers (`oemer`)** into `ACTIVE_TASK.md`.
