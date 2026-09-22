# WIN-01 Task Proposal and Governance Handoff

## Authority

- **Active Task**: `L3-00` — Lesson 3 native source contract and red acceptance (`status: PROMOTED`, `pull_request: 462`)
- **Authority Source**: `projects/score2gp/ORCHESTRATION_STATE.json` (Authority Revision 35)
- **Proposed Successor Task**: `WIN-01` — Windows-Native Primary Execution Migration (`status: PROPOSED`, `dependencies: ["L3-00"]`)
- **Maintainer Decision**: Present maintainer direction on 2026-09-22 authorizing preparation of successor task `WIN-01` ([Decision Record](../decisions/2026-09-22-windows-native-execution-migration.md))
- **Project Profile**: `projects/score2gp/AGENT_CONTROL.md`
- **Skills Revision**: `439404f7342f4e324147efb6b0276f698fbf2bdb` (pinned in `SKILLS_LOCK.md`)

## Repository state

- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Repository**: `tticom/score2gp`
- **Product PR #462 State**: `MERGED` by maintainer `tticom` at `2026-09-21T20:51:51Z` (head: `8c2a2d7316aced550c0b292fa2dae8c93b68c3f3`, merge commit: `1672d5de4560f9fa76913274f9ee41bac46fc36b`)
- **Base Revision (`score2gp-agentops`)**: `1acecc57e66b5e9a710154eaf7c82d4ed3311a85`
- **Governance Branch**: `governance/propose-win-01-windows-native`
- **Local HEAD**: `4d04ed4b5c6a45ce85757d1b832bc15be7fef334`
- **Worktree Status**: Clean working tree; no uncommitted diffs

## Outcome and scope

- **Outcome**: Smallest valid successor-task proposal/authority packet created for `WIN-01` in the governance repository.
  - Recorded present maintainer authorization as a binding decision.
  - Defined bounded task prompt for `WIN-01` in `projects/score2gp/prompts/next/win-01-windows-native-execution-migration.md`.
  - Added `WIN-01` as `next_task_proposal` in `ORCHESTRATION_STATE.json` (bumped authority revision 34 -> 35).
  - Explicitly blocked `WIN-01` from execution until `L3-00` is reconciled and the authority promotes it.
  - Retained active task `L3-00` untouched in `task` and left `ACTIVE_TASK.md` 100% byte-for-byte aligned with generated authority.
  - Updated backlog in `projects/score2gp/PLANNING_DATA.md`.
- **Changed paths**:
  - `projects/score2gp/decisions/2026-09-22-windows-native-execution-migration.md`
  - `projects/score2gp/prompts/next/win-01-windows-native-execution-migration.md`
  - `projects/score2gp/ORCHESTRATION_STATE.json`
  - `projects/score2gp/PLANNING_DATA.md`
  - `projects/score2gp/handoffs/2026-09-22-windows-native-execution-task-proposal.md`
- **Frozen or excluded scope**:
  - Zero product files modified; no changes to `score2gp` repository.
  - No changes to `ACTIVE_TASK.md` (re-rendering authority produces identical content).
  - No alteration of `L3-00` task status (it remains `PROMOTED` pending governance reconciliation).
  - No merge actions performed.

## Evidence

- **Independently verified**:
  - `verify_identity.sh`: passed with `os_user=tticom`, `home=/home/tticom`, `host_login=tticomgov-code`, `git_name=tticomgov-code`, `git_email=tticomgov-code@users.noreply.github.com`, `repo_prefix=/home/tticom/work/score2gp-workspace`.
  - Python compile check: `python3 -m compileall -q scripts tests` passed cleanly.
  - Offline governance audit: `SCORE2GP_GOVERNANCE_AUDIT_OFFLINE=1 python3 scripts/score2gp_governance_audit.py` passed with zero violations.
  - Orchestrator test suite: `PYTHONPATH=. pytest tests/test_score2gp_orchestrator.py tests/test_score2gp_orca_control.py` passed (86/86 passed).
  - Authority probe: `render_active_task(authority) == ACTIVE_TASK.md` confirmed byte-for-byte; `build_task_registry` registers `WIN-01` with `lifecycle_state: successor_prepared`.
  - PR #462 state: `gh pr view 462 --repo tticom/score2gp` confirmed `state: MERGED`, `mergedBy: tticom`, `headRefOid: 8c2a2d7316aced550c0b292fa2dae8c93b68c3f3`, `mergeCommit: 1672d5de4560f9fa76913274f9ee41bac46fc36b`.
- **Live blocker**:
  - `score2gp_governance_audit.py` online check reports that product PR #462 on branch `feat/l3-00-native-acceptance` is already `MERGED` on `tticom/score2gp`. Active task `L3-00` requires post-merge reconciliation into `completed_tasks` before any successor task can be promoted or dispatched.
- **Intentionally unrun**:
  - Task execution of `WIN-01`: strictly blocked until promoted.

## Risks and comments

- **Unresolved risks**: None for proposal recording. Line-ending (CRLF vs LF) and path-separator normalization will be verified during `WIN-01` implementation.
- **Review threads**: None open.
- **Safety safeguards**: Direct pushes to `main`, force pushes, branch deletions, admin bypasses, self-approvals, and tracking private fixtures remain unconditionally prohibited.

## Next authorised action

1. **Governance Reconcile `L3-00`**: Execute standard post-merge state reconciliation (`score2gp_orca_control.py reconcile --task-id L3-00` or governance reconciliation cycle) to move `L3-00` into `completed_tasks` with its verified merge commit `1672d5de4560f9fa76913274f9ee41bac46fc36b` and head SHA `8c2a2d7316aced550c0b292fa2dae8c93b68c3f3`.
2. **Promote `WIN-01`**: Promote `WIN-01` from `next_task_proposal` into `task` via a dedicated governance promotion PR.
3. **Claude Implementation Execution**: Once promoted, Claude begins `WIN-01` implementation under the defined prompt in `projects/score2gp/prompts/next/win-01-windows-native-execution-migration.md`.
