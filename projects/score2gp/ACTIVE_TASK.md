# Active Task

**Task**: MXS-00: Build Candidate-Neutral Sidecar Evaluation Harness
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/mxs00-candidate-neutral-sidecar-evaluator`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0028-mxs00-build-candidate-neutral-sidecar-evaluator.md`

## Context

PR #430 (`codex/musicxml-sidecar-alternatives-research-plan`) merged the MusicXML Sidecar Generation Alternatives Research Plan (`projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`), authorizing Developer task `MXS-00` to establish a common candidate-neutral sidecar evaluation harness before candidate bake-offs.

## Goal

Add a public-fixture-only evaluator that accepts a candidate MusicXML/MXL file and writes ignored structured evaluation results for the common contract. Reuse existing MusicXML parser, timing analyser, OMR manifest concepts, and explicit conversion report capabilities. Classify `empty_musicxml`, `timing_invalid`, `handoff_refused`, and `non_deterministic` separately.

## Allowed Files

- `src/score2gp/sidecar_evaluator.py`
- `src/score2gp/musicxml.py`
- `src/score2gp/report.py`
- `tests/test_mxs00_sidecar_evaluator.py`

## Non-goals

- No changes to product conversion logic or `build_ir.py` in `MXS-00`.
- No new third-party tools or external OMR dependencies in `MXS-00`.
- No upload or processing of private fixtures.

## Acceptance

Pass validation suite (`pytest tests/test_mxs00_sidecar_evaluator.py` and `python scripts/agent_verify.py`). Assert known-good `generated_tiny_tab.musicxml` passes non-empty and handoff controls, synthetic empty-but-valid sidecar fails as `empty_musicxml`, parseable timing-invalid sidecar fails as `timing_invalid`, and candidate artifacts/reports remain ignored. Publish one Developer pull request on branch `agy/mxs00-candidate-neutral-sidecar-evaluator` in `tticom/score2gp` for independent Codex review.
