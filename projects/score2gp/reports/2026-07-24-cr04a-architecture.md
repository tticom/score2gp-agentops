# CR-04A Architecture Report: False-Rest Candidate and Per-Voice Capacity Gate

**Authorised Role**: Architect  
**Governance Repository**: `score2gp-agentops`  
**Product Repository**: `score2gp`  
**Product Base**: `ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`  
**Date**: 2026-07-24  

---

## 1. Executive Summary & Objective

The objective of **CR-04A** is to analyze the root cause of false-rest candidate creation (evidenced in benchmark scores like `Lesson-5.pdf`) and establish a deterministic per-voice measure capacity gate. 

Prior to CR-04A, false rest candidates (such as orphan flag primitives converted into `quarter_rest_candidate` objects) or unscaled note sequences could cause a voice's total measure duration to exceed expected meter capacity ($D_{\text{voice}} > C_{\text{measure}}$). The OMR pipeline lacked a formal capacity validation gate, allowing overfull voice timelines to pass silently down the pipeline into IR, GPIF, and MusicXML serialization.

This report establishes:
1. The exact extraction and timeline propagation path of false rest candidates;
2. A deterministic per-voice measure capacity calculation model;
3. The exact refusal code (`omr_voice_capacity_overfull`) and fail-closed gate injection point in `score2gp.notation_omr.timeline`;
4. A narrow product file allowlist and public regression test plan for Developer implementation in CR-04B.

---

## 2. Evidence Analysis & Cause Tracing

### 2.1 False-Rest Extraction Tracing
False rest candidates originate in two OMR extraction stages:
1. **`quarter_rest_recogniser.py`**: Promotes orphan `flag_candidate` primitives (flag vector graphics not attached to note stems) into `quarter_rest_candidate` objects. If vector noise or isolated staff marks resemble flag fragments, they are converted into false quarter rest candidates.
2. **`pdf_candidate_quarter_rest.py`**: Extracts `QuarterRestCandidate` objects from vector bounding boxes and z-shaped curve primitives near staff center.

### 2.2 Timeline Propagation & Overfull Divergence
When a false rest candidate is added to `outcomes`:
- `pipeline.py` passes all `read_only_recognition_outcomes` to `build_staff_timeline_preview()` in `notation_omr/timeline.py`.
- `timeline.py` calculates total duration per voice per measure by summing `duration_ticks` for all note and rest candidates in that voice.
- For a standard 4/4 measure, expected measure capacity $C_{\text{measure}} = 3840$ ticks.
- If a voice contains valid notes totaling 3840 ticks PLUS a false quarter rest (960 ticks), total per-voice duration becomes $D_{\text{voice}} = 4800$ ticks ($4800 > 3840$).
- Previously, `timeline.py` constructed the overfull timeline preview without verifying $D_{\text{voice}} \le C_{\text{measure}}$, resulting in downstream MusicXML measure overflow or invalid time signature score heuristics.

---

## 3. Deterministic Per-Voice Capacity Model

### 3.1 Expected Measure Capacity ($C_{\text{measure}}$)
Given a measure with time signature $P/Q$ (beats/beat-type):
$$C_{\text{measure}} = P \times \frac{3840}{Q} \text{ ticks}$$
- For 4/4 meter: $C_{\text{measure}} = 4 \times 960 = 3840$ ticks.
- For 3/4 meter: $C_{\text{measure}} = 3 \times 960 = 2880$ ticks.
- For 6/8 meter: $C_{\text{measure}} = 6 \times 480 = 2880$ ticks.
- For 2/4 meter: $C_{\text{measure}} = 2 \times 960 = 1920$ ticks.

### 3.2 Event Duration Grain & Voice Ownership
- **Voice Assignment**: Events are assigned to independent voices (Voice 1, Voice 2) per measure and staff.
- **Time-Advancing Events**:
  - Note candidates (`whole_note`, `half_note`, `quarter_note`, `eighth_note`, `sixteenth_note`, `thirty_second_note`, and candidate variants): advance cursor by `duration_ticks` (e.g. quarter = 960, eighth = 480, tuplet eighth = 320).
  - Rest candidates (`whole_rest`, `half_rest`, `quarter_rest`, `eighth_rest`, and candidate variants): advance cursor by `duration_ticks` (e.g. quarter rest = 960).
