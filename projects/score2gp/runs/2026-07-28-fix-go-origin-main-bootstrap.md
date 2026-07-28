# Operational Incident & Repair Record: Agy `go` Origin/Main Bootstrap Repair

**Task**: Dispatcher State-Transition Operational Repair
**Status**: COMPLETED
**Author**: tticom-codex
**Repository**: tticom/score2gp-agentops
**Branch**: `codex/fix-go-origin-main-bootstrap`

## Observed Failure Mode

Following the external merge of AgentOps PR #389 (`285582947a60f122eb4890c2b179ca6e05693c25`), remote governance main moved to `73382c06b5682a6ef06591f48cfcee117cfa4aee`, promoting task PDFTAB-DUR-03 (`agy/pdftab-duration-extraction-architecture`).

However, Agy's local working trees remained checked out on the completed task branch (`agy/generate-public-pdf-tab-duration-fixture`). When `go` executed, it fetched remote state but read `ACTIVE_TASK.md` from the stale local working tree (task PDFTAB-DUR-02) rather than `origin/main`. Consequently, `go` returned `MERGED_AWAITING_GOVERNANCE_PROMOTION` even though the promotion PR had already merged.

## Executable Repair Implementation

Created `scripts/score2gp_go_bootstrap.py` and updated `projects/score2gp/prompts/next/go-dispatch.md` and `projects/score2gp/AGENT_CONTROL.md`.

The helper script enforces a 6-phase state transition:
1. **Identity & Cleanliness**: Verifies identity and requires clean working trees in both AgentOps and Product repositories before making any branch mutations.
2. **Fetch Authoritative State**: Fetches `origin/main` in AgentOps and reads `ACTIVE_TASK.md` directly from `origin/main` (`git show origin/main:projects/score2gp/ACTIVE_TASK.md`).
3. **Synchronize AgentOps Canonical Branch**: Switches to `main` and fast-forwards to `origin/main` (`git merge --ff-only origin/main`). Verifies working-tree `ACTIVE_TASK.md` matches `origin/main`.
4. **Synchronize Authorised Output Repository**: Reads `Repository` from `ACTIVE_TASK.md` metadata, switches to `main` in that repository, and fast-forwards to `origin/main`.
5. **Select Authorised Task Branch**: Switches to or creates the branch declared by `PR Branch` from `origin/main`.
6. **Dispatch**: Emits machine-actionable state JSON.

## Test Verification

Added `tests/test_score2gp_go_bootstrap.py` covering 10 automated regression scenarios using synthetic temporary Git repositories:
1. Completed task branch with stale local main & changed remote task (reproduces observed failure mode).
2. Fetch succeeds when working tree task differs from `origin/main`.
3. AgentOps and Product repositories both behind remote main.
4. Dirty working tree hard stop.
5. Local main cannot fast-forward hard stop.
6. Authorised branch already exists remotely.
7. Exact PR already exists.
8. Merged old task plus merged new governance promotion.
9. Repository field selecting `score2gp-agentops`.
10. Missing or malformed required task fields fail closed.

All 10 automated regression tests passed.
