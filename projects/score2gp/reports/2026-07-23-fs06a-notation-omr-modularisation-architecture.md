# FS-06A Notation OMR Modularisation Architecture

## Executive Summary & Claim Ledger
FS-06A defines a compatibility-first refactor architecture to modularise the overloaded `src/score2gp/whole_note_recogniser.py` module (1,942 lines) into a cohesive `score2gp.notation_omr` package.

`whole_note_recogniser.py` currently combines multiple distinct domain responsibilities:
- Candidate evidence shaping;
- Staff line geometry, system bounding box association, and ledger line detection;
- Treble clef detection (logical and raster treble clef evidence);
- Notehead candidate shaping and outcome mapping (whole, half, quarter, multi-note clusters);
- Beam and flag duration evidence extraction and duration candidate composition;
- Staff-position-to-pitch mapping and clef-resolved pitch calculation;
- Staff timeline preview generation and measure alignment;
- Overall OMR pipeline orchestration (`run_recognition_on_file`).

This architecture defines a zero-risk, multi-PR migration sequence. A backwards-compatible shim in `whole_note_recogniser.py` re-exports all legacy public symbols, ensuring zero breaking changes to existing CLI routes (`score2gp inspect-pdf`, `extract-tab`, `whole-note-recognition`, `note-candidate-recognition`, `convert`) or the test suite. No product code is modified in this architecture task.

---

## Import & Caller Map (`whole_note_recogniser.py`)

### Product CLI Callers (`src/score2gp/cli.py`)
- `cli.py` (L121, L158, L195, L228, L287): Imports `run_recognition_on_file` for notation recognition, note candidate inspection, and single-note export CLI routes.

### Test Suite Callers
1. `tests/test_cli_notation_whole_note_export.py` (L12, L229): `run_recognition_on_file`
2. `tests/test_deterministic_multinote_sequencing.py` (L3): `run_recognition_on_file`
3. `tests/test_deterministic_multinote_sequencing_quarter_rest.py` (L3): `run_recognition_on_file`
4. `tests/test_quarter_rest_e2e_acceptance.py` (L3): `run_recognition_on_file`
5. `tests/test_quarter_rest_recogniser_extraction.py` (L4): `run_recognition_on_file`
6. `tests/test_whole_note_intermediate_representation.py` (L3): `run_recognition_on_file`, `map_whole_note_candidates_to_intermediate_notes`
7. `tests/test_whole_note_recogniser_fractional_beam_extraction.py` (L3): `run_recognition_on_file`
8. `tests/test_whole_note_recognition_outcome.py` (L2, L42): `map_whole_note_candidates_to_read_only_outcomes`, `map_half_note_candidates_to_read_only_outcomes`
9. `tests/test_whole_note_staff_association.py` (L3): `run_recognition_on_file`, `_associate_staves`
10. `tests/test_logical_clef_bridge.py` (L2, L43, L306): `extract_treble_clef_candidate_evidence`, `build_clef_resolved_pitch_coverage_report`
11. `tests/test_logical_clef_coverage_proof.py` (L2, L259): `map_clef_resolved_staff_pitch`
12. `tests/test_raster_treble_clef_bridge.py` (L2, L12): `extract_treble_clef_candidate_evidence`
13. `tests/test_rhythm_timeline_diagnostics.py` (L2): `build_staff_timeline_preview`
14. `tests/test_single_note_export_cli_rejection.py` (L29): patches `src.score2gp.whole_note_recogniser.run_recognition_on_file`
15. `tests/test_note_candidate_recognition_report.py` (L309, L339, L382, L531, L574, L674, L727, L873, L1004): `_associate_staves`, `compose_filled_duration_candidates`, `map_staff_position_to_read_only_outcomes`, `map_ledger_lines_to_note_candidates`, `map_assumed_treble_pitch_to_read_only_outcomes`, `map_clef_resolved_staff_pitch`, `extract_treble_clef_candidate_evidence`, `map_treble_clef_candidates_to_read_only_outcomes`, `build_clef_resolved_pitch_coverage_report`

---

