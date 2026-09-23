# WIN-03 — Product Repository OS-Agnostic Tooling

- **Status**: PROPOSED (in `queued_task_proposals`). Not executable until governance promotes it.
- **Repository**: `tticom/score2gp`
- **Branch**: `feat/win-03-product-os-agnostic-tooling`
- **Owner Role**: `implementation`
- **Reviewer Role**: `reviewer`
- **Delivery Action**: `pull_request`
- **Prerequisites**: `WIN-01`

---

## 1. Authority

[Decision: OS-Agnostic Development Environment](../../decisions/2026-09-23-os-agnostic-development-environment.md)
(maintainer, 2026-09-23). This replaces the deferred product scope in §3.2 of
the 2026-09-22 decision.

## 2. Objectives

An inventory of product `main` on 2026-09-23 found only these OS assumptions
outside `src/`:

1. `scripts/corpus_harness.py:106-114`, `resolve_score2gp_cmd()`: looks only for `.venv/bin/score2gp`, and its comments call this "the native WSL CLI entrypoint". Resolve `.venv/Scripts/score2gp.exe` or `.venv/bin/score2gp`, then `PATH`. Remove the WSL wording.
2. `Makefile:1`: `PYTHON ?= $(shell [ -f .venv/bin/python3 ] ...)` uses POSIX shell and the Linux venv layout. Make it resolve on both layouts, or document the `python -m …` equivalent of every target in `CLAUDE.md`.
3. `CLAUDE.md`: make every command work unchanged on Windows and Linux.

Add tests in `tests/test_corpus_harness.py` for both virtualenv layouts.

## 3. Allowed Paths and Acceptance

As listed for `WIN-03` in `queued_task_proposals` in
`ORCHESTRATION_STATE.json` (authoritative). No change to `src/score2gp/`.
