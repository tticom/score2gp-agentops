# 0028 - MXS-00 Candidate-Neutral Sidecar Evaluation Harness

## Objective

Implement Developer slice `MXS-00` on the MusicXML sidecar evaluation pipeline in `tticom/score2gp`, as authorized by the merged research plan `projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`.

Add a public-fixture-only evaluator module and CLI command in `score2gp` that accepts candidate MusicXML/MXL files and evaluates them against the common sidecar contract. The evaluator must classify `empty_musicxml`, `timing_invalid`, `handoff_refused`, and `non_deterministic` separately without altering core conversion logic or leaking report artifacts.

## Authorized Product Files

- `src/score2gp/sidecar_evaluator.py`
- `src/score2gp/cli.py`
- `tests/test_mxs00_sidecar_evaluation_harness.py`

No other product files in `src/` or `tests/` may be edited in this task.

## Start Protocol

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/next/0028-mxs00-candidate-neutral-sidecar-evaluation-harness.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/mxs00-candidate-neutral-sidecar-evaluation-harness` in `tticom/score2gp`.
6. Run `.venv/bin/python scripts/agent_verify.py` in `score2gp` before making code modifications.

## Implementation Scope & Contract

1. **`src/score2gp/sidecar_evaluator.py`**:
   - Define data models and classification functions for sidecar evaluation:
     - `SidecarEvaluationResult`: dataclass/Pydantic model containing `status` (`Literal["passed", "empty_musicxml", "timing_invalid", "handoff_refused", "non_deterministic"]`), `note_count: int`, `rest_count: int`, `pitch_count: int`, `measure_count: int`, `score_ir_event_count: int`, `matched_tab_candidate_count: int`, `refusal_reason: str | None`, and `provenance: dict`.
   - Implement `evaluate_sidecar(xml_path: Path, pdf_fixture_path: Path | None = None) -> SidecarEvaluationResult`:
     1. **Xml/MXL Parsing Check**: Extract & parse MusicXML/MXL. If missing/unparseable, set `status = "handoff_refused"`.
     2. **Zero Note/Rest Check**: Count all `<note>`, `<pitch>`, and `<rest>` elements. If `note_count == 0` and `rest_count == 0`, set `status = "empty_musicxml"`, `refusal_reason = "zero_notes_and_rests"`.
     3. **Timing Validation**: Run internal measure timing checks. If measure durations/divisions fail balance or produce negative/invalid durations, set `status = "timing_invalid"`, `refusal_reason = "measure_timing_error"`.
     4. **Conversion Handoff Check**: Test dry-run handoff into ScoreIR event builder and TAB candidate matcher. If handoff raises exceptions or generates zero ScoreIR events on non-empty input, set `status = "handoff_refused"`.
     5. **Determinism Check**: Re-evaluate to verify byte/result equality across runs.

2. **`src/score2gp/cli.py`**:
   - Register `eval-sidecar` subcommand accepting `--sidecar <path>` and optional `--pdf <path>` or `--json`, invoking `evaluate_sidecar` and printing structured output.

3. **`tests/test_mxs00_sidecar_evaluation_harness.py`**:
   - Add unit test suite asserting:
     - `test_mxs00_known_good_sidecar_passes`: Asserting `generated_tiny_tab.musicxml` passes with `status = "passed"`.
     - `test_mxs00_empty_musicxml_classified`: Asserting a valid XML file with parts/measures but 0 notes/rests is classified as `empty_musicxml`.
     - `test_mxs00_timing_invalid_classified`: Asserting a sidecar with invalid measure timing is classified as `timing_invalid`.
     - `test_mxs00_cli_eval_sidecar`: Asserting CLI `score2gp eval-sidecar` output.

## Validation Commands

1. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_mxs00_sidecar_evaluation_harness.py`
2. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python scripts/agent_verify.py`

## Non-goals

- No change to product `convert` default execution or core conversion pipeline.
- No third-party network API calls or private input file access.
- No model training or external OMR dependencies in this task.
