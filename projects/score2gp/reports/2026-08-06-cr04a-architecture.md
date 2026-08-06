# CR-04A Architecture Report: False-Rest Rejection and Per-Voice Measure-Capacity Gate

**Date**: 2026-08-06  
**Task**: CR-04A: False-Rest and Per-Voice Capacity Architecture  
**Repository**: `tticom/score2gp` / `tticom/score2gp-agentops`  
**Authorised Identity**: `tticom-automation`  
**Role**: Architect  

---

## 1. Executive Summary & Objective

Task `CR-04A` investigates and defines a deterministic per-voice measure-capacity gate and false-rest rejection rule. In complex born-digital score conversions (such as Lesson 5), extra rest candidates can be incorrectly inferred or emitted due to unvalidated voice cursors or unchecked measure capacity.

This report establishes:
1. The exact trace of rest candidate extraction and timeline duration accumulation.
2. The deterministic per-voice measure capacity calculation formula.
3. The precise failure outcomes: `underfull`, `exact`, and `overfull`.
4. The refusal code (`musicxml_measure_overfull`, `musicxml_rest_voice_overlap`, `musicxml_voice_duration_overfull`) and stage emitting it (`ScoreIR` construction in `src/score2gp/build_ir.py`).
5. A Developer-ready prompt packet (`0008-cr04b-false-rest-capacity-developer.md`) for implementation in `CR-04B`.

---

## 2. Evidence & Call-Chain Analysis

### 2.1 Rest Candidate Origin & Timeline Construction
- **Rest Recognition**: Rests originate either from explicit MusicXML `<rest/>` elements or candidate flags extracted from PDF vector geometry (`quarter_rest_recogniser.py`, `pdf_candidate_whole_half_rest.py`).
- **Voice Cursor Tracking**: Each note or rest element advances the voice cursor by `duration_divisions`.
- **Backup & Forward Elements**: `<backup>` rewinds the voice cursor by `duration_divisions`; `<forward>` advances the cursor without emitting a note.
- **Chord Stack Treatment**: Notes belonging to a chord stack (`chord=True`) share the same onset as the anchor note and do not advance the voice cursor.

### 2.2 Capacity Divergence Location
The extra rest candidate in Lesson 5 first appears when candidate rests are inserted into a voice timeline without checking if the voice has already satisfied the expected measure duration. When a voice's accumulated duration exceeds `expected_duration_divisions`, an overfull condition occurs, creating timing ambiguity and overlapping events.

---

## 3. Deterministic Per-Voice Capacity Rule Packet

### 3.1 Expected Measure Duration Formula
The expected measure capacity in divisions for a measure with time signature $N/D$ and attribute `divisions` $S$ is:
$$\text{Expected Divisions} = \frac{N \times 4 \times S}{D}$$
For standard $4/4$ meter with $S = 4$, $\text{Expected Divisions} = \frac{4 \times 4 \times 4}{4} = 16\text{ divisions}$.

### 3.2 Voice Duration Accumulation
For a given voice $V$ in measure $M$:
- Each non-chord note or rest event $E_i$ advances the cursor from $T_{\text{cursor}}$ to $T_{\text{cursor}} + D(E_i)$.
- `<backup>` decreases $T_{\text{cursor}}$ by $D_{\text{backup}}$.
- `<forward>` increases $T_{\text{cursor}}$ by $D_{\text{forward}}$.
- Accumulated Voice Duration: $\text{VoiceDuration}(V) = \max_{E_i} (\text{Onset}(E_i) + D(E_i))$.

### 3.3 Outcome Classification
1. **Exact ($\text{VoiceDuration}(V) == \text{Expected Divisions}$)**:
   - Voice capacity is valid and fully specified.
2. **Underfull ($\text{VoiceDuration}(V) < \text{Expected Divisions}$)**:
   - Voice capacity is incomplete. Triggers `musicxml_voice_duration_underfull` warning/refusal in strict mode.
3. **Overfull ($\text{VoiceDuration}(V) > \text{Expected Divisions}$)**:
   - Voice capacity is exceeded. Triggers refusal `musicxml_voice_duration_overfull` / `musicxml_measure_overfull`.

---

## 4. Refusal & Fail-Closed Constraints

1. **Refusal Code**: `musicxml_measure_overfull` / `musicxml_rest_voice_overlap`.
2. **Emitting Stage**: `ScoreIR` construction (`src/score2gp/build_ir.py`) and timing verification (`src/score2gp/report.py`).
3. **No-Mutation Principle**:
   - The parser must **never** silently trim, rescale, or delete overfull notes or rests.
   - It must fail closed and report the refusal code when strict mode is enabled.
4. **No Special-Casing**:
   - The capacity check must apply generically to all voices and measures without filename rules, measure index filters, or fixed coordinate thresholds.

---

## 5. Implementation Injection Point & Allowed Files

- **Single Injection Point**: `src/score2gp/build_ir.py` during `ScoreIR` measure and voice timeline validation.
- **Allowed Product Files**:
  - `src/score2gp/build_ir.py`
  - `src/score2gp/report.py`
  - `tests/test_cli_convert.py`

---

## 6. Verification & Test Plan

### 6.1 Public Tests
- **Positive Test**: Standard measure with matching voice duration passes without warnings.
- **Negative Test**: Overfull measure (extra rest candidate) correctly emits `musicxml_measure_overfull` refusal.
- **Adversarial Test**: Backup/forward cursor movement causing voice overlap triggers `musicxml_rest_voice_overlap`.

### 6.2 Verification Commands
- Focused: `PYTHONPATH=. pytest tests/test_cli_convert.py`
- Governance: `python3 scripts/score2gp_governance_audit.py`

---

## 7. Decision & Next Step

**Decision**: **CONTINUE to Developer Phase (CR-04B)**.
All 5 continuation criteria pass:
1. Single injection point identified (`src/score2gp/build_ir.py`).
2. Deterministic capacity formula defined.
3. Generic refusal rule specified (`musicxml_measure_overfull`).
4. Measurable public regression tests designed.
5. Narrow product file allowlist established.