- **Zero-Advance Events** (Duration = 0 ticks):
  - Clef candidates and clef assignments.
  - Key and time signature markers.
  - Barline candidates and barlines.
  - Secondary chord member noteheads (only 1 notehead per chord event advances the cursor; additional chord members sharing the same start tick have 0 advance).
  - Grace notes (`grace_note`).
  - Tuplet markers (`TupletMarkerEvidence`).

### 3.3 Capacity Outcome Classifications
For each measure $m$ and voice $v$ containing at least 1 note or rest event:
1. **Exact**: $D_{\text{voice}, v} == C_{\text{measure}}$. Voice duration matches measure capacity perfectly.
2. **Underfull**: $D_{\text{voice}, v} < C_{\text{measure}}$. Voice duration is less than measure capacity (eligible for padding rest calculation up to $C_{\text{measure}}$).
3. **Overfull**: $D_{\text{voice}, v} > C_{\text{measure}}$. Voice duration exceeds measure capacity! Indicates extra false rest or unscaled note candidate.

---

## 4. Refusal Gate & Suppression Rules

### 4.1 Refusal Gate Specification
- **Injection Point**: `src/score2gp/notation_omr/timeline.py` (`build_staff_timeline_preview()`).
- **Refusal Code**: `omr_voice_capacity_overfull`
- **Condition**: If $D_{\text{voice}, v} > C_{\text{measure}}$ for any voice $v$ in any measure $m$.
- **Action**: Emit a structured refusal diagnostic in `timeline_preview` / pipeline result. Fail closed without mutating event durations, silently deleting notes, or emitting invalid overfull MusicXML measures.

### 4.2 False-Rest Suppression Rule
- **Injection Point**: `src/score2gp/quarter_rest_recogniser.py` (`extract_quarter_rest_candidates()`).
- **Condition**: Suppress an orphan flag candidate from being promoted to `quarter_rest_candidate` if adding its duration (960 ticks) to the containing measure voice would cause $D_{\text{voice}} + 960 > C_{\text{measure}}$.

### 4.3 Fail-Closed Governance Constraints
- **No Coordinate Hardcoding**: Rules must apply generically based on ticks and meter; no hardcoded PDF coordinates or bounding boxes.
- **No Fixture-Specific Logic**: No filenames, fixture names, or hardcoded measure indices.
- **No Silent Deletion / Cross-Voice Balancing**: Overfull voices must refuse via `omr_voice_capacity_overfull` rather than silently dropping notes or balancing across independent voices.

---

## 5. Developer Implementation Allowlist & Verification Plan

### 5.1 Product File Allowlist
Implementation is strictly bounded to the following product files:
1. `[MODIFY] src/score2gp/notation_omr/timeline.py`
2. `[MODIFY] src/score2gp/quarter_rest_recogniser.py`
3. `[NEW] tests/test_notation_omr_voice_capacity.py`

### 5.2 Required Tests
- **Positive Test**: Exact-capacity measure ($D = C$) produces clean timeline preview with `status="exact"`.
- **Underfull Test**: Underfull measure ($D < C$) produces timeline preview with `status="underfull"` and padding rests up to $C_{\text{measure}}$.
- **Overfull Refusal Test**: Overfull measure ($D > C$) emits `omr_voice_capacity_overfull` diagnostic refusal.
- **False-Rest Suppression Test**: Orphan flag primitive that would cause measure overflow is suppressed from becoming a `quarter_rest_candidate`.
- **Chord Member Zero-Advance Test**: Multi-notehead chords count duration only once toward voice capacity.

### 5.3 Verification Commands
```bash
.venv/bin/python -m pytest -v tests/test_notation_omr_voice_capacity.py
.venv/bin/python -m pytest
.venv/bin/python -m score2gp.cli export-schema --out schemas
.venv/bin/python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
.venv/bin/python scripts/artifact_audit.py
git diff --check origin/main...HEAD
git diff --exit-code -- schemas
git ls-files fixtures/private work
git status --short
```

---

## 6. Architect Recommendation & Next Action

All continue criteria pass. Proceed to create versioned Developer prompt `projects/score2gp/prompts/next/0008-cr04b-voice-capacity-gate-implementation.md` and update `ACTIVE_TASK.md` and `prompts/NEXT.md`.
