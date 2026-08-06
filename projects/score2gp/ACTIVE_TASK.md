# Active Task

**Task**: MXS-00: Candidate-Neutral Sidecar Evaluation Harness
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/mxs00-candidate-neutral-sidecar-evaluation-harness-v2`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0028-mxs00-candidate-neutral-sidecar-evaluation-harness.md`

## Context

Task `CR-05A` (PDF-Tab Barline Style Classification Seam) completed and merged via product PR #410 (`149919a8b4ffdcab156e519e0f0b1cfb0cbef306`). The project now promotes task `MXS-00` from `APPROVED_TASK_QUEUE.md` under the MusicXML Sidecar Ingestion Series to add a candidate-neutral evaluator module and CLI command for MusicXML/MXL sidecars.

## Goal

Add `sidecar_evaluator.py` and CLI `eval-sidecar` command in `score2gp` to evaluate MusicXML sidecars against the common sidecar contract, classifying `empty_musicxml`, `timing_invalid`, `handoff_refused`, and `non_deterministic` statuses cleanly.

## Allowed Files

- `src/score2gp/sidecar_evaluator.py`
- `src/score2gp/cli.py`
- `tests/test_mxs00_sidecar_evaluation_harness.py`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- No change to product `convert` default execution or core conversion pipeline.
- No third-party network API calls or private input file access.
- No model training or external OMR dependencies in this task.

## Acceptance

Implement `evaluate_sidecar()`, add `score2gp eval-sidecar` subcommand, pass `test_mxs00_sidecar_evaluation_harness.py` and `scripts/agent_verify.py`, update `ACTIVE_TASK.md`, and publish one product pull request on branch `agy/mxs00-candidate-neutral-sidecar-evaluation-harness-v2` in `tticom/score2gp` for independent Codex review.