## Target Package Structure (`score2gp.notation_omr`)

The proposed package layout partitions existing functions into single-purpose submodules under `src/score2gp/notation_omr/`:

```text
src/score2gp/
├── notation_omr/
│   ├── __init__.py                # Package exports
│   ├── evidence.py                # Shared candidate-evidence shaping
│   ├── staff_geometry.py          # Staff bounds, system clustering, ledger lines
│   ├── clef.py                    # Treble clef detection and clef-resolved coverage
│   ├── notehead.py                # Whole, half, quarter, and cluster notehead candidates
│   ├── duration.py                # Beams, flags, and duration composition
│   ├── pitch.py                   # Staff position to MIDI pitch mapping
│   ├── timeline.py                # Timeline preview generation & measure alignment
│   └── pipeline.py                # Orchestrator (run_recognition_on_file facade)
└── whole_note_recogniser.py      # Backwards-compatibility shim re-exporting all symbols
```

---

## Exact Function Ownership Mapping (Committed Symbols)

| Committed Symbol (`whole_note_recogniser.py`) | Source Line Range | Target Submodule (`score2gp.notation_omr`) | Purpose |
|---|---|---|---|
| `shape_candidate_evidence` | L3-L45 | `evidence.py` | Generic candidate location dictionary shaper |
| `extract_treble_clef_candidate_evidence` | L46-L200 | `clef.py` | Treble clef evidence extraction |
| `shape_whole_note_candidate_evidence` | L201-L207 | `notehead.py` | Whole note candidate shaping |
| `shape_half_note_candidate_evidence` | L208-L214 | `notehead.py` | Half note candidate shaping |
| `shape_quarter_note_candidate_evidence` | L215-L221 | `notehead.py` | Quarter note candidate shaping |
| `shape_x_aligned_cluster_candidate_evidence` | L222-L251 | `notehead.py` | X-aligned notehead cluster shaping |
| `shape_left_margin_candidate_evidence` | L252-L285 | `notehead.py` | Left margin candidate shaping |
| `shape_ledger_line_candidate_evidence` | L286-L330 | `staff_geometry.py` | Ledger line candidate shaping |
| `map_treble_clef_candidates_to_read_only_outcomes` | L331-L376 | `clef.py` | Treble clef outcome mapping |
| `map_whole_note_candidates_to_read_only_outcomes` | L377-L405 | `notehead.py` | Whole note outcome mapping |
| `map_whole_note_candidates_to_intermediate_notes` | L406-L470 | `notehead.py` | Whole note intermediate representation |
| `map_half_note_candidates_to_read_only_outcomes` | L471-L489 | `notehead.py` | Half note outcome mapping |
| `map_quarter_note_candidates_to_read_only_outcomes` | L490-L509 | `notehead.py` | Quarter note outcome mapping |
| `map_x_aligned_cluster_candidates_to_read_only_outcomes` | L510-L526 | `notehead.py` | Cluster outcome mapping |
| `map_left_margin_candidates_to_read_only_outcomes` | L527-L546 | `notehead.py` | Left margin candidate outcome mapping |
| `map_ledger_line_candidates_to_read_only_outcomes` | L547-L560 | `staff_geometry.py` | Ledger line outcome mapping |
| `shape_flag_candidate_evidence` | L561-L593 | `duration.py` | Flag evidence shaping |
| `shape_beam_candidate_evidence` | L594-L626 | `duration.py` | Beam evidence shaping |
| `map_flag_candidates_to_read_only_outcomes` | L627-L643 | `duration.py` | Flag outcome mapping |
| `map_beam_candidates_to_read_only_outcomes` | L644-L660 | `duration.py` | Beam outcome mapping |
| `map_staff_geometry_to_read_only_report` | L661-L683 | `staff_geometry.py` | Staff line geometry report generation |
| `_associate_staves` | L684-L758 | `staff_geometry.py` | System staff bounding box association |
| `compose_filled_duration_candidates` | L759-L885 | `duration.py` | Filled notehead duration composition |
| `map_staff_position_to_read_only_outcomes` | L886-L973 | `pitch.py` | Staff position line/space to pitch |
| `map_assumed_treble_pitch_to_read_only_outcomes` | L974-L982 | `pitch.py` | Default treble pitch mapping |
| `map_clef_resolved_staff_pitch` | L983-L1179 | `pitch.py` | Clef-resolved staff position to pitch |
| `build_staff_timeline_preview` | L1180-L1473 | `timeline.py` | Staff timeline preview construction |
| `build_clef_resolved_pitch_coverage_report` | L1474-L1622 | `clef.py` | Clef-resolved pitch coverage diagnostics |
| `map_ledger_lines_to_note_candidates` | L1623-L1695 | `staff_geometry.py` | Ledger line to note candidate attachment |
| `run_recognition_on_file` | L1696-L1942 | `pipeline.py` | Top-level OMR pipeline facade |

