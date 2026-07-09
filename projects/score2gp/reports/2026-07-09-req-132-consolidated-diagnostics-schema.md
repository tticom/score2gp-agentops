# Req-132 Consolidated Diagnostics Schema and CLI Reporting Format

This document defines the schema, validation rules, display formats, and compatibility expectations for consolidating all OMR semantic, pitch, and timeline diagnostics.

## 1. Schema Versioning & Backwards Compatibility

- **Schema Version**: `1.0.0`
- **Compatibility Rules**:
  - **Adding fields**: Allowed. Downstream parsers must ignore unrecognized keys.
  - **Removing/renaming fields**: Disallowed. Any modification to existing fields requires a major version bump.
  - **Validation Constraints**: All dictionary structures must validate against Pydantic definitions. Missing or malformed coordinate bboxes or parameters must fail closed gracefully rather than causing runtime exceptions.

---

## 2. JSON Schema Definition

The consolidated diagnostics JSON output structure consists of:

```json
{
  "source": "filename.pdf",
  "recognition_mode": "read_only_diagnostic_derived",
  "staff_geometry": [
    {
      "page_index": 1,
      "system_index": 1,
      "staff_index": 1,
      "bbox": [50.0, 200.0, 500.0, 240.0],
      "line_y_coords": [200.0, 210.0, 220.0, 230.0, 240.0]
    }
  ],
  "read_only_recognition_outcomes": [
    {
      "symbol_type": "quarter_note_candidate",
      "candidate_id": "quarter_note_candidate_001",
      "page_index": 1,
      "system_index": 1,
      "staff_index": 1,
      "bbox": [100.0, 205.0, 110.0, 215.0],
      "clef_resolved_staff_pitch": "E4",
      "clef_resolved_midi_pitch": 64,
      "timeline_start_tick": 0,
      "timeline_duration_ticks": 960
    }
  ],
  "clef_resolved_pitch_coverage": {
    "total_note_candidates_in_scope": 1,
    "note_candidates_with_staff_position_index": 1,
    "note_candidates_on_staves_with_valid_clef": 1,
    "note_candidates_on_staves_with_assumed_clef": 0,
    "note_candidates_with_clef_resolved_staff_pitch": 1,
    "note_candidates_with_assumed_treble_clef_pitch": 0,
    "assumed_clef_mode": false,
    "in_staff_mapped_notes": 1,
    "out_of_staff_mapped_notes": 0,
    "skipped_missing_required_ledger_support": 0,
    "skipped_clef_missing": 0,
    "skipped_clef_ambiguous": 0,
    "skipped_staff_association_malformed": 0,
    "skipped_staff_position_malformed": 0,
    "sample_diagnostics": []
  },
  "semantic_candidates": [
    {
      "page_index": 1,
      "system_index": 1,
      "staff_index": 1,
      "logical_clef": {
        "status": "logical_clef_candidate",
        "reason": "Treble clef curve patterns detected",
        "clef_kind": "treble"
      },
      "quarter_rests": [],
      "whole_rests": [],
      "half_rests": []
    }
  ],
  "timeline_preview": [
    {
      "page_index": 1,
      "system_index": 1,
      "staff_index": 1,
      "measures": [
        {
          "measure_index": 1,
          "valid": true,
          "voice_1_final_tick": 3840,
          "voice_2_final_tick": 3840,
          "events": [
            {
              "candidate_id": "quarter_note_candidate_001",
              "symbol_type": "quarter_note_candidate",
              "voice": 1,
              "start_tick": 0,
              "duration_ticks": 960,
              "resolved_pitch": "E4"
            },
            {
              "candidate_id": null,
              "symbol_type": "padding_rest",
              "voice": 1,
              "start_tick": 960,
              "duration_ticks": 2880,
              "resolved_pitch": null
            },
            {
              "candidate_id": null,
              "symbol_type": "padding_rest",
              "voice": 2,
              "start_tick": 0,
              "duration_ticks": 3840,
              "resolved_pitch": null
            }
          ]
        }
      ]
    }
  ]
}
```

---

## 3. CLI Display & Table Format

When running the diagnostics CLI command with human-readable mode (default, non-JSON option), the CLI will output a clean, formatted report:

```text
================================================================================
OMR CONSOLIDATED DIAGNOSTICS REPORT
================================================================================
Source File: filename.pdf
Recognition Mode: read_only_diagnostic_derived

--------------------------------------------------------------------------------
STAFF INDEX SUMMARY: Page 1 | System 1 | Staff 1
--------------------------------------------------------------------------------
Clef: Treble (Detected)
Key Signature: C Major

Note / Rest Candidates:
- Quarter Notes: 1
- Half Notes: 0
- Whole Notes: 0
- Quarter Rests: 0
- Half Rests: 0
- Whole Rests: 0

Diatonic Pitch Coverage:
- Total Note Candidates: 1
- Successfully Mapped: 1 (100.0%)
- Skipped/Failed: 0 (0.0%)

Timeline Preview:
Measure 1 [VALID]
  Voice 1 (Upper): |--(E4, 960)--|--[Padding Rest, 2880]--|
  Voice 2 (Lower): |--[Padding Rest, 3840]--|
```

---

## 4. No-ScoreIR Leakage & Safety Boundaries

- **Separation**: All JSON schemas, validation Pydantic classes, and printer formatters are strictly kept within read-only diagnostic packages.
- **Conversion Safety**: Downstream compilation, ScoreIR build steps, and playable package exports (`write_gp` and `.gp` output) remain completely decoupled and continue to build from standard noteheads without processing `timeline_preview` metadata.
