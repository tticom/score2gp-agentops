# WIN-01 — OS-Agnostic Governance and Dispatch

- **Status**: PROMOTED (authority revision 37). `ORCHESTRATION_STATE.json` is authoritative for allowed paths, acceptance and validation commands.
- **Repository**: `tticom/score2gp-agentops`
- **Branch**: `feat/win-01-windows-native-execution`
- **Owner Role**: `implementation` (dispatched by `go`)
- **Reviewer Role**: `reviewer`
- **Delivery Action**: `pull_request`
- **Prerequisites**: `L3-00` (reconciled in `completed_tasks`)
- **Followed by**: `WIN-02` (retire the Docker/WSL runtime and shell scripts), `WIN-03` (product repository tooling)

---

## 1. Requirement and Authority

On 2026-09-23 the maintainer (`tticom`) directed that Score2GP development be
OS-agnostic, that Docker be discontinued, and that WSL be removed from the
development environment. Linux remains a deployment and test target. See
[Decision: OS-Agnostic Development Environment](../../decisions/2026-09-23-os-agnostic-development-environment.md),
which supersedes tenets 1–2 and §3 of the
[2026-09-22 decision](../../decisions/2026-09-22-windows-native-execution-migration.md).

This task was originally scoped as "Windows-native primary, WSL optional". It
is refocused on governance, identity and dispatch. Removing the Docker runtime
and the shell scripts is `WIN-02`; the product repository is `WIN-03`.

---

## 2. Bounded Objectives

1. **Role from GitHub identity, cross-checked by workspace.**
   - Resolve the role from `gh api user --jq .login` using `ORCHESTRATION_STATE.json` `roles`.
   - Cross-check the working directory: a path under `worktrees/auto`, `worktrees/gov` or `worktrees/codex` must belong to `tticom-automation`, `tticomgov-code` or `tticom-codex` respectively.
   - Fix the missing route: `score2gp_dispatch.py` currently refuses `tticomgov-code` ("unsupported Score2GP worker identity: niall; authenticated GitHub identity: tticomgov-code").
   - A mismatch, unknown login or failed `gh` call fails closed. OS usernames (`niall`, `agent`, `tticom-gov`, …) and environment variables (`SCORE2GP_AGENT_ROLE`) must never select a role. Remove those paths rather than keeping them as alternatives.
2. **Remove WSL and Linux-layout mandates from live governance.** Rewrite the WSL Execution Environment Gate, the WSL Edit Coherency Gate and the `/home/<user>` identity/workspace rules in `AGENT_CONTROL.md` as OS-neutral rules:
   - a workspace root containing `worktrees/{auto,gov,codex}`;
   - a Workspace Edit Coherency Gate: the edited checkout and the checkout where `git diff` and tests run must be the same absolute path.

   Apply the same to `ORCA_WORKFLOW.md`, `WORKFLOW_SKILLS_PROFILE.md`, `got-dispatch.md`, `address-current-pr-review.md` (`.venv/bin/python`), `CLAUDE.md`, `.agents/agents/project-director/agent.json` and `scripts/link_session.py` (WSL UNC path translation). Leave the Docker identity text in `AGENT_CONTROL.md` for `WIN-02`.

   The root agent entrypoints need the same treatment:
   - `AGENTS.md` (lines 21-43) runs the router with `python3` and says "the host Linux worker identity … selects the role". Change it to portable `python` commands and to role selection from the authenticated GitHub login, as in §2.1.
   - `AGENT-RULES.md` line 6 requires `python3 scripts/score2gp_got_bootstrap.py` at session start. Make it portable. It must keep mentioning `agent_verify.py`, `artifact_audit.py` and `pr_body.py`, because `score2gp_governance_audit.py` requires them.
3. **Portable Python and tool resolution.** Resolve `.venv/Scripts/python.exe` or `.venv/bin/python`, and fail cleanly when neither exists. Use `pathlib`; never build paths with `/` string concatenation or assume `python3` exists.
4. **One Python identity gate.** `scripts/verify_identity.py` checks the GitHub login, global Git `user.name`/`user.email` and the workspace path on any OS. There is no bash or PowerShell identity script.
5. **Test suite starts everywhere.** `tests/conftest.py` must not call `os.statvfs` where it doesn't exist, and must keep its noexec protection on Linux.
6. **Skills source is `agentops-claude-skills`.** The maintainer has replaced `tticom/agy-skills` with `tticom/agentops-claude-skills`.
   - `SKILLS_LOCK.md` pins a full commit on `agentops-claude-skills` `main`.
   - `score2gp_control_plane.py` maps `REQUIRED_SKILLS` to that repository's flat `skills/<name>` layout, not agy-skills' `skills/engineering/...` layout, and materializes pins outside `agy-skills-pins/`.
   - The `--skills-repo` defaults in `score2gp_dispatch.py` and both bootstrap scripts resolve to the `agentops-claude-skills` checkout next to the running `score2gp-agentops` checkout: `worktrees/<auto|gov|codex>/agentops-claude-skills`. Derive it from the agentops path, not the process working directory. `../../agentops-claude-skills` is wrong, because it resolves to `worktrees/agentops-claude-skills`.
   - Update the `AGENT_CONTROL.md` and `WORKFLOW_SKILLS_PROFILE.md` sections that name `agy-skills` as the locked skills source.
   - Keep every pin-mismatch, dirty-checkout and `REQUIRED_SKILL_MISSING` gate fail-closed.

