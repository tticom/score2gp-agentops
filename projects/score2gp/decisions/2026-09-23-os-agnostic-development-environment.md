# Decision: OS-Agnostic Development Environment; Docker and WSL Removed from Development

- **Date**: 2026-09-23
- **Status**: APPROVED by Maintainer (`tticom`)
- **Authority**: Present Maintainer Direction (2026-09-23)
- **Supersedes**: tenets 1–2 and §3 of [2026-09-22 Windows-Native Primary Execution Migration](2026-09-22-windows-native-execution-migration.md)
- **Related Tasks**: `WIN-01` (active, refocused), `WIN-02` (proposed), `WIN-03` (queued)

---

## 1. Context

The 2026-09-22 decision made native Windows the primary environment but kept
WSL as an optional secondary environment and kept the Docker agent runtime
(`agent-runtime/`). In practice:

1. Working in WSL is too difficult, and headless development in WSL is
   impossible. Nothing depends on a WSL shell starting an agent, so the
   `~/.bashrc` auto-start hook (`configure-shell-startup.sh` →
   `start-instance.sh`) has no future use.
2. Docker use is being discontinued. The Docker "disposable cycle" runtime
   (`agent-runtime/`: `cycle.py`, `worker.py`, `egress_proxy.py`,
   `assignment_adapter.py`, `supervisor.py`, Dockerfiles, `compose.yaml` and 14 shell scripts) has no
   callers outside its own tests and documentation. The dispatcher and Orca
   control plane do not use it.
3. The shell scripts cannot run on native Windows without bash, and the
   Python around them uses POSIX-only APIs (`os.getuid`, `os.statvfs`, `pty`).

## 2. Decision

1. **OS-agnostic development.** Score2GP development, governance, dispatch and
   validation must work on any OS with Python ≥3.11, Git and `gh`. No rule,
   script, test or gate may depend on a particular OS, shell, distribution or
   home-directory layout.
2. **Python only for tooling.** Operational tooling is Python. No bash or
   PowerShell script is required to develop, dispatch, validate or review.
   Existing shell scripts are either deleted with the runtime they serve or
   replaced with Python.
3. **Docker removed.** The Docker agent runtime is retired and all Docker
   references are removed from live code, tests and governance documents.
4. **WSL removed from development.** WSL references, gates and dependencies
   are removed from the development environment. There is no WSL execution
   gate, no `/home/<user>` or `/mnt/c` path rule and no `~/.bashrc` auto-start.
5. **Linux remains a deployment and test target.** Score2GP is expected to be
   deployed to Linux. Linux CI (GitHub Actions, Ubuntu) and, optionally, a WSL
   or other Linux checkout are used to prove the system still works on Linux.
   Code must therefore stay portable; Linux-specific behaviour is not removed,
   only made non-mandatory.
6. **Role from identity, cross-checked by workspace.** A worker's role comes
   from the authenticated GitHub login (`gh api user --jq .login`):
   `tticom-automation` → implementation/author; `tticomgov-code` and
   `tticom-codex` → reviewer/governance, as listed in
   `ORCHESTRATION_STATE.json` `roles`. The working directory is a cross-check:
   a workspace under `worktrees/auto`, `worktrees/gov` or `worktrees/codex`
   must match `tticom-automation`, `tticomgov-code` or `tticom-codex`
   respectively. A mismatch, an unknown login or a failed `gh` call fails
   closed. OS usernames and environment variables never select a role.
7. **Loss of container isolation accepted.** Docker provided a sandbox:
   network egress limited to an allowlist, the GitHub token kept out of the
   agent process, no direct push from the agent, and a throwaway clone per
   cycle. The maintainer accepts losing it. The remaining safeguards are
   Orca task scoping, allowed-path enforcement, per-identity GitHub token
   permissions, separate author/reviewer identities, branch protection and
   human-only merge.
8. **Historical records are not rewritten.** Runs, reports, research,
   reviews, handoffs and earlier decisions keep their WSL/Docker references as
   a record of what happened. Only live rules, prompts, code and tests change.
9. **No semantic product changes.** Recognition, geometry, grouping, ScoreIR
   and GP export behaviour are unchanged.

## 3. Task Split

| Task | Repository | Scope |
|---|---|---|
| `WIN-01` (active) | `score2gp-agentops` | Role resolution from GitHub login plus workspace cross-check (including the missing `tticomgov-code` route); cross-platform virtualenv and tool resolution; Python identity gate; remove WSL/`/home`/`.venv/bin` mandates from live governance documents and prompts; `tests/conftest.py` portability. |
| `WIN-02` (proposed) | `score2gp-agentops` | Delete `agent-runtime/` and its tests; delete the obsolete `scripts/*.sh` helpers and `legacy/`; make `scripts/agy_cycle.py` portable (no module-level `pty`); remove Docker references from live docs; full `python -m pytest` passes on native Windows and Linux CI. |
| `WIN-03` (queued) | `score2gp` | Product repository: remove WSL references and POSIX-only virtualenv assumptions (`scripts/corpus_harness.py`, `Makefile`, `CLAUDE.md`). |

## 4. Consequences

- **Positive**: One workflow on every OS; no shell or container prerequisites;
  the full test suite can run where development happens; much less code to
  maintain.
- **Negative / Risks**: Agents run directly on the host without container
  isolation (accepted, §2.7). Linux regressions are caught by CI rather than
  by daily development, so CI must keep running the full suite on Ubuntu.
