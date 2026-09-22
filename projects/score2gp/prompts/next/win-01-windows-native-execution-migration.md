# WIN-01 — Windows-Native Primary Execution Migration

- **Status**: PROPOSED; explicitly blocked from execution until `L3-00` is reconciled and orchestration authority promotes it.
- **Repository**: `tticom/score2gp-agentops` (governance control plane and scripts)
- **Suggested Branch**: `feat/win-01-windows-native-execution`
- **Owner Role**: `governance`
- **Reviewer Role**: `reviewer`
- **Delivery Action**: `pull_request`
- **Prerequisites**: `L3-00` (reconciled in `completed_tasks`)

---

## 1. Requirement and Authority

On 2026-09-22, the project maintainer (`tticom`) explicitly authorized preparing this successor governance task to **remove WSL as a mandatory prerequisite and make native Windows the supported primary execution environment** for Score2GP development, testing, and governance.

The complete rationale and architectural principles are recorded in [Decision: Windows-Native Primary Execution Migration and WSL Deprecation](../../decisions/2026-09-22-windows-native-execution-migration.md).

This task is **not executable** while `L3-00` (PR #462) remains in `task` or until Orca / the governance authority promotes it into active execution.

---

## 2. Bounded Objectives

The implementation agent executing this task must satisfy these bounded objectives:

1. **Remove Mandatory WSL Requirement**: Eliminate all policy language and gate logic in `projects/score2gp/AGENT_CONTROL.md` that strictly mandates Ubuntu WSL or treats Windows-host execution as an environment boundary failure.
2. **Define Windows-Native Canonical Workspace**:
   - Establish standard canonical paths for Windows (e.g. `C:\Users\<user>\work\score2gp-workspace\score2gp` and `...\score2gp-agentops`).
   - Define a cross-platform **Workspace Edit Coherency Gate** verifying that the editor and test execution commands operate on the identical absolute checkout path.
3. **Replace Linux-Only Command and Path Assumptions**:
   - Update Python virtual environment discovery to check `.venv\Scripts\python.exe` (Windows) alongside `.venv/bin/python` (Linux/WSL).
   - Provide a cross-platform identity gate (`scripts/verify_identity.py` or `.ps1`) verifying OS user, user home, GitHub login, Git author credentials, and workspace path without depending on bash syntax.
   - Ensure `scripts/score2gp_dispatch.py`, `scripts/score2gp_go_bootstrap.py`, and `scripts/score2gp_got_bootstrap.py` work seamlessly on Windows PowerShell and cmd.
4. **Retain WSL as Optional**: Ensure Linux/WSL and containerized runners (`agent-runtime/`) continue to function without regressions. WSL is an optional secondary environment, not prohibited.
5. **Strict File Scope**: Update only the governance and product files proven necessary by inventory. Do not broaden into unrelated product behavior.
6. **Safeguards Against Coherency and Git Hazards**:
   - Enforce edit-to-execution worktree matching before any edit.
   - Retain all prohibitions against direct pushes to `main`, force-pushes, branch deletions, admin bypasses, or self-approvals.
   - Guarantee private fixture repositories (`score2gp-private-fixtures`) and generated outputs remain untracked and gitignored.

---

## 3. Allowed Paths

### Governance Repository (`tticom/score2gp-agentops`)
- `projects/score2gp/AGENT_CONTROL.md`
- `projects/score2gp/CLAUDE.md`
- `CLAUDE.md`
- `scripts/score2gp_dispatch.py`
- `scripts/score2gp_go_bootstrap.py`
- `scripts/score2gp_got_bootstrap.py`
- `scripts/verify_identity.sh`
- `scripts/verify_identity.py`
- `tests/test_score2gp_dispatch.py`
- `tests/test_score2gp_orchestrator.py`

### Product Repository Companion Scope (`tticom/score2gp`)
*(To be executed via companion PR if needed)*
- `CLAUDE.md`
- `scripts/corpus_harness.py`
- `scripts/agent_verify.py`

*No file outside these allowed paths may be created, modified, or deleted.*

---

## 4. Acceptance Criteria

1. **WSL Mandatory Requirement Removed**: `AGENT_CONTROL.md` no longer requires `uname -s == Linux` or `wsl.exe`. Windows PowerShell (Desktop or 7+) is explicitly documented and supported as primary.
2. **Cross-Platform Identity Verification**: A Python-based `verify_identity.py` (or PowerShell equivalent) passes on native Windows and Linux/WSL, asserting:
   - Operating system user and home directory
   - Remote Git-host login (`gh api user --jq .login`)
   - Global Git config `user.name` and `user.email`
   - Canonical workspace root prefix
3. **Cross-Platform Virtualenv Resolution**: Bootstrap scripts and dispatchers resolve:
   - Windows: `.venv\Scripts\python.exe`
   - Linux/WSL: `.venv/bin/python`
   Failing cleanly if neither is present.
4. **Workspace Edit Coherency Gate**: A documented procedure and automated check confirm that file edits occurring via IDE/agent tools are visible in the exact git worktree where `git diff` and tests execute.
5. **Audit and Suite Pass**:
   - `python3 scripts/score2gp_governance_audit.py` passes with zero violations.
   - All tests in `tests/test_score2gp_dispatch.py`, `tests/test_score2gp_orchestrator.py`, and `tests/test_score2gp_orca_control.py` pass.
   - `git diff --check` exits 0.
6. **Zero Semantic Changes**: Zero lines of product code in `src/score2gp/` are touched. Recognition algorithms, geometry models, schemas, and export logic remain completely unchanged.

---

## 5. Non-Goals

- **Non-goal 1**: Modifying any parser, recognizer, tab alignment, pitch assignment, or ScoreIR compiler logic.
- **Non-goal 2**: Removing or breaking Linux GitHub Actions CI workflows (`.github/workflows/pylint.yml`).
- **Non-goal 3**: Changing merge policy: maintainer merge and independent review approval remain strictly required.
- **Non-goal 4**: Automatic cross-filesystem synchronization or copying files between WSL and Windows directories.

---

## 6. Rollback and Stop Conditions

Immediate hard stop without write if:
1. `product_recognition_semantics_modified`: Any product code in `src/score2gp/` is changed.
2. `identity_gate_loosened_or_bypassed`: Any check for GitHub identity or Git author matching is skipped or disabled.
3. `cross_checkout_desynchronization`: The working tree being edited does not match the working tree being tested.
4. `wsl_compatibility_broken_without_fallback`: Changes cause existing Linux CI or container workers to fail.
5. `private_fixture_leakage`: Any private score, PDF, MusicXML, or generated `.gp` file is staged or committed.

---

## 7. Claude Implementation Handoff

When `WIN-01` is promoted to active execution, the executing agent (Claude) must follow this exact sequence:

### Step 1: Preflight Verification
Confirm environment on Windows (or WSL during transition):
```powershell
# Windows PowerShell
python --version
git --version
gh auth status
git status
```

### Step 2: Implement Cross-Platform Identity Gate
Create `scripts/verify_identity.py` to replace or supplement `scripts/verify_identity.sh`.
Ensure it supports `--os-user`, `--home`, `--host-login`, `--git-name`, `--git-email`, and `--repo-prefix` across Windows and Linux.

### Step 3: Update Governance Policy in `AGENT_CONTROL.md`
- Replace "WSL Execution Environment Gate" with "Primary Windows-Native Execution Environment & Optional WSL Gate".
- Replace "WSL Edit Coherency Gate" with "Workspace Edit Coherency Gate".
- Update startup commands to include PowerShell syntax alongside bash.

### Step 4: Update Dispatch and Bootstrap Helpers
- In `scripts/score2gp_go_bootstrap.py` and `scripts/score2gp_got_bootstrap.py`:
  Add `.venv\Scripts\python.exe` check when `os.name == 'nt'`.
- In `scripts/score2gp_dispatch.py`:
  Ensure cross-platform path handling and Windows identity resolution.

### Step 5: Validate and Audit
Run:
```powershell
python scripts/score2gp_governance_audit.py
python -m pytest tests/test_score2gp_dispatch.py tests/test_score2gp_orchestrator.py
git diff --check
```

### Step 6: Publish Author Handback
Publish exact-head handback on the task PR, verify checks, and await independent review.
