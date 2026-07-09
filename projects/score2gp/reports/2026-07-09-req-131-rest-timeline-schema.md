# Req-131 Rest Mapping and Rhythm Timeline Reconstruction Schema

This document defines the schema, data structures, voice cursor rules, polyphonic alignments, and fail-closed behaviors for reconstructing a rhythm timeline from note and rest candidates.

## 1. Timeline Duration Units

To support precise fractional rhythms, all durations are represented in integer **ticks**, with a standard Time Division (PPQ) of **960 ticks per quarter note**.

| Musical Note/Rest | Duration (fraction) | Duration (ticks) |
| :--- | :---: | :---: |
| **Double Whole (Breve)** | $2/1$ | 7680 |
| **Whole Rest / Note** | $1/1$ | 3840 |
| **Half Rest / Note** | $1/2$ | 1920 |
| **Quarter Rest / Note** | $1/4$ | 960 |
| **Eighth Rest / Note** | $1/8$ | 480 |
| **Sixteenth Rest / Note** | $1/16$ | 240 |
| **Thirty-Second** | $1/32$ | 120 |
| **Sixty-Fourth** | $1/64$ | 60 |

---

## 2. Voice Cursors and Measure Positions

1. **Voice Allocation**:
   - The system supports up to 2 active voices per staff:
     - **Voice 1 (Upper Voice)**: Stems pointing upwards, melody.
     - **Voice 2 (Lower Voice)**: Stems pointing downwards, bass/accompaniment.
   - Note candidates are assigned to Voice 1 or Voice 2 based on their detected stem direction.
   - Rest candidates (which lack stems) are assigned based on vertical staff position:
     - Rests located on or above the middle staff line default to Voice 1.
     - Rests located below the middle staff line default to Voice 2.
     - A whole rest centered on the staff in an otherwise empty measure defaults to Voice 1.

2. **Voice Cursors**:
   - For each voice $V \in \{1, 2\}$, we maintain a `voice_cursor` representing the current tick offset from the beginning of the measure ($0 \le \text{cursor}_V \le \text{measure\_duration}$).
   - When a note or rest of duration $D$ is processed in voice $V$, the cursor advances:
     $$\text{cursor}_V \leftarrow \text{cursor}_V + D$$

---

## 3. Polyphonic Alignment and X-Clustering

Because scanned/printed scores contain horizontal spacing offsets, primitives must be clustered into vertical time slices (beats) using their $x$-coordinates.

### 3.1. Clustering Algorithm
- Let $X_{\text{tol}} = 1.5 \cdot \text{staff\_spacing}$.
- Candidates (notes and rests) on a staff are sorted by their horizontal center coordinate.
- Adjacent candidates whose horizontal centers differ by less than $X_{\text{tol}}$ are grouped into the same **Time Slice**.
- Each Time Slice represents a single point in time within the measure.

### 3.2. Grid Alignment Rules
- When a Time Slice is processed, all notes/rests within it start at the same tick offset:
  $$\text{start\_tick} = \max(\text{cursor}_1, \text{cursor}_2)$$
- The voice cursors for the active voices are updated to the start tick, the respective note/rest durations are added, and the cursors advance.

---

## 4. Barline and Reset Behavior

- **Reset**: When a barline candidate is encountered:
  - All voice cursors are reset to $0$.
  - The measure-local memory is cleared.
- **Validation**:
  - The expected measure duration $D_{\text{measure}}$ is determined by the time signature (e.g. 3840 ticks for 4/4).
  - If a voice cursor is less than $D_{\text{measure}}$, a warning is logged, and the remaining space is padded with a silent rest (fail-closed/auto-fill).
  - If any voice cursor exceeds $D_{\text{measure}}$, the measure is marked as invalid.

---

## 5. Explicit Separation: Diagnostic Preview vs. Core Code

To prevent leakage of diagnostic candidates into downstream output:
1. **Diagnostic Preview Output**:
   - The timeline reconstruction logic is implemented in a separate helper `build_staff_timeline_preview`.
   - The output is stored in the read-only diagnostics under the key `"timeline_preview"`.
2. **Core Output Boundary**:
   - The core `build_ir.py` and `notation_bridge.py` modules do not import or run `build_staff_timeline_preview`.
   - No `"timeline_preview"` metadata is written to the final `scoreir.json` or packed GP package.

---

## 6. Fail-Closed Behaviors

1. **Duration Conflict**: If the notes in a time slice conflict or exceed the time signature's maximum measure duration, the timeline generation for that measure is aborted, and a warning is written to the diagnostic output.
2. **Ambiguous Rests**: If a rest candidate cannot be assigned to a voice or staff with high confidence, it is ignored, and the voice cursor is padded during barline validation.
