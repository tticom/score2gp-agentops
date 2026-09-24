# WIN-04 Reorder Promotion Handoff

## Authority

- Promoted task: `WIN-04` - Post-migration governance hygiene and merge-rule alignment (`PROMOTED`)
- Next proposal: `L3-01` - Paired-staff barline acceptance for the Lesson 3 first system
  (`PROMOTED` -> `PROPOSED`, otherwise unchanged)
- Authority source: `projects/score2gp/ORCHESTRATION_STATE.json` (authority revision 41 -> 42)
- Base: `main` at `c8207b545e6da8371e216f1ef75cbfa1502bd5cd`. That is #686, which promoted L3-01 and
  set `merge_policy.minimum_approvals` to 1, merged at reviewed head
  `194f3ba083956a78eb2a0467541b0a4feda79311`.
- Ordering: on 2026-09-24 the maintainer `tticom` directed that WIN-04 goes before L3-01, so agent
  merge authority is aligned before product work continues. L3-01 had no branch, PR or work
  started, so returning it to `PROPOSED` discards nothing.
- Governance publisher: `tticomgov-code` from `worktrees/gov`

## Outcome and scope

- Swapped `task` and `next_task_proposal`: WIN-04 is `PROMOTED` and L3-01 is `PROPOSED`.
- WIN-04's scope is frozen at promotion with one addition to the #685 proposal:
  - `tests/test_score2gp_control_plane.py` is added to `allowed_paths`.
  - A matching acceptance criterion is added: `test_role_policy_is_derived_from_authority_roles`
    asserts only that `tticom-automation` never merges and that delegated mergers equal the
    `roles.merge_controller` logins, so it passes whether `merge_controller` is empty or holds
    [`tticom-codex`, `tticomgov-code`].
  - The targeted validation command includes that file.
- `merge_policy` is unchanged here; #686 already set it to 1. `roles.merge_controller` is unchanged (empty).
- Changed paths: `ORCHESTRATION_STATE.json`, `ACTIVE_TASK.md`, this handoff.

## Notes carried forward for L3-01

- H1 (require a TAB-staff stroke at the same x) conflicts with
  `tests/test_barline_recovery.py::test_notation_to_tab_barline_inheritance`, whose internal
  barlines cross only the notation staff. Record that as H1's counterexample and take the prompt's
  H2 pivot, unless H1 can be met by a TAB-staff stroke that the TAB filter rejected.
- Local test runs on this Windows host need `python -m pytest --capture=sys`. Under the default fd
  capture, subprocess-based tests fail with `WinError 6`, which is a host artifact.

## Next authorised action

- Action: `tticom-automation` implements WIN-04 on `feat/win-04-post-migration-governance-hygiene`
  in `tticom/score2gp-agentops`. A non-author reviewer then publishes an exact-head APPROVE or
  REQUEST_CHANGES.
- Merge: the maintainer `tticom` merges.
  - `roles.merge_controller` is empty, so `scripts/score2gp_control_plane.py::role_policy` classes
    `tticom-codex` and `tticomgov-code` as never-merge. Neither agent merges until a separate
    governance change adds them to `merge_controller` and that change is merged.
  - That change follows WIN-04's merge, together with WIN-04's reconciliation and L3-01's promotion.
- Stop condition: any WIN-04 stop condition; the governance audit failing on `main`.
