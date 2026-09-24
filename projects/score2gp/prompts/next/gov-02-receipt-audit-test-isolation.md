# GOV-02 — Isolate governance-audit tests from the live receipt audit

- **Status**: PROMOTED (the `task` in `ORCHESTRATION_STATE.json`, authority revision 45). Executable by the implementation role.
- **Repository**: `tticom/score2gp-agentops`
- **Branch**: `feat/gov-02-receipt-audit-test-isolation`
- **Owner Role**: `implementation`
- **Reviewer Role**: `reviewer`
- **Delivery Action**: `pull_request`
- **Prerequisites**: `GOV-01`

## 1. Authority

GOV-01's reconciliation found this defect on 2026-09-24. With `merge_policy.executor_audit_since`
set in the live authority, 7 tests in `tests/test_governance_audit.py` fail, including
`test_open_matching_pr_passes_audit` and `test_non_active_task_no_github_lookup`. Those tests run
`score2gp_governance_audit.main()` against the repository's live `ORCHESTRATION_STATE.json`, with
`gh` mocked, and assert an exact number of GitHub calls. GOV-01's step 6 (the delegated-merge
receipt audit) then activates and makes additional `gh` calls. The maintainer directed that this fix
goes before L3-01. Governance deferred `executor_audit_since` until this task merges.

## 2. Objective

Make the `main()`-level governance-audit tests independent of whether live authority enables the
receipt audit, without changing the audit's behaviour.

- Tests that exercise other audit steps through `main()` must control step 6 explicitly, for example
  by patching `audit_delegated_merges` or supplying a fixture authority. They must not depend on
  live `merge_policy` or `roles`.
- Keep step 6 covered: at least one `main()`-level test shows a receipt-audit violation makes the
  audit fail, and one shows the step is skipped when `executor_audit_since` is unset.
- Do not change the receipt audit's semantics, the executor, or any merge rule.

## 3. Allowed Paths and Acceptance

As listed for `GOV-02` in `ORCHESTRATION_STATE.json` (authoritative). Acceptance includes running the
full suite against a temporary copy of the authority with `executor_audit_since` and
`merge_controller` set, so the defect is proven fixed before governance sets them live.
