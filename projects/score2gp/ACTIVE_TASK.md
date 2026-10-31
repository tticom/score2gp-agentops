# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: CP-18 — Launchers clean up after themselves: remove merged author worktrees, review checkouts and pytest temp directories

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/cp-18-launchers-clean-up-after-themselves`

**Pull Request**: 909

**Owner Role**: implementation

## Objective

Measured by governance on 2026-09-29 at product main 2e8c00b (worktree at d7eef3f) on this Windows host. worktrees/codex holds about 60 entries: 3 merged author worktrees (3-5 GB each, mostly gitignored work/), about 30 review checkouts (up to 231 MB each) and about 12 empty pytest temp directories; worktrees/gov holds 6 review checkouts of about 217 MB each. Remove review checkouts when the review publishes, author worktrees after merge (keeping any requested deliverables), and temp directories on exit; preserve dirty or locked worktrees and record a receipt, as the workspace-cleanup skill does.

## Allowed paths

- `scripts/*.py`
- `tests/test_cp_18_*.py`

## Validation commands

- `python -m pytest`
- `PYTHONUTF8=1 python scripts/score2gp_governance_audit.py`
- `git diff --check`