---

## Migration Sequence (Ordered PRs)

### PR 1 (FS-06B): Shared Evidence and Staff Geometry Extraction
- **Scope**: Create `score2gp.notation_omr` with `evidence.py` and `staff_geometry.py`. Move the shared candidate-evidence shaper to `evidence.py` and five staff-geometry functions to `staff_geometry.py`; re-export each through the `whole_note_recogniser.py` shim.
- **Allowed Files**: `src/score2gp/notation_omr/__init__.py`, `src/score2gp/notation_omr/evidence.py`, `src/score2gp/notation_omr/staff_geometry.py`, `src/score2gp/whole_note_recogniser.py`, `tests/test_notation_omr_staff_geometry.py`.
- **Test Command**: `pytest tests/test_whole_note_staff_association.py tests/test_note_candidate_recognition_report.py tests/test_notation_omr_staff_geometry.py`.

### PR 2 (FS-06C): Clef & Pitch Module Extraction
- **Scope**: Extract `clef.py` and `pitch.py` under `score2gp.notation_omr`.
- **Changes**: Move treble clef detection (`extract_treble_clef_candidate_evidence`, `map_treble_clef_candidates_to_read_only_outcomes`, `build_clef_resolved_pitch_coverage_report`) and pitch mapping (`map_staff_position_to_read_only_outcomes`, `map_assumed_treble_pitch_to_read_only_outcomes`, `map_clef_resolved_staff_pitch`). Re-export through shim.
- **Allowed Files**: `src/score2gp/notation_omr/clef.py`, `src/score2gp/notation_omr/pitch.py`, `src/score2gp/whole_note_recogniser.py`, `tests/test_logical_clef_bridge.py`, `tests/test_logical_clef_coverage_proof.py`, `tests/test_raster_treble_clef_bridge.py`.
- **Test Command**: `pytest tests/test_logical_clef_bridge.py tests/test_logical_clef_coverage_proof.py tests/test_raster_treble_clef_bridge.py`.

### PR 3 (FS-06D): Notehead & Duration Module Extraction
- **Scope**: Extract `notehead.py` and `duration.py` under `score2gp.notation_omr`.
- **Changes**: Move notehead shaping/mapping (`shape_whole_note_candidate_evidence`, `shape_half_note_candidate_evidence`, `shape_quarter_note_candidate_evidence`, `shape_x_aligned_cluster_candidate_evidence`, `shape_left_margin_candidate_evidence`, `map_whole_note_candidates_to_read_only_outcomes`, `map_whole_note_candidates_to_intermediate_notes`, `map_half_note_candidates_to_read_only_outcomes`, `map_quarter_note_candidates_to_read_only_outcomes`, `map_x_aligned_cluster_candidates_to_read_only_outcomes`, `map_left_margin_candidates_to_read_only_outcomes`) and duration functions (`shape_flag_candidate_evidence`, `shape_beam_candidate_evidence`, `map_flag_candidates_to_read_only_outcomes`, `map_beam_candidates_to_read_only_outcomes`, `compose_filled_duration_candidates`). Re-export through shim.
- **Allowed Files**: `src/score2gp/notation_omr/notehead.py`, `src/score2gp/notation_omr/duration.py`, `src/score2gp/whole_note_recogniser.py`, `tests/test_whole_note_recognition_outcome.py`, `tests/test_whole_note_intermediate_representation.py`, `tests/test_whole_note_recogniser_fractional_beam_extraction.py`.
- **Test Command**: `pytest tests/test_whole_note_recognition_outcome.py tests/test_whole_note_intermediate_representation.py tests/test_whole_note_recogniser_fractional_beam_extraction.py`.

