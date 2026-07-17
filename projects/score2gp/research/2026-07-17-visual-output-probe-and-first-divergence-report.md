# Visual Output Probe and First-Divergence Report (CR-02 Amended)

## 1. VO-01 Fixture Identification

Through analysis of the supplied visual observations and corpus characteristics, the exact approved input represented by **VO-01** has been identified:
- **Fixture File**: [Lesson-5.pdf](file:///home/tticom/work/score2gp-workspace/score2gp-private-fixtures/fixtures/private/Lesson-5.pdf)
- **Source Facts**: Expected tempo is **70 BPM**, time signature is **4/4** with triplet groupings (printed `3` tuplet markers above arpeggiated eighth notes), printed title "Close Position Diatonic Arpeggios", and structural double barlines.
- **Generated Defects**: The generated output retains the tempo of 70, but emits a **12/8** meter, followed by a false half rest in measure 1, wrong sequential grouping, and missing section names/double barlines.

---

## 2. First-Divergence Analysis

### Stage of First Divergence
The divergence first occurs during the **Timeline Reconstruction** stage inside [whole_note_recogniser.py](file:///home/tticom/work/score2gp-workspace/score2gp-recovery/src/score2gp/whole_note_recogniser.py) at the function `detect_time_signature`.

### Causal Path and Code Walkthrough
1. **Text-based bypass skipped**:
   - `detect_time_signature` first attempts regex extraction of standard signatures (`4/4`, `6/8`, `12/8`) from the first three pages of the PDF.
   - For `Lesson-5.pdf`, no literal time signature string (like `4/4`) is present in the extracted text stream. The bypass returns `None`.
2. **Measured First-Measure Evidence**:
   For staff `(1, 1, 1)` (Page 1, System 1, Staff 1):
   - **Candidate Symbol Types**: 12 `eighth_note_candidate` notehead candidates.
   - **X-Order / Slices or Voices**: The 12 candidates are sorted by their X coordinates and split into 12 distinct time slices since consecutive X coordinate deltas ($\approx 9.59$ points) exceed the computed threshold (`X_tol = 6.378` points).
     - Slice 1: X=71.265, voice 1
     - Slice 2: X=80.856, voice 1
     - Slice 3: X=90.446, voice 1
     - Slice 4: X=100.036, voice 1
     - Slice 5: X=109.627, voice 1
     - Slice 6: X=119.217, voice 1
     - Slice 7: X=128.808, voice 1
     - Slice 8: X=138.398, voice 1
     - Slice 9: X=147.988, voice 1
     - Slice 10: X=157.579, voice 1
     - Slice 11: X=167.169, voice 1
     - Slice 12: X=176.759, voice 1
   - **Per-Voice Cursor Lengths**: `cursor_1` = 5760 ticks (12 notes $\times$ 480 ticks/note), `cursor_2` = 0 ticks.
   - **Meter Scores**:
     - `(4, 4)` Score: `-1587.0` (includes overfull penalties for measures $> 4080$ ticks)
     - `(6, 8)` Score: `-2284.0`
     - `(12, 8)` Score: `10.0`
     - Consequently, `(12, 8)` is selected during timeline reconstruction in `whole_note_recogniser.py`.
   - **Emitted MusicXML Note/Rest Durations**:
     - 8 notes of type `eighth` and duration `480` ticks each.
     - 1 rest of type `half` and duration `1920` ticks.

### Corrected Causal Narrative (Half Rest)
- **False Rest Candidate**: The half rest in measure 1 of `Lesson-5` is a separate false rest candidate extracted during the OMR phase, rather than padding time automatically inserted by the conversion stage to fill a 12/8 bar. It remains a separate **CR-04** concern.

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

### Tightened CR-03 Requirements
To resolve this divergence:
1. **Generic Meter Rule**:
   - Add support for common time text symbols (like `C` or `Common Time` markers) in standard margin parsing.
   - Implement a tuplet-aware duration scaler: represent tuplets as structured timing evidence (e.g. from OMR outcomes or explicit tuplet markings in metadata) rather than a proximity-based text "3" shortcut. Scale triplet durations by $\frac{2}{3}$ prior to summing the measure length.
   - If duration evidence is ambiguous or conflicts with text metadata, fail closed with a descriptive warning or allow explicit CLI time signature overrides.
2. **Verification Plan**:
   - **Public Structured Test**: Add public synthetic tests in `tests/test_timing_mapping.py` that explicitly distinguish 4/4 triplets, 6/8, and 12/8.
   - **Acceptance Facts**: `Lesson-5.pdf` converts successfully as 4/4.
   - **Pivot Condition**: If triplet scaling fails due to layout noise, default to text-based common-time layout heuristics first.
