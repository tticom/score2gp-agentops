# Decision: Windows-Native Primary Execution Migration and WSL Deprecation

- **Date**: 2026-09-22
- **Status**: APPROVED by Maintainer (`tticom`)
- **Authority**: Present Maintainer Direction
- **Related Tasks**: `L3-00` (PR #462), `WIN-01` (Proposed Successor)

---

## 1. Context and Problem Statement

Score2GP governance previously enforced a strict **WSL Execution Environment Gate** in `AGENT_CONTROL.md`, prohibiting direct Windows execution, PowerShell, Windows Python virtual environments, and Windows Git/GitHub tooling. All agent work was required to run inside an Ubuntu WSL environment.

In practice, this policy introduced material operational friction and risk:
1. **Dual-Environment Friction**: The maintainer's primary host and inspection environment is native Windows. Maintaining parallel checkout hierarchies (WSL ext4 vs. Windows NTFS) causes IDE-to-worktree coherency confusion, worktree bind-mount complexities, and path-translation edge cases.
2. **Native Product Verification**: Guitar Pro (`.gp`) file verification, audio playback acceptance, and desktop GUI smoke checks are inherently desktop operations best verified where native tools reside.
3. **Validation Discrepancies**: During `L3-00` implementation (PR #462), the developer on native Windows encountered 16 baseline test failures that passed in Linux CI, driven by OS-specific path, virtualenv, and subprocess assumptions rather than core product defects.
4. **Toolchain Maturity**: Python ≥3.11, PyMuPDF, Git, and GitHub CLI (`gh`) are fully supported and stable on native Windows with PowerShell.

## 2. Present Decision

The maintainer has explicitly authorized transitioning Score2GP to **Windows-native as the supported primary execution environment** and deprecating WSL as a mandatory prerequisite.

Key architectural tenets of this decision:
1. **Primary Windows-Native Support**: Native Windows PowerShell, Python ≥3.11 (`.venv\Scripts\python.exe`), native Git, and GitHub CLI (`gh.exe`) become the primary, first-class execution and governance environment.
2. **WSL Demoted to Optional**: WSL remains supported as an optional secondary environment for developers choosing Linux on Windows, but no governance rule, audit script, or product gate may mandate WSL or fail solely due to executing on native Windows.
3. **Workspace & Coherency Gate**: The "WSL Execution Environment Gate" and "WSL Edit Coherency Gate" are replaced with a cross-platform **Workspace Edit Coherency Gate** ensuring that the editing agent and validation commands operate on the identical absolute checkout path.
4. **No Semantic Product Changes**: This migration is strictly operational, tooling, and governance. It does not alter musical recognition, geometry extraction, layout grouping, ScoreIR schemas, or Guitar Pro export algorithms.
5. **Precedence and Promotion Sequencing**:
   - `L3-00` (product PR #462, merged on remote `main`) remains the current promoted task until formally reconciled into `completed_tasks`.
   - The successor task `WIN-01` is recorded in `next_task_proposal` with status `PROPOSED`.
   - `WIN-01` is strictly blocked from execution until `L3-00` reconciliation is complete and the governance authority promotes `WIN-01`.
   - *Update 2026-09-23:* `L3-00` was reconciled and `WIN-01` promoted (PRs #678 and #679). At the maintainer's direction, authority revision 37 reassigns `WIN-01` to the implementation role so `go` can dispatch it, and aligns its allowed paths with the files that carry the WSL mandate.

## 3. Scope Inventory

### 3.1 Governance Repository (`score2gp-agentops`)
- `projects/score2gp/AGENT_CONTROL.md`: Remove mandatory WSL gates; define Windows canonical workspace structure; add cross-platform coherency gate.
- `scripts/verify_identity.py` (or PowerShell equivalent): Cross-platform identity verification replacing Linux-only bash checks.
- `scripts/score2gp_dispatch.py`: Handle Windows path separators, Windows usernames, and native GitHub CLI credential retrieval.
- `scripts/score2gp_go_bootstrap.py` & `scripts/score2gp_got_bootstrap.py`: Support `.venv\Scripts\python.exe` virtualenv path resolution.
- `CLAUDE.md`: Provide native Windows PowerShell execution guidance.

### 3.2 Product Repository (`score2gp`)
- `CLAUDE.md`: Provide PowerShell instructions (`.venv\Scripts\Activate.ps1`, `python -m pytest`).
- `scripts/corpus_harness.py`: Resolve `.venv\Scripts\score2gp.exe` and `.venv\Scripts\python.exe` alongside POSIX `.venv/bin/`.
- `scripts/agent_verify.py` & `scripts/artifact_audit.py`: Verify path handling on Windows without hardcoded `/` assumptions.

## 4. Consequences

- **Positive**: Eliminates WSL setup overhead; removes cross-filesystem synchronization errors; aligns development with maintainer desktop environment; unblocks clean Windows pytest runs.
- **Negative / Risks**: Must ensure Windows CRLF/LF line endings, backslash path escaping, and shell quoting are handled reliably without breaking Linux CI.
