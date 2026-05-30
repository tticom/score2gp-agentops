# Goal Description - Relational GPIF Compilation for Guitar Pro Compatibility

When opening the generated `smoke.gp` files in Guitar Pro, they display as a blank page. Although they are well-formed XML zip packages, their size is significantly smaller than the original `.gp` files (~6 KB vs ~19 KB) because the current writer compiles the ScoreIR into a custom, nested **hierarchical XML format**, whereas official Guitar Pro applications (GP7/GP8) strictly require a **flat relational database XML schema**.

This plan outlines the transitioning of `score2gp`'s GPIF compiler and parser to use the official flat relational GPIF XML schema, ensuring that generated GP files display, play, and edit correctly inside standard Guitar Pro software.

---

## Technical Blocker Analysis

Through comparative analysis of the official `Lesson-3.gp` XML and our generated `smoke.gp` XML, we have identified the root cause of the blank page rendering:

### 1. Custom Hierarchical Format (Current Blocker)
The current `gpif.py` compiler wraps all structural elements under `<Score>` in a nested, object-oriented tree:
```xml
<GPIF version="7">
  <Score>
    <Tracks>
      <Track id="gtr-1">
        ...
    <Bars>
      <Bar index="1">
        <Event id="e1" track="gtr-1" voice="1" position="0" duration="1/8">
          <Note string="3" fret="0" pitch="56" />
```
Because the official Guitar Pro app does not expect this nested structure under `<Score>`, it parses 0 tracks, 0 bars, and 0 notes, rendering a completely **blank sheet**.

### 2. Official Flat Relational Format (Guitar Pro Native Schema)
The native GP7/GP8 format decouples notes, beats, voices, rhythms, and bars into **flat, normalized relational tables** placed directly under the root `<GPIF>` element, linked by unique ID attributes or space-separated ID reference arrays:

*   **`<Rhythms>`**: A list of unique `<Rhythm id="...">` values defining note values (e.g. `Quarter`, `Eighth`) and dots.
*   **`<Notes>`**: A list of unique `<Note id="...">` values capturing fret, string, concert pitch, and transposed pitch.
*   **`<Beats>`**: A list of unique `<Beat id="...">` values referencing their rhythm (`<Rhythm ref="[id]" />`) and note IDs (`<Notes>[note_ids]</Notes>`).
*   **`<Voices>`**: A list of unique `<Voice id="...">` values listing space-separated beat IDs (`<Beats>[beat_ids]</Beats>`).
*   **`<Bars>`**: A list of `<Bar id="...">` values mapping to exactly four voice IDs (`<Voices>[voice_ids]</Voices>`) representing the four voices of a measure (using `-1` for empty/unused voices).
*   **`<Tracks>`**: Flat list of `<Track id="...">` tracks with tuning and staves.

---

## User Review Required

> [!IMPORTANT]
> **Complete Relational Transformation**
> This change will entirely replace the internal XML structure written to `Content/score.gpif` inside generated GP packages. 
> To maintain regression parity, we must also update the parser `extract_score_ir_from_gp` under `gp_package.py` to correctly extract ScoreIR from this flat relational layout.

> [!WARNING]
> **Test Suite Refactoring**
> Many existing unit tests in `test_gp_writer.py`, `test_gpif_multi_voice.py`, etc., inspect specific nested XML tags (`.//Bars/Bar/Voices/Voice/Event`). These tests must be refactored to verify the new flat relational tag mappings and ID reference joins.

---

## Proposed Changes

### Component 1: GPIF XML Generation

We will refactor `gpif.py` to compile `ScoreIR` into a flat relational schema.

#### [MODIFY] [gpif.py](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/gpif.py)
*   **`build_gpif`**:
    *   Construct the root `<GPIF>` element with flat relational sub-elements: `<Rhythms>`, `<Notes>`, `<Beats>`, `<Voices>`, `<Bars>`, `<Tracks>`, `<MasterBars>`, `<Score>`.
    *   Collect all unique rhythmic durations in the score and populate the `<Rhythms>` database, assigning incremental ID references.
    *   Collect all unique playable notes and rests, write them into `<Notes>` with concert/transposed pitches, and assign unique IDs.
    *   Aggregate notes into `<Beats>`, referencing rhythm and note IDs.
    *   Group beats into `<Voices>` and map them under `<Bars>` using space-separated GP8/7 voice references.
    *   Output standard GP7/8-compliant XML.

---

### Component 2: GPIF XML Parsing & Recovery

We will refactor the GP package deserializer to read relational XML.

#### [MODIFY] [gp_package.py](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/gp_package.py)
*   **`_extract_score_ir_from_gpif_root`**:
    *   Parse the flat `<Rhythms>`, `<Notes>`, `<Beats>`, `<Voices>`, `<Bars>` databases.
    *   Resolve references: Join `<Bars>` $\to$ `<Voices>` $\to$ `<Beats>` $\to$ `<Notes>` $\to$ `<Rhythms>` to reconstruct hierarchical ScoreIR measures, events, durations, and notes.

---

### Component 3: Regression Verification

We will update the tests to align with the new schema.

#### [MODIFY] [test_gp_writer.py](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/tests/test_gp_writer.py) (and other GPIF-inspecting test files)
*   Update XML assertions to verify `<Rhythms>`, `<Notes>`, `<Beats>`, `<Voices>`, and `<Bars>` relational joins rather than nested hierarchical paths.

---

## Verification Plan

### Automated Tests
Run the entire regression suite to verify that relational roundtrip conversions achieve 100% parity:
```bash
python -m pytest
```

### Manual Verification
1.  Run the private smoke test pass:
    ```bash
    python scripts/private_e2e_smoke.py
    ```
2.  Open the newly generated `smoke.gp` files in Guitar Pro 7 or 8.
3.  Confirm that the score renders visual notes and tablature correctly on the page, instead of displaying a blank sheet.
