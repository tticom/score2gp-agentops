# GOV-01 Reconciliation, Delegated Merge Enablement and GOV-02 Promotion Handoff

## Authority

- Reconciled task: `GOV-01` - Delegated merge execution through the merge gate (audited) (`COMPLETED`)
  - PR tticom/score2gp-agentops#691, `MERGED` by `tticom` at 2026-09-24T18:16:58Z
  - Head `9d721675241b934d2c1f176889c24164560d37c6`, approved by tticom-codex in `devils-advocate-review` (review `5308362238`)
  - Merge commit `0a442eb2af4d58a9c542fd580766cb7ec58f1303`
- Promoted task: `GOV-02` - Isolate governance-audit tests from the live receipt audit (`PROMOTED`)
- Next proposal: `L3-01` (`PROPOSED`, unchanged)
- Authority source: `projects/score2gp/ORCHESTRATION_STATE.json` (authority revision 44 -> 45)
- Governance publisher: `tticomgov-code` from `worktrees/gov`

## Outcome and scope

- Reconciled `GOV-01` into `completed_tasks` with `reconcile_task`, from a `snapshot` of PR 691.
- **Delegated merge execution enabled**, as GOV-01's acceptance assigns to governance at reconciliation:
  - `roles.merge_controller.github_logins`: [] -> [`tticom-codex`, `tticomgov-code`].
    `role_policy` now classes only `tticom-automation` as never-merge among the agent logins.
  - `merge_policy.required_checks_by_repository`: `tticom/score2gp` -> [`test`];
    `tticom/score2gp-agentops` -> [`deterministic-control-plane`].
- **`merge_policy.executor_audit_since` is deferred.** Setting it makes 7 tests in
  `tests/test_governance_audit.py` fail: they run `main()` against live authority, with `gh` mocked,
  and count GitHub calls. That is GOV-01's defect, fixed by GOV-02.
  - When GOV-02 merges, governance sets the cut-off to **`2026-09-24T18:16:59Z`** (one second after
    #691 merged). Because the value is a date filter, the audit then covers every delegated merge
    since GOV-01 merged, so none escapes the receipt audit.
  - #685 (merged by tticom-codex before the executor existed) stays outside the window by design.
- **GOV-02 promoted ahead of L3-01** at the maintainer's direction on 2026-09-24. L3-01 returns to
  `next_task_proposal` unchanged, and its prompt is unchanged.
- Changed paths: `ORCHESTRATION_STATE.json`, `ACTIVE_TASK.md`,
  `prompts/next/gov-02-receipt-audit-test-isolation.md` (new), this handoff.
- Residual risk, accepted by the maintainer on 2026-09-24: delegated credentials can technically merge
  outside the executor or forge a receipt. Until GOV-02's reconciliation sets the cut-off, the
  receipt audit is inactive. It covers this interval retroactively once set.

## Notes carried forward for L3-01

- H1 conflicts with `tests/test_barline_recovery.py::test_notation_to_tab_barline_inheritance`.
  Record that as H1's counterexample.
- H2 evidence from a read-only probe of product `main` at `71535f3`, Lesson 3 page 1 system 1:
  - Each of the 4 wrongly inherited partner candidates has a small filled closed path (a notehead of
    about one notation staff space) touching one end.
  - The genuine partner barline has none, and neither does the synthetic recovery test.
- Local test runs on this Windows host need `python -m pytest --capture=sys`. Lesson 3 private
  fixtures resolve through `worktrees/auto/score2gp-private-fixtures`.

## Next authorised action

- Action: `tticom-automation` implements GOV-02 on `feat/gov-02-receipt-audit-test-isolation`.
  A non-author reviewer publishes an exact-head APPROVE or REQUEST_CHANGES.
- Merge: once this PR is merged, `tticom-codex` or `tticomgov-code` merges approved PRs they did not
  author through `python scripts/score2gp_orca_control.py merge --repository <r> --pull-request <n>`.
  The maintainer may also merge.
- Then governance reconciles GOV-02, sets `executor_audit_since` to `2026-09-24T18:16:59Z`, and promotes L3-01.
- Stop condition: any GOV-02 stop condition; the governance audit failing on `main`.
