# CR-04A Architecture Report: False-Rest Candidate and Per-Voice Capacity (Observability Gap)

**Authorised Role**: Architect  
**Governance Repository**: `score2gp-agentops`  
**Product Repository**: `score2gp`  
**Product Base**: `ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`  
**Date**: 2026-07-24
**Verdict**: `OBSERVABILITY_GAP`


---

## 1. Executive Summary & Classification

CR-04A investigated the root cause of the `Lesson-5.pdf` false rest defect and the per-voice measure capacity gate.

Based on committed evidence in `projects/score2gp/research/2026-07-17-first-divergence-evidence-ledger.json`, this architecture pass is formally classified as **`OBSERVABILITY_GAP`**:

1. **Disproven Quarter-Rest Hypothesis**: The committed `Lesson-5.pdf` evidence ledger records a false **half rest** (1920 ticks), not a quarter rest (960 ticks). The previously proposed `quarter_rest_recogniser.py` orphan-flag promotion path handles only quarter rests and does not extract half rests. The primitive source and candidate ID of the false half rest are not yet observable from committed diagnostics.
2. **Timeline Preview Isolation**: `build_staff_timeline_preview()` in `notation_omr/timeline.py` is a read-only diagnostic for CLI reporting. Its validity flags do not feed into `ScoreIR`, `GPIF`, or `MusicXML` conversion. Adding a refusal string to `timeline_preview` alone does not cause strict conversion commands (`score2gp convert` / `build_ir`) to refuse overfull output safely.
3. **No Product Code Authorized**: Under governance boundaries, no product code changes or developer implementation prompts are authorized until candidate provenance, primitive source, and active conversion refusal points are instrumented and proven from committed evidence.

---

## 2. Disconfirmation & Evidence Traceability

### 2.1 Lesson-5.pdf Evidence Analysis
From `2026-07-17-first-divergence-evidence-ledger.json`:
- **Recorded Note/Rest Durations**: `[480, 480, 480, 480, 480, 480, 480, 480, 1920]` (8 eighth notes = 3840 ticks + 1 half rest = 1920 ticks). Total duration = 5760 ticks.
- **Defect Class**: False **Half Rest** (1920 ticks).
- **Disproven Extractor**: `quarter_rest_recogniser.py` extracts `quarter_rest_candidate` objects (960 ticks) from orphan flags. It does not extract `half_rest_candidate` (1920 ticks). The false half rest is created either by `pdf_candidate_whole_half_rest.py` / `_extract_half_note_candidates` or inserted during timeline/IR bridge voice alignment.

### 2.2 Conversion Pipeline vs Diagnostic Preview
- `build_staff_timeline_preview()` already contains `cursor_1 > 3840` invalidity checks for diagnostic display.
- However, `convert_read_only_outcomes_to_ir_events()` in `notation_bridge.py` and `build_ir.py` process `outcomes` directly without querying `timeline_preview`.
- Therefore, the true conversion refusal injection point for overfull measure capacity must be in the active conversion path (`score2gp.notation_bridge` / `score2gp.build_ir`), rather than the read-only OMR diagnostic preview.

---

## 3. Required Instrumentation & Observability Action Plan

To unblock Developer implementation in a future prompt, the following minimum instrumentation must be established in committed diagnostics:

1. **Candidate Provenance & Source Tracing**:
   - Instrument `pdf_candidate_whole_half_rest.py`, `_extract_half_note_candidates`, and `notation_bridge.py` to record candidate ID, primitive bounding box, symbol type (`half_rest_candidate`), and extraction source for every extracted half rest.
2. **Measure & Voice Ownership Logging**:
   - Trace candidate outcomes through `convert_read_only_outcomes_to_ir_events()` to record exact measure index, staff index, and voice assignment for every note and rest candidate.
3. **First Divergence Stage Identification**:
   - Log the exact conversion stage where the 1920-tick false half rest is first introduced into the measure event stream.
4. **Conversion Refusal Injection Point**:
   - Identify and validate the exact conversion refusal point in `score2gp.notation_bridge` or `score2gp.build_ir` where $D_{\text{voice}} > C_{\text{measure}}$ triggers an atomic pipeline refusal (exit code 2/3 for OMR/timing refusal).

---

## 4. Governed Next State

- **Status**: `OBSERVABILITY_GAP`
- **Developer Prompt**: None authorized for CR-04B. Product code changes remain strictly prohibited until observability instrumentation is committed and verified.
- **Governance Branch**: `agy/cr04a-false-rest-capacity-architecture`
- **Governance PR**: [#364](https://github.com/tticom/score2gp-agentops/pull/364)
