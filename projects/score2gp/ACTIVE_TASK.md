# Active Task

**Task**: MXS-00: Candidate-Neutral Sidecar Evaluation Harness
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/mxs00-candidate-neutral-sidecar-evaluation-harness`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0028-mxs00-candidate-neutral-sidecar-evaluation-harness.md`

## Context

PR #398 (`agy/cr05a-pdf-tab-barline-style-classification`) on `tticom/score2gp` was merged into product `main`. The project has approved research plan `projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md` and requires Developer slice `MXS-00` to build a candidate-neutral MusicXML sidecar evaluation harness.

## Goal

Add a public-fixture-only evaluator module (`src/score2gp/sidecar_evaluator.py`) and CLI subcommand (`score2gp eval-sidecar`) in `tticom/score2gp` that accepts candidate MusicXML/MXL files and evaluates them against the common contract, classifying `empty_musicxml`, `timing_invalid`, `handoff_refused`, and `non_deterministic` separately.

## Allowed Files

- `src/score2gp/sidecar_evaluator.py`
- `src/score2gp/cli.py`
- `tests/test_mxs00_sidecar_evaluation_harness.py`

## Non-goals

- No change to product `convert` default execution or core conversion pipeline.
- No third-party network API calls or private input file access.
- No model training or external OMR dependencies in this task.

## Acceptance

Pass validation suite (`pytest tests/test_mxs00_sidecar_evaluation_harness.py` and `python scripts/agent_verify.py`). Assert exact classification behavior for known-good sidecar (`"passed"`), zero note/rest sidecar (`"empty_musicxml"`), invalid timing sidecar (`"timing_invalid"`), and handoff failures (`"handoff_refused"`). Publish one Developer pull request on branch `agy/mxs00-candidate-neutral-sidecar-evaluation-harness` in `tticom/score2gp` for independent Codex review.
