# 0040 - M3: Integrate and Test OMR Sidecar Generator

## Objective

Integrate and test the newly implemented OMR-to-MusicXML sidecar generator in the `score2gp` pipeline. Ensure the `generate-sidecar` CLI command is covered by robust integration tests, produces valid MusicXML files (not malformed or misclassified MXL archives), and timing/refusal metrics are traceably validated.

## Authorized Product Files

### Source Files
- `src/score2gp/cli.py`
- `src/score2gp/notation_omr/pipeline.py`
- `src/score2gp/notation_omr/musicxml_generator.py`

### Test Files
- `tests/test_musicxml_generator.py`
- `tests/test_omr_pipeline.py`
- `projects/score2gp/ACTIVE_TASK.md`

No other product files in `src/` or `tests/` may be edited in this task.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/m3-integrate-and-test-sidecar-generator` in `tticom/score2gp`.
6. Run `python scripts/agent_verify.py` in `score2gp` before making code modifications.

## Implementation Scope & Seam Contract

1. **CLI and Extension Check**: Ensure `generate-sidecar` outputs plain text XML by default when the output has a `.musicxml` or `.xml` extension, and zipped MXL packages when the output has a `.mxl` extension. Prevent malformed plain-text XML files from being written with a `.mxl` extension (or vice versa).
2. **Timing & Refusal Verification**: Write integration tests that invoke the `generate-sidecar` command against public synthetic PDF fixtures (e.g. `generated_standard_staff_whole_note.pdf`) and check the validity and formatting of the output MusicXML.
3. **Integration Test Suite**: Ensure OMR pipeline and MusicXML generator are covered by automated unit/integration tests (`tests/test_musicxml_generator.py` and `tests/test_omr_pipeline.py`).
4. **General Corpus Gating**: Ensure that when a sidecar is generated and used in `convert`, standard layout/timing validation still runs properly and triggers correct refusal codes (e.g. `musicxml_timing_risk` or `partial_pdf_grouping`) rather than exiting with unhandled exceptions.

## Validation Commands

1. `.venv/bin/python -m pytest`
2. Run `generate-sidecar` on a public PDF fixture and verify the generated sidecar parses successfully as a valid MusicXML/MXL document.
3. Run `convert` using the newly generated sidecar on a public PDF fixture to confirm successful end-to-end event mapping.

## Non-goals

- Do not implement any key signature, meter, layout, double/final barlines, page breaks, or legato/pull-off/slides/vibrato (embellishment) changes.
