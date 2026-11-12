# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: PERF-03 — Cut the longest source's conversion time further without changing any output

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/perf-03-longest-source-conversion-time`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

MEM-04 cut the 34-page source from about 1500 s to about 546 s (duration stage about 305 s) and left peak memory near 1.8 GB. The PERF-01 budget and report allowance are protected and are not touched. Leads, not facts: re-measure by stage on the current runtime, then reduce the slowest stage and peak memory.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