---

## 3. Allowed Paths

- `projects/score2gp/AGENT_CONTROL.md`
- `projects/score2gp/ORCA_WORKFLOW.md`
- `projects/score2gp/SKILLS_LOCK.md`
- `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md`
- `projects/score2gp/prompts/next/address-current-pr-review.md`
- `projects/score2gp/prompts/next/got-dispatch.md`
- `AGENTS.md`
- `AGENT-RULES.md`
- `CLAUDE.md`
- `.agents/agents/project-director/agent.json`
- `scripts/link_session.py`
- `scripts/score2gp_control_plane.py`
- `scripts/score2gp_dispatch.py`
- `scripts/score2gp_go_bootstrap.py`
- `scripts/score2gp_got_bootstrap.py`
- `scripts/score2gp_orca_control.py`
- `scripts/verify_identity.py`
- `tests/conftest.py`
- `tests/test_dispatch_entrypoint_contract.py` (asserts `CLAUDE.md` wording)
- `tests/test_governance_audit.py` (asserts `AGENT_CONTROL.md` wording)
- `tests/test_score2gp_control_plane.py`
- `tests/test_score2gp_dispatch.py`
- `tests/test_score2gp_orchestrator.py`
- `tests/test_score2gp_orca_control.py`
- `tests/test_verify_identity.py`

This list mirrors `ORCHESTRATION_STATE.json`, which is authoritative. Tests may
change only to follow reworded documents or to cover the new behaviour; never
delete an identity, privacy or fail-closed assertion without replacing it with
an equivalent one. Historical records (runs, reports, research, reviews,
handoffs, earlier decisions) are not rewritten. Product-repository changes are
`WIN-03`.

*No file outside these allowed paths may be created, modified, or deleted.*

---

## 4. Acceptance Criteria

1. The live documents above contain no WSL execution gate, no `/home/<user>` or `/mnt/c` rule and no `.venv/bin`-only instruction. `AGENTS.md` and `AGENT-RULES.md` use portable `python` commands and describe role selection by GitHub login, not by host OS identity.
2. Role resolution behaves as in §2.1. Tests cover, at minimum:
   - each of the three logins in its own workspace (allowed);
   - each login in another identity's workspace (refused);
   - an unknown login (refused);
   - a failing `gh` call (refused);
   - `SCORE2GP_AGENT_ROLE` set to another role (ignored or refused, never obeyed).
3. Python/virtualenv resolution is portable and fails cleanly when no interpreter is found.
4. `scripts/verify_identity.py` passes on native Windows and Linux, with tests.
5. `tests/conftest.py` starts on native Windows and still redirects temp files on a Linux noexec mount.
6. The skills source is `agentops-claude-skills` as in §2.6. Tests cover:
   - a valid pin activating the required skills;
   - a pin not on `main` (refused);
   - a dirty pin checkout (refused);
   - a missing required skill (`REQUIRED_SKILL_MISSING`);
   - the default skills path resolving to the sibling `agentops-claude-skills` for each of the `auto`, `gov` and `codex` layouts, from a working directory other than the checkout.
7. The governance audit and the targeted tests pass on native Windows and in Linux CI. The full `python -m pytest` passes in Linux CI. The full suite on native Windows is `WIN-02`'s acceptance, because it depends on removing the Docker runtime tests.
8. Zero changes to product code.

---

## 5. Non-Goals

- Deleting `agent-runtime/`, shell scripts, `legacy/` or Docker references (`WIN-02`).
- Product-repository changes (`WIN-03`).
- Changing merge policy: independent review and human-only merge remain required.

---

## 6. Stop Conditions

Stop without writing if:

1. `product_recognition_semantics_modified`
2. `identity_gate_loosened_or_bypassed`: any GitHub-login or Git-author check is skipped or weakened.
3. `role_selected_from_environment_or_os_user`: a role can still be chosen by an OS username or environment variable.
4. `linux_ci_broken`
5. `unauthorized_cross_repository_writes`

---

## 7. Validation

```text
python scripts/score2gp_governance_audit.py
python -m pytest tests/test_score2gp_dispatch.py tests/test_score2gp_orchestrator.py tests/test_score2gp_orca_control.py tests/test_verify_identity.py tests/test_dispatch_entrypoint_contract.py tests/test_governance_audit.py tests/test_score2gp_control_plane.py
python -m pytest        # must pass in Linux CI
git diff --check
```

Then publish the exact-head author handback on the task PR and await independent review.
