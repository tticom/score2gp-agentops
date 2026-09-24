# L3-01 Promotion and Merge-Authority Alignment Handoff

## Authority

- Promoted task: `L3-01` - Paired-staff barline acceptance for the Lesson 3 first system (`PROMOTED`)
- Next proposal: `WIN-04` - Post-migration governance hygiene and merge-rule alignment (`PROPOSED`)
- Authority source: `projects/score2gp/ORCHESTRATION_STATE.json` (authority revision 40 -> 41)
- Proposal source: architect PR #685 (tticom-automation), approved by tticom-codex (review `5303729934`), merged at `79b00e3e041840e516f2d8f95fd474a4951929ab`
- Governance publisher: `tticomgov-code` from `worktrees/gov`

## Outcome and scope

- Promoted `L3-01` from `next_task_proposal` to `task`, unchanged apart from `status`.
- Moved `WIN-04` from `queued_task_proposals` to `next_task_proposal`.
- Aligned authority with the maintainer's merge decision of 2026-09-24, recorded in
  `reports/2026-09-24-win-01-win-02-out-of-policy-merges.md`:
  - `merge_policy.minimum_approvals`: 2 -> 1. This matches the GitHub rulesets on both repositories, which now require 1.
  - `roles.merge_controller.github_logins` is **not** changed here.
    `tests/test_score2gp_control_plane.py::test_role_policy_is_derived_from_authority_roles`
    reads live authority and asserts `tticomgov-code` is never-merge, so the change fails that test.
    When governance promotes WIN-04, it adds `tests/test_score2gp_control_plane.py` to WIN-04's
    allowed paths so the test asserts only `tticom-automation` never merges, and sets
    `merge_controller` to [`tticom-codex`, `tticomgov-code`] after WIN-04 merges.
- Changed paths: `ORCHESTRATION_STATE.json`, `ACTIVE_TASK.md`, this handoff.
- The live documentation merge rules (`AGENTS.md`, `CLAUDE.md`, `AGENT_CONTROL.md`) are WIN-04's scope and are not changed here.

## Notes for the L3-01 developer

- H1 as written (require a TAB-staff stroke at the same x) conflicts with the existing
  `tests/test_barline_recovery.py::test_notation_to_tab_barline_inheritance`. Its internal
  barlines cross only the notation staff, with no TAB stroke at all, and must still be inherited.
  Record that as H1's counterexample. Then take the prompt's H2 pivot (reject partner candidates
  that are note stems) unless H1 can be satisfied by a TAB-staff stroke that the TAB filter rejected.
- Local test runs on this Windows host need `python -m pytest --capture=sys`. Under the default fd
  capture, subprocess-based tests fail with `WinError 6`, an artifact of the host rather than a
  product failure. With it, product `main` at `71535f3` passes all 244 tests in
  `test_barline_recovery.py`, `test_pdf.py`, `test_native_slice_acceptance.py` and
  `test_lesson3_native_acceptance.py`.

## Next authorised action

- Action: `tticom-automation` implements L3-01 on `feat/l3-01-paired-staff-barline-acceptance`
  in `tticom/score2gp`. A non-author reviewer using `devils-advocate-review` then publishes an
  exact-head APPROVE or REQUEST_CHANGES.
- Merge after that APPROVE: the maintainer `tticom` merges, or `tticom-codex` or `tticomgov-code`
  merges under the maintainer's standing 2026-09-24 decision recorded in the report.
  - Until WIN-04 aligns `roles.merge_controller`, the machine role gate
    (`scripts/score2gp_control_plane.py::role_policy`) still classes both as never-merge and refuses
    their merges.
  - An agent merge therefore rests on the maintainer's recorded decision, not on that gate. The
    agent must cite the report and the exact reviewed head when it merges.
- Stop condition: any L3-01 stop condition in its prompt; the governance audit failing on `main`.
