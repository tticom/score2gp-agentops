# Teamwork Containment and Correction Gate Report: M3/M4 Claim Verification

This report details the execution and results of the mandatory correction gate and regression containment for the M3/M4 claims.

## 1. Commits and Containment Outcomes

The following commit has been created in the product repository `score2gp`:
- **Commit SHA**: [34b7c2e5](file:///home/tticom/work/score2gp-workspace/score2gp) (branch `feature/teamwork-corpus-conversion-accuracy-v0.1`)
- **Capabilities and Containment Controls Delivered**:
  - **Embellishment Containment**: Disabled automatic Legato/HO/PO/slide/vibrato/sustain emission by default. Only re-enable Hammer-On candidates passing strict page, system, voice, chronological adjacency, staff-distance, and pitch constraints.
  - **Key Signature Containment**: Missing key signature classifiers are treated as unknown (not defaulted to C Major), preventing fabricated accidentals. In MusicXML output, the `<key>` tag is omitted entirely for unknown keys.
  - **Evidence Logging & Trace Reports**:
    - `embellishment_candidates.json` records detailed candidate parameters, horizontal/vertical coordinates, and explicit rejection reasons (e.g. `slide_disabled_not_re_enabled`, `pitch_descending_is_pull_off_disabled`, etc.).
    - `layout_title_trace.json` documents the trace from OMR page/system/staff bounding boxes -> select first measure -> MusicXML print/rehearsal attributes -> ScoreIR layout/marker attributes -> actual GPIF `MasterBar/Bar` xml serialization.
  - **Section & Layout Parsing**: Handled both standard relational and classic GPIF formats to parse, compare, and serialize layout breaks (`layout_break`) and section markers (`marker` / `<Section><Name>`) in the roundtrip pipeline.

---

## 2. Before/After Mismatch Ledger for Lesson-3 and Lesson-4

### Lesson-3
- **Before Containment**: Contained filename-specific key signature overrides.
- **After Containment**:
  - **Matches**: **True** (100% exact semantic match).
  - **Mismatches**: **0**

### Lesson-4
- **Before Containment**: Emitted unwanted accidentals and unwanted legato/slide markings.
- **After Containment**:
  - **Matches**: **False**
  - **First Remaining Mismatch**: `tempo` mismatch (expected: 70 bpm, actual: 120 bpm).
  - **Details**: Pitch spelling, key signatures, rests, voice groupings, barlines, and system breaks are **100% correct**. Legacy unwanted accidentals, vibrato, and slide markings have been successfully contained.

---

## 3. Public Verification and Integration Tests

The following suite of public regression and trace-validation tests was added:
- `test_accidental_semantics` in [test_deterministic_musicxml.py](file:///home/tticom/work/score2gp-workspace/score2gp/tests/test_deterministic_musicxml.py): Verifies G Major signature alterations (F -> F#), natural cancellation (F natural), explicit accidentals (C -> C#), and unknown key fallback behavior.
- `test_layout_and_title_propagation` in [test_system_breaks.py](file:///home/tticom/work/score2gp-workspace/score2gp/tests/test_system_breaks.py): Verifies the end-to-end trace from system breaks/section markers to the final zipped GPIF package.
- `test_comparator_synthetic_mismatches` in [test_comparator.py](file:///home/tticom/work/score2gp-workspace/score2gp/tests/test_comparator.py): Verifies comparator detection of technique differences.

---

## 4. Operational Status & Baselines

- Conversions were run locally against the private corpus without reference leakage.
- Output artifacts generated at: `work/teamwork/run_containment/`
- Zero untracked or generated files remain in the source tree root.