### PR 4 (FS-06E): Timeline & Pipeline Facade Extraction
- **Scope**: Extract `timeline.py` and `pipeline.py` under `score2gp.notation_omr`.
- **Changes**: Move timeline preview builder (`build_staff_timeline_preview`) and `run_recognition_on_file` pipeline facade. Complete `whole_note_recogniser.py` shim transition.
- **Allowed Files**: `src/score2gp/notation_omr/timeline.py`, `src/score2gp/notation_omr/pipeline.py`, `src/score2gp/whole_note_recogniser.py`, `tests/test_rhythm_timeline_diagnostics.py`, `tests/test_deterministic_multinote_sequencing.py`, `tests/test_cli_notation_whole_note_export.py`.
- **Test Command**: `pytest` (full test suite execution).

---

## First Implementation Task (FS-06B) - Rebuilt from 30 Committed Symbols

The smallest, highest-confidence first implementation step is **FS-06B: Shared Evidence and Staff Geometry Extraction**:

1. **Target Package**: `src/score2gp/notation_omr/`
2. **New Modules**: `src/score2gp/notation_omr/evidence.py` and `src/score2gp/notation_omr/staff_geometry.py`
3. **Exact Committed Symbols Moved**:
   - `shape_candidate_evidence` (L3-L45) to `evidence.py`.
   - `shape_ledger_line_candidate_evidence` (L286-L330), `map_ledger_line_candidates_to_read_only_outcomes` (L547-L560), `map_staff_geometry_to_read_only_report` (L661-L683), `_associate_staves` (L684-L758), and `map_ledger_lines_to_note_candidates` (L1623-L1695) to `staff_geometry.py`.
4. **Shim Modification**: `src/score2gp/whole_note_recogniser.py` imports and re-exports `shape_candidate_evidence` from `score2gp.notation_omr.evidence` and the five staff-geometry symbols from `score2gp.notation_omr.staff_geometry`.
5. **New Unit Test**: `tests/test_notation_omr_staff_geometry.py` directly tests the `evidence.py` import and representative staff-geometry functions.
6. **Allowed Files**:
   - `[NEW] src/score2gp/notation_omr/__init__.py`
   - `[NEW] src/score2gp/notation_omr/evidence.py`
   - `[NEW] src/score2gp/notation_omr/staff_geometry.py`
   - `[MODIFY] src/score2gp/whole_note_recogniser.py`
   - `[NEW] tests/test_notation_omr_staff_geometry.py`
7. **Test Command**:
   `pytest tests/test_whole_note_staff_association.py tests/test_note_candidate_recognition_report.py tests/test_notation_omr_staff_geometry.py`
8. **Acceptance Criteria**:
   - `shape_candidate_evidence` resides in `src/score2gp/notation_omr/evidence.py`; the five staff-geometry functions reside in `src/score2gp/notation_omr/staff_geometry.py`.
   - `whole_note_recogniser.py` re-exports them without changing signature, behavior, or dictionary structures.
   - All tests pass 100% with 0 regressions.

---

## Pre-Submit Challenge
1. **Did product code change in this architecture task?** No. Product worktree is clean.
2. **Are file and symbol names verified against active committed code?** Yes. All 30 functions in `whole_note_recogniser.py` and 15 calling test files were mapped with exact line numbers from committed `origin/main`. No speculative dataclasses or uncommitted model classes are introduced.
3. **Was the report generated natively in WSL without shell-quoted multiline strings?** Yes. Written directly via native file writing without passing Markdown through a shell-quoted Python string.
4. **Is the ASCII control-character scan clean?** Yes. 0 control characters detected.
