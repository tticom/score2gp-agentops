# Run Record: MusicXML Polyphony Gate Diagnostics

Durable record of research, instrumentation, and analysis for the polyphony timing blocker in the melodic soloing guitar score.

## Metadata
- **Run ID**: `2026-05-31-musicxml-polyphony-gate-diagnostics`
- **Product Repository**: `tticom/score2gp`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Branch**: `research/musicxml-polyphony-gate-diagnostics-v0.1`
- **Agentops Branch**: `agent/pdf-to-gp-smoke-v1/tpo`

---

## 1. Gate Location and Trigger Conditions

We located the timing preflight gate in:
- **Source File**: [build_ir.py](file:///\\wsl.localhost\Ubuntu-24.04\home\tticom\work\score2gp-workspace\score2gp\src\score2gp\build_ir.py)
- **Function**: `build_ir_with_diagnostics_from_imports`
- **Line Range**: 1330–1364

### Gate Condition
The gate evaluates issues returned by `timing_issues = analyze_musicxml_timing(musicxml)`. If any fatal timing errors (`severity == "error"`) are present, it evaluates their codes. If all fatal errors belong to polyphony/multi-voice limits:
- `musicxml_polyphony_not_supported`
- `musicxml_multivoice_timing_not_supported`
- `musicxml_cross_voice_timing_unsupported`
- `musicxml_valid_multivoice_unsupported`
- `musicxml_voice_cursor_alignment_risk`
- `musicxml_alignment_not_attempted_due_to_timing_risk`
- `musicxml_many_timing_risks`

It raises a `BuildIrInputRiskError` with the category:
```text
musicxml_scoreir_polyphony_gate_refused
```
This is a blocking gate that halts all downstream ScoreIR and Guitar Pro package serialization in default execution modes (when `allow_remediation=False`).

---

## 2. Failure Classification

For the private melodic guitar soloing score, the blocker is classified as:
```text
over_conservative_duplicate_staff_tab_voice
```

### Rationale
MusicXML files exported from dual-staff editors (e.g., GPX or XML containing a standard staff and a TAB staff representing the exact same performance) typically map each staff to separate voices (e.g., Staff 1 to Voice 1, Staff 2 to Voice 5). 
Because the importer parses both staves as independent tracks/voices, it detects massive cross-voice timeline overlaps inside every measure. When `allow_remediation=False`, these overlaps are treated as unsupported polyphony errors, triggering the gate. In reality, these are musically duplicate representations rather than safe overlapping polyphonic parts.

---

## 3. Private-Safe Telemetry & E2E Smoke Metrics

Our E2E smoke tests successfully processed the private melodic soloing score with the following metrics:
- **Input Label**: `private_input_custom_melodic_soloing`
- **MusicXML Measure Count**: `8`
- **Voices Detected Across Part**: `2` (Voice 1 and Voice 5)
- **Playable Fret Candidates Extracted**: `59`
- **Technique-Text Candidates Extracted**: `51`
- **E2E Smoke Status**:
  - **With Remediation (`allow_remediation=True`, `allow_skip_unboxed=True`)**:
    - **Timing Status**: `passed` (errors demoted to warnings under remediation)
    - **ScoreIR Written**: `True`
    - **GP Written**: `True` (written to `work/private_e2e_smoke_v0_1/private_input_custom_melodic_soloing/smoke.gp`)
    - **Fret Alignment**: Matched `0` candidates because PDF staff grouping had warnings and layout checks were skipped under `allow_skip_unboxed=True`.
  - **Without Remediation (`allow_remediation=False`)**:
    - **Stage**: `musicxml-import`
    - **Refusal Code**: `musicxml_scoreir_polyphony_gate_refused`

---

## 4. Synthetic Public Tests Added

To maintain full repository correctness and back our findings, we implemented three robust synthetic tests under:
- [test_musicxml_polyphony_diagnostics_edge_cases.py](file:///\\wsl.localhost\Ubuntu-24.04\home\tticom\work\score2gp-workspace\score2gp\tests\test_musicxml_polyphony_diagnostics_edge_cases.py)

1. **`test_suspected_duplicate_staff_tab_diagnostics`**:
   Verifies that the new diagnostic `musicxml_polyphony_gate_duplicate_staff_tab_suspected` is correctly triggered when a measure contains two voices with identical note onsets, durations, and exactly a 12-semitone midi pitch offset.
2. **`test_suspected_valid_chord_diagnostics`**:
   Ensures that simultaneous note attacks representing valid chords in the same voice and onset are NOT treated as cross-voice overlap risks.
3. **`test_slur_tie_continuation_diagnostics`**:
   Verifies that tie and slur notations are correctly classified as suspected tie/slur continuations rather than overlapping timing risks.

We also added `test_musicxml_polyphony_diagnostics` to `tests/test_musicxml.py` to confirm backwards compatibility when `include_polyphony_diagnostics=False`.

---

## 5. Recommended Next Branch and Acceptance Criteria

### Proposed Branch Name
`feature/musicxml-duplicate-staff-tab-dedup-v0.1`

### Acceptance Criteria
1. **Deduplication Pass**:
   - Implement a post-processing step in the MusicXML importer to identify suspected duplicate staff/TAB representation (`musicxml_polyphony_gate_duplicate_staff_tab_suspected`).
   - Merge the overlapping staves/voices by prioritizing TAB fret coordinates and standard notation duration/pitch information.
2. **Safe Polyphony Resolution**:
   - Flatten duplicate voices into a single unified voice/track structure for the guitar part.
   - Ensure the score cleanly passes `build_ir_with_diagnostics_from_files` without needing `allow_remediation=True` or triggering `musicxml_scoreir_polyphony_gate_refused`.
3. **Fret Snapping and Layout Alignment**:
   - Ensure that the `Melodic Soloing Masterclass` score achieves 100% matched fret candidates by combining deduplicated voice timelines with our previous large-spaced TAB staff detector.
