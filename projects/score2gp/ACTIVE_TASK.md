# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: CP-10 — Decode gh output as UTF-8 in the control plane

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/cp-10-decode-gh-output-as-utf-8`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

run_json, capture_live_state and the gh calls in score2gp_got_bootstrap.py read gh output with the locale codec and crash on UTF-8 review text on Windows (a false audit violation and a crashed merge executor were seen). Pass an explicit UTF-8 encoding to every gh subprocess, with a test that can fail.

## Allowed paths

- `scripts/*.py`
- `tests/test_cp_10_*.py`
- `tests/test_score2gp_orca_control.py`

## Validation commands

- `python -m pytest`
- `PYTHONUTF8=1 python scripts/score2gp_governance_audit.py`
- `git diff --check`
