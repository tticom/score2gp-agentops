# Active Task

**Task**: M1: Bar-Level Comparator and Mismatch Ledger
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/m1-bar-level-comparator`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0038-m1-bar-level-comparator-and-mismatch-ledger.md`

## Context

Task `Remediate PyMuPDF Deprecation Warning Failures` completed and merged via product PR #413. The project now promotes task `0038` to implement the bar-level comparator under the `Teamwork Programme: Corpus Conversion Accuracy`.

## Goal

Implement the reusable bar-level comparator, add unit tests, and expose it via the CLI.

## Allowed Files

- `src/score2gp/compare.py`
- `src/score2gp/cli.py`
- `tests/test_bar_comparator.py`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- Do not implement any OMR, pitch inference, duration association, or GPIF writing changes in this task.
- Do not modify existing `compare_gp` logic in `gp_package.py`.
- Do not commit any private fixture data or generated private GP/MusicXML files.

## Acceptance

Successfully implement the bar-level comparator, verify all tests pass locally and on CI, update `ACTIVE_TASK.md`, and publish one product pull request on branch `agy/m1-bar-level-comparator` in `tticom/score2gp` for independent Codex review.
