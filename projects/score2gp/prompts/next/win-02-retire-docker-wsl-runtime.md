# WIN-02 — Retire the Docker/WSL Agent Runtime and Shell Scripts

- **Status**: PROPOSED. Not executable until `WIN-01` is merged, reconciled and governance promotes this task.
- **Repository**: `tticom/score2gp-agentops`
- **Branch**: `feat/win-02-retire-docker-wsl-runtime`
- **Owner Role**: `implementation`
- **Reviewer Role**: `reviewer`
- **Delivery Action**: `pull_request`
- **Prerequisites**: `WIN-01`

---

## 1. Authority

[Decision: OS-Agnostic Development Environment](../../decisions/2026-09-23-os-agnostic-development-environment.md)
(maintainer, 2026-09-23): Docker is discontinued, WSL is removed from
development, and tooling is Python only. The maintainer has accepted losing
the Docker sandbox (decision §2.7).

## 2. Objectives

1. **Delete the Docker runtime.** Remove `agent-runtime/` entirely:
   - `cycle.py`, `worker.py`, `egress_proxy.py`, `assignment_adapter.py` and `supervisor.py`;
   - the Dockerfiles, `compose.yaml` and `.dockerignore`;
   - `policies/`, `README.md` and every `*.sh` script.

   Also delete the tests that only exercise it: `test_agent_runtime.py`, `test_assignment_adapter.py`, `test_codex_runtime.py`, `test_cycle_egress.py`, `test_disposable_cycle.py` and `test_supervisor.py`.

   Before deleting, search the repository for live callers (code, CI and non-historical documents). If one exists, stop with `live_caller_of_deleted_runtime_found`.
2. **Delete the remaining shell scripts.** Remove `scripts/agy-cycle` (a bash wrapper around `agy_cycle.py`), `scripts/status.sh`, `scripts/capture-pytest.sh`, `scripts/capture-developer-diff.sh` and `legacy/`. Update `tests/test_governance_audit.py::test_operational_scripts_default_to_current_linux_home`, which asserts on the three helpers. The repository must end with no `.sh` or `.ps1` file.
3. **Make `scripts/agy_cycle.py` portable.** It imports `pty` at module level, which fails on Windows (`termios`). Only the interactive agent launch (`pty.fork()`, about line 517) needs a terminal:
   - import `pty`/`select` inside that function, or replace it with a portable `subprocess` equivalent;
   - keep the Linux interactive behaviour, or document and test its replacement;
   - document `python scripts/agy_cycle.py …` as the entry point in `README.md` and the `docs/agy-cycle-*.md` plans.
4. **Remove Docker references from live text.** `README.md` ("Docker is optional hardening…"), the Docker identity section of `projects/score2gp/AGENT_CONTROL.md`, and the `docs/agy-cycle-*.md` plans. Do not edit historical records.
5. **Full suite on every OS.** `python -m pytest` must pass on native Windows and in Linux CI. Do not add platform skips to hide failures; a skip is acceptable only for behaviour that genuinely exists on one OS, and it needs a stated reason. Keep `.github/workflows/governance-control-plane.yml` running the full suite on Ubuntu, and update its `py_compile` line if files move.

## 3. Allowed Paths

See `next_task_proposal.allowed_paths` in `ORCHESTRATION_STATE.json`
(authoritative). Directory entries (`agent-runtime/`, `legacy/`) cover deleting
their whole contents.

## 4. Acceptance

As listed in `ORCHESTRATION_STATE.json`. In short: runtime and shell scripts
gone; `agy_cycle.py` imports everywhere; no live Docker references; full suite
green on native Windows and Linux CI; no product code touched.

## 5. Stop Conditions

`product_recognition_semantics_modified`, `identity_gate_loosened_or_bypassed`,
`live_caller_of_deleted_runtime_found`, `linux_ci_broken`,
`unauthorized_cross_repository_writes`.
