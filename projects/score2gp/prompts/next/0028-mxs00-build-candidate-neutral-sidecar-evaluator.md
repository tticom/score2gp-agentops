# 0028 - MXS-00 Candidate-Neutral Sidecar Evaluation Harness

## Objective

Implement Developer task `MXS-00` in `tticom/score2gp` to build a candidate-neutral evaluation harness for candidate MusicXML/MXL sidecars, as authorized by the MusicXML Sidecar Generation Alternatives Research Plan (`projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`).

Add a public-fixture-only evaluator that accepts a candidate MusicXML/MXL file and evaluates it against the common sidecar evaluation contract. The harness must reuse existing MusicXML parsing, timing analysis, OMR manifest concepts, and explicit conversion report capabilities, and must separately classify `empty_musicxml`, `timing_invalid`, `handoff_refused`, and `non_deterministic` failure modes.

## Authorized Product Files

- `src/score2gp/sidecar_evaluator.py`
- `src/score2gp/musicxml.py`
- `src/score2gp/report.py`
- `tests/test_mxs00_sidecar_evaluator.py`

No other product files in `src/` or `tests/` may be edited in this task. Do not modify core conversion semantics or `build_ir.py` in `MXS-00`.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/next/0028-mxs00-build-candidate-neutral-sidecar-evaluator.md`, `projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/mxs00-candidate-neutral-sidecar-evaluator` in `tticom/score2gp`.
6. Run `python scripts/agent_verify.py` in `score2gp` before making code modifications.

## Implementation Scope & Seam Contract

1. **`src/score2gp/sidecar_evaluator.py`**:
   - Create candidate-neutral sidecar evaluator `evaluate_musicxml_sidecar(xml_path: Path, fixture_pdf_path: Path | None = None) -> SidecarEvaluationResult`.
   - Record MusicXML/MXL package validity, root, part, measure, note, pitch, and rest counts.
   - Evaluate timing validity via existing timing analyser and classify `timing_invalid` if timing errors/imbalances are detected.
   - Test Score2GP handoff via `convert --musicxml` mechanisms without mutating product conversion state.
   - Classify failure modes separately: `empty_musicxml` (zero note/pitch/rest elements), `timing_invalid`, `handoff_refused`, and `non_deterministic`.
   - Ensure all output reports and candidate artifacts are written to ignored directories.

2. **`tests/test_mxs00_sidecar_evaluator.py`**:
   - Add comprehensive test suite asserting:
     - Known-good `generated_tiny_tab.musicxml` passes non-empty and handoff controls (`status = "viable"`).
     - Synthetic empty-but-structurally-valid sidecar fails closed with classification `empty_musicxml`.
     - Synthetic parseable timing-invalid sidecar fails closed with classification `timing_invalid`.
     - Synthetic invalid handoff sidecar fails closed with classification `handoff_refused`.
     - Generated reports remain in ignored output directories.

## Validation Commands

1. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_mxs00_sidecar_evaluator.py`
2. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python scripts/agent_verify.py`

## Non-goals

- Do not alter conversion semantics or core `build_ir.py` logic in `MXS-00`.
- Do not integrate external OMR tools or third-party dependencies in `MXS-00`.
- Do not upload or process private fixtures in `MXS-00`.
