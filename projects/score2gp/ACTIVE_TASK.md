# Active Task

**Task**: M3: Integrate and Test OMR Sidecar Generator
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/m3-integrate-and-test-sidecar-generator`
**Pull Request**: `NO_PR_OPEN`
**Original Prompt**: `projects/score2gp/prompts/next/0040-m3-integrate-and-test-sidecar-generator.md`

## Context

Task `M2: Fix Event Timing and Duration Semantics` completed and merged via product PR #415. The project now promotes task `0040` to integrate and test the newly implemented OMR sidecar generator.

## Goal

Integrate and test the newly implemented OMR-to-MusicXML sidecar generator in the `score2gp` pipeline. Ensure the `generate-sidecar` CLI command is covered by robust integration tests, produces valid MusicXML files (not malformed or misclassified MXL archives), and timing/refusal metrics are traceably validated.

## Allowed Files

- `src/score2gp/cli.py`
- `src/score2gp/notation_omr/pipeline.py`
- `src/score2gp/notation_omr/musicxml_generator.py`
- `tests/test_musicxml_generator.py`
- `tests/test_omr_pipeline.py`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- Do not implement any key signature, meter, layout, double/final barlines, page breaks, or legato/pull-off/slides/vibrato (embellishment) changes.

## Acceptance

Successfully integrate and test the OMR sidecar generator, verify all tests pass locally and on CI, update `ACTIVE_TASK.md`, and publish one product pull request on branch `agy/m3-integrate-and-test-sidecar-generator` in `tticom/score2gp` for independent Codex review.
