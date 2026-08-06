# CR-04A Current-Runtime Lesson-5 Evidence Replay Report

**Date**: 2026-08-06  
**Task**: CR-04A: Current-Runtime Lesson-5 Evidence Replay  
**Repository**: `tticom/score2gp` / `tticom/score2gp-agentops`  
**Authorised Identity**: `tticom-automation`  
**Role**: Architect  

---

## 1. Executive Summary & Objective

Task `CR-04A Evidence Replay` evaluates whether the historical false 1920-tick half rest recorded in the Lesson-5 ledger still reaches the current conversion pipeline on product `origin/main` (commit `a9b127c311617dced5422e97e46a7bab840f7981`, containing `ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`).

**Decision Gate Verdict**: **`DEFECT_NOT_REPRODUCED`**.  
On current product `origin/main`, `Lesson-5.pdf` conversion fails closed at stage `layout-gating` with refusal code `pdf_only_tab_grouping_unsafe` (exit code 4). No half rest or 1920-tick rest candidate is emitted, entered into `build_ir`, or serialized to output. Obsolete half-rest suppression is not required.

---

## 2. Runtime Provenance

- **Product Commit**: `a9b127c311617dced5422e97e46a7bab840f7981` (clean working tree)
- **Ancestor Verification**: Confirmed ancestor `ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f` present in HEAD history
- **Executable Path**: `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/score2gp`
- **Import Path**: `/home/tticom-automation/work/score2gp-workspace/score2gp/src/score2gp`
- **Private Input**: `fixtures/private/Lesson-5.pdf` (SHA-256 verified)
- **Command Executed**: `score2gp convert --pdf Lesson-5.pdf --out work/lesson5.gp --work-dir work/lesson5_work --pdf-only-tab --editable-draft --json-report work/lesson5_work/convert-report.json`
- **Execution Status**: `status: refused`, `exit_code: 4`, `refusal_code: pdf_only_tab_grouping_unsafe`, `stage: layout-gating`.

---

## 3. Evidence & Comparative Analysis

| Dimension | Historical Ledger | Current `origin/main` Observation |
| :--- | :--- | :--- |
| **Pipeline Stage Reached** | `build_ir` / MusicXML bridge | `layout-gating` (Fail-Closed) |
| **Half Rest Emission** | 1920-tick half rest emitted | 0 half rests emitted |
| **Refusal Code** | Unrefused / unhandled overfull | `pdf_only_tab_grouping_unsafe` |
| **Exit Status** | Success / unhandled artifact | Exit Code 4 |
| **Output State** | Flawed GP package emitted | Output refused (`output_written: false`) |

---

## 4. Decision Gate Rationale & Next Steps

1. **`DEFECT_NOT_REPRODUCED`**: The false 1920-tick half rest defect does not manifest in current product `origin/main`. The conversion pipeline fails closed prior to `build_ir` due to `pdf_only_tab_grouping_unsafe`.
2. **No Code Mutation**: No product code changes are authorized or required for obsolete defect suppression.
3. **Queue Advancement**: Task `CR-04A` is complete. The project advances to candidate tasks in `APPROVED_TASK_QUEUE.md` for PDF candidate grouping refinement when authorized.
