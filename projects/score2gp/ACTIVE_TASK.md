# Active Task

**Task**: CR-04B: False-Rest Rejection and Per-Voice Measure-Capacity Gate
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr04b-false-rest-capacity-gate`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0040-cr04b-false-rest-capacity-developer.md`

## Context

Task `M2: Fix Event Timing and Duration Semantics` has been completed and merged. We now promote `CR-04B` to implement the per-voice measure-capacity gate and false-rest rejection rules as defined in the `CR-04A` architecture report.

## Goal

Implement the capacity gate check to refuse overfull measures or rest voice overlap scenarios in strict mode, without silently mutating (trimming or deleting) note or rest event durations.

## Allowed Files

- `src/score2gp/build_ir.py`
- `src/score2gp/report.py`
- `tests/test_cli_convert.py`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- Do not implement any key signature, meter, layout, double/final barlines, page breaks, or legato/pull-off/slides/vibrato (embellishment) changes.

## Acceptance

Successfully implement the capacity gate, verify all tests pass, and publish one product pull request on branch `agy/cr04b-false-rest-capacity-gate` in `tticom/score2gp` for independent Codex review.
