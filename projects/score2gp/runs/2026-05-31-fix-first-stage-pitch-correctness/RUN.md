# Diagnose and Fix First Stage Pitch Correctness Defect

## Session Summary

- **Product Branch:** `research/domain-knowledge-stage-tests-v1`
- **AgentOps Branch:** `agent/pdf-to-gp-smoke-v1/tpo`
- **Task Overview:** Trace the unrealistic pitch defect to the earliest possible stage, implement a safe fix, and verify it under the automated test suite.

---

## 1. Problem & Context

1. **Unrealistic Stave Display Pitch:** In the generated `smoke.gp` files, guitar notes (e.g. sounding G2, MIDI 43) were being drawn on the stave one full octave lower than written standard treble clef notation (drawing as written G2 instead of written G3).
2. **Analysis Spine:** Systematically traced visual/auditory pitch through all 5 actual pipeline stages (`inspect-pdf` -> `extract-tab` -> `align-ascii-musicxml` -> `build-ir` -> `write-gp`).

---

## 2. Earliest Defective Stage Diagnosis

### Target Stage
- **Defective Stage:** **Stage 5: `write-gp`** (Guitar Pro Relational XML compilation in `gpif.py`)

### Evidence & Findings
1. **Upstream Correctness:**
   - Visual fret/string evidence correctly extracted G2 sounding (MIDI 43) at `inspect-pdf` and `extract-tab`.
   - MusicXML alignment correctly aligned the standard treble written G3 (MIDI 55) and tablature sounding G2 (MIDI 43) under a 12-semitone transposition correction strategy in `build-ir`, resulting in correct MIDI 43 in the final `score.ir.json`.
2. **Upstream Verification Command:**
   - Running `inspect_pitches_clean.py` proved that `score.ir.json` correctly stored the sounding pitch 43 at bar 0 onset 0:
     `Voice 5 at onset 0: ['string=6, fret=3, pitch=43']`
3. **The Defect Root Cause:**
   - In `gpif.py` lines 835-847, octaves were calculated using `octave = note.pitch // 12 - 1` (yielding octave 2).
   - `ConcertPitch` Octave was set to 2 and `TransposedPitch` Octave was set to `octave + 1 = 3`.
   - Under Guitar Pro's flat relational GPIF schema, octaves are calculated based on division of standard MIDI numbering (`midi // 12`). Sounding G2 (MIDI 43) expects a ConcertPitch octave of `3` and TransposedPitch octave of `4` to represent transposing written G3.
   - Because it was written one octave too low, Guitar Pro displayed the treble clef note a full octave lower (written G2, which sounds as an impossible G1), violating the treble clef transposing stave display invariant.

---

## 3. Implementation & Safe Fix

1. **The Corrective Fix:**
   - Corrected `gpif.py`'s octave formulas to use `octave = note.pitch // 12` for transposing guitar tracks, mapping G2 sounding (MIDI 43) to ConcertPitch Octave 3 and TransposedPitch Octave 4.
2. **Regression Verification:**
   - Added `test_gpif_standard_guitar_pitch_stave_display` in `tests/test_gp_writer.py` and `test_relational_gpif_clef_transposition_invariants` in `tests/integration/domain_contracts/test_intermediate_products.py` to assert correct octave mappings.
   - All 404 tests pass successfully.
