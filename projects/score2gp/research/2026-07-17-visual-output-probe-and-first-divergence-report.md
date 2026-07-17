# Visual Output Probe and First-Divergence Report (CR-02)

## 1. VO-01 Fixture Identification

Through analysis of the supplied visual observations and corpus characteristics, the exact approved input represented by **VO-01** has been identified:
- **Fixture File**: [Lesson-5.pdf](file:///home/tticom/work/score2gp-workspace/score2gp-private-fixtures/fixtures/private/Lesson-5.pdf)
- **Source Facts**: Expected tempo is **70 BPM**, time signature is **4/4** with triplet groupings (printed `3` tuplet markers above arpeggiated eighth notes), printed title "Close Position Diatonic Arpeggios", and structural double barlines.
- **Generated Defects**: The generated output retains the tempo of 70, but emits a **12/8** meter, followed by ghost rests (half rest in measure 1), wrong sequential grouping, and missing section names/double barlines.

---

## 2. First-Divergence Analysis

### Stage of First Divergence
The divergence first occurs during the **Timeline Reconstruction** stage inside [whole_note_recogniser.py](file:///home/tticom/work/score2gp-workspace/score2gp-recovery/src/score2gp/whole_note_recogniser.py) at the function `detect_time_signature`.

### Causal Path and Code Walkthrough
1. **Text-based bypass skipped**:
   - `detect_time_signature` first attempts regex extraction of standard signatures (`4/4`, `6/8`, `12/8`) from the first three pages of the PDF.
   - For `Lesson-5.pdf`, no literal time signature string (like `4/4`) is present in the extracted text stream. The bypass returns `None`.
2. **Tuplet neglect in duration heuristics**:
   - The OMR duration heuristics fall back to summing note candidate lengths per measure.
   - Each detected notehead candidate is mapped to a default tick duration (e.g. `eighth_note_candidate` $\rightarrow$ 480 ticks).
   - Because OMR does not recognize the printed `3` tuplet bracket in this early stage, each triplet eighth note is assigned the full 480 ticks instead of the scaled 320 ticks ($480 \times \frac{2}{3}$).
3. **Measure length inflation**:
   - A single 4/4 measure containing four triplet eighth-note beats (12 notes) yields a computed length of $12 \times 480 = 5760$ ticks.
4. **Meter score selection and overfull penalty**:
   - In `detect_time_signature` (lines 1601–1635), the computed length of 5760 matches a 12/8 meter ($12 \times 480 = 5760$ ticks) with 0 difference.
   - Since $5760 > 3840 + 240$ (the 4/4 overfull limit of 4080 ticks), the 4/4 score gets penalized by `-100.0 * count`.
   - As a result, the time signature heuristic selects `12/8` as the best meter.
5. **Downstream defects**:
   - The reconstructed timeline is serialized into MusicXML with `<beats>12</beats><beat-type>8</beat-type>`.
   - The subsequent `score2gp` orchestration matches the inflated 5760-tick timeline, inserting a ghost half rest to fill the remaining space of each measure and misaligning notes.

---

## 3. Evidence Ledger Summary

The complete sanitized ledger is recorded in [2026-07-17-first-divergence-evidence-ledger.json](file:///home/tticom/work/score2gp-workspace/score2gp-agentops/projects/score2gp/research/2026-07-17-first-divergence-evidence-ledger.json).

| Fixture | Stage | Expected Meter | Actual Meter | Expected Tempo | Actual Tempo | First Divergence Stage / Description |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Lesson-5.pdf** (VO-01) | `Timeline Reconstruction` | 4/4 | 12/8 | 70 | 70 | **detect_time_signature**: Inflated duration estimation of triplet groupings selects 12/8 due to tuplet neglect and 4/4 overfull penalty. |
| **Lesson-3.pdf** (Distinct check) | `No Divergence` | 4/4 | 4/4 | 120 | 120 | **None**: Correctly resolved because the staves contain standard eighth-note groups of 8 per measure, matching 3840 ticks exactly. |

---

## 4. Next Task Promotion: CR-03

Based on the evidence, the first divergence is the lack of robust, tuplet-aware or common-time aware meter resolution.

### Proposed Task: CR-03: Repair Generic Meter Evidence and Emission
- **Generic Meter Rule**:
  1. Add support for common time text symbols (like `C` or `Common Time` markers) in standard margin parsing.
  2. Implement a tuplet-aware duration scaler: if standard notation text contains `3` candidates vertically aligned with note groups of three, scale their duration tick assignment by $\frac{2}{3}$ prior to summing the measure length.
  3. If duration evidence is ambiguous or conflicts with text metadata, fail closed with a descriptive warning or allow explicit CLI time signature overrides.
- **Verification Plan**:
  - **Public Structured Test**: Add a test in `tests/test_timing_mapping.py` verifying that measures containing 12 notes under tuplet markings are correctly evaluated as 4/4.
  - **Acceptance Facts**: `Lesson-5.pdf` converts successfully as 4/4 with no ghost rests.
  - **Pivot Condition**: If triplet scaling fails due to layout noise, default to text-based common-time layout heuristics first.
