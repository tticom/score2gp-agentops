# GOV-03 — Active-task PR discovery and fail-closed binding

- **Status**: PROPOSED (queued in `ORCHESTRATION_STATE.json`). Governance must promote it before execution.
- **Repository**: `tticom/score2gp-agentops`
- **Branch**: `feat/gov-03-active-task-pr-discovery`
- **Owner Role**: `implementation`
- **Reviewer Role**: `reviewer`
- **Delivery Action**: `pull_request`

## 1. Defect (observed 2026-09-25, authority revision 46)

For L3-01, the dispatcher returned `READY` / `authorised_task_without_pr` with `pull_request: null`. In fact tticom/score2gp#464 was OPEN on the task branch, with a CHANGES_REQUESTED review at its exact head `22048b6`. Followed literally, `READY` would have restarted the task from its original prompt and ignored a blocking finding. This **fails open**.

Root cause (read from code at `5ce2547`):

1. `scripts/score2gp_go_bootstrap.py:78` snapshots live PR state only when the authority already holds a PR number. Otherwise it writes `{}`. `score2gp_got_bootstrap.py` has the same pattern.
2. With empty live state, `resolve_state` (`scripts/score2gp_orca_control.py:414-417`) maps `PROMOTED` to `READY / authorised_task_without_pr`. `tests/test_score2gp_orca_control.py` pins that mapping.
3. If a live PR were supplied while the authority number is null, `orca_control.py:420-422` returns `BLOCKED / active_task_missing_pull_request`, so discovery alone is not enough.
4. Nothing records the PR number in the authority while a task is in flight. The only precedent is a manual governance commit (`0f13e8a`).
5. `validate_legacy_alignment` skips the PR check when both sides are null or TBD. The governance audit queries `gh pr list --head` but flags only MERGED, never an OPEN PR missing from the authority.

## 2. Goal

The dispatcher must never report "no PR" while a PR exists for the active task's exact repository, branch and base. It must route a discovered PR exactly as a bound PR for author and reviewer actions, and fail closed on any ambiguity.

## 3. Required behaviour

1. **Discovery.** When the authority PR number is null and the task is not terminal, list PRs for the task's `repository`, `branch` and `base_branch` (all states).
   - Exactly one match, authored by an implementation-role login: use it, and mark it `pr_binding: discovered`.
   - No match, but the remote branch has commits ahead of base: `BLOCKED / active_task_branch_without_pr`.
   - More than one match, the wrong base, or an author outside the implementation role: `BLOCKED` with a named reason.
2. **Routing.** A discovered PR is routed like a bound PR (for example `current_head_changes_requested` → address the review). The result carries `binding_required: true` and a `next_action` asking governance to record the number.
3. **Merge gate unchanged.** `verify_merge_gate` still requires the number in the authority, so no merge happens on a discovered binding alone.
4. **Audit.** The governance audit flags an OPEN PR on the active branch that is not recorded in the authority.

## 4. Allowed paths

- `scripts/score2gp_go_bootstrap.py`, `scripts/score2gp_got_bootstrap.py`, `scripts/score2gp_orca_control.py`, `scripts/score2gp_governance_audit.py`
- `tests/test_score2gp_orca_control.py`, `tests/test_score2gp_dispatch.py`, `tests/test_governance_audit.py`

## 5. Acceptance

1. **Replay test** of the 2026-09-25 state: authority revision 46, `pull_request: null`, and faked `gh` returning #464 OPEN at `22048b6` with CHANGES_REQUESTED. The result is `RUNNING / current_head_changes_requested`, `binding_required: true`, expected head `22048b6…`, and never `READY`.
2. **Negative controls:**
   - two PRs → `BLOCKED`;
   - wrong base → not bound;
   - author outside the implementation role → not bound;
   - branch with commits but no PR → `BLOCKED`;
   - closed and unmerged → `BLOCKED`;
   - merged → governance required.
3. **Merge gate:** `DENY` while the authority number is null, even with an APPROVE on a discovered PR.
4. **Mutation check:** with discovery disabled, the replay test fails.
5. Existing dispatcher tests pass, except the pinned `authorised_task_without_pr` expectation, which is updated only for the case where a PR exists.
6. `python -m pytest`, `python scripts/score2gp_governance_audit.py` and `git diff --check` pass.

## 6. Stop conditions

- `merge_gate_weakened`
- `role_boundary_changed`
- `product_edit_required`
