# WIN-04 — Post-migration governance hygiene and merge-rule alignment

- **Status**: PROMOTED (the `task` in `ORCHESTRATION_STATE.json`, authority revision 42). Executable by the implementation role.
- **Repository**: `tticom/score2gp-agentops`
- **Branch**: `feat/win-04-post-migration-governance-hygiene`
- **Owner Role**: `implementation`
- **Reviewer Role**: `reviewer`
- **Delivery Action**: `pull_request`
- **Prerequisites**: `WIN-03`

## 1. Authority

- These are non-blocking review findings carried over from WIN-01 (review `5299557145`) and WIN-02 (review `5300426043`), listed in `reports/2026-09-24-win-01-win-02-out-of-policy-merges.md`.
- The maintainer's merge decision of 2026-09-24 is recorded in the same report:
  - `tticom-codex` and `tticomgov-code` may merge. `tticom-automation` may not.
  - Every task PR needs a formal APPROVE at the exact head from a non-author.
  - One approval is enough. `merge_policy.minimum_approvals` is 1, and the GitHub rulesets on both repositories require 1.
- On 2026-09-24 the maintainer ordered WIN-04 before L3-01. Governance promoted it in #687; see `handoffs/2026-09-24-win-04-reorder-promotion.md`.

## 2. Objectives

1. `docs/agy-cycle.md` documents the deleted `scripts/agy-cycle` wrapper. Replace each command with its `python scripts/agy_cycle.py …` equivalent, or delete the document if `agy_cycle.py` is no longer used.
2. `projects/score2gp/prompts/next/go-dispatch.md:23` still names `agy-skills/main` as the skills source. Point it at `agentops-claude-skills`, following `SKILLS_LOCK.md`.
3. Restate every live statement of the merge rule to match the maintainer decision, in the form the machine role policy can enforce:
   - `tticom-automation` never merges, and no identity merges in the reviewer run.
   - `tticom-codex` and `tticomgov-code` may merge only in a separate operation, only while authority lists them in `roles.merge_controller`, and only a PR with a formal APPROVE at its exact live head from a non-author reviewer.
   - The live statements are:
     - `AGENTS.md:86`
     - `CLAUDE.md:84`
     - `projects/score2gp/AGENT_CONTROL.md:186-189`, `:525` and `:531-534`
     - `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md:45-48`
     - `projects/score2gp/prompts/next/got-dispatch.md:164-165`
     - `skills/score2gp-pr-hard-review.md:67-69`
     - `skills/score2gp-task-orchestration.md:32`
     - `.agents/skills/score2gp-project-director/SKILL.md:86-89`
     - this prompt
   - Update `tests/test_dispatch_entrypoint_contract.py::test_reviewer_and_merge_role_firewalls_are_explicit`, which asserts the old wording.
   - `AGENT-RULES.md:63` ("Must never merge to main") stays, because it describes the automation role.
4. `tests/test_governance_audit.py::test_repository_tooling_is_python_only` (line 468) walks the filesystem with `rglob`, so untracked leftovers such as a local `agent-runtime/` directory make it fail. Make it check tracked files (`git ls-files`) instead. Add a negative control: a tracked `.sh` file still fails the test.
5. `tests/test_score2gp_dispatch.py::orca_checkout` (line 219) copies the repository's
   live `ORCHESTRATION_STATE.json` and `ACTIVE_TASK.md` into its fixture. As a result,
   the three `test_orca_path_*` tests fail whenever live authority has no promoted
   implementation task: on 2026-09-24, CI failed on #684 with
   `resolver requires role <none>, not implementation; state=COMPLETE`. Give those
   tests a self-contained fixture authority with a promoted implementation task. Add
   a check that they pass when the live task is `COMPLETED`.
6. `tests/test_score2gp_control_plane.py::test_role_policy_is_derived_from_authority_roles`
   asserts that `tticomgov-code` is never-merge. Make it assert only what holds whether
   `roles.merge_controller` is empty or holds [`tticom-codex`, `tticomgov-code`].

`merge_policy` and `roles.merge_controller` in `ORCHESTRATION_STATE.json` are
authority, not task scope. Governance fills `merge_controller` in a separate change after WIN-04 merges.

## 3. Allowed Paths and Acceptance

As listed for the `WIN-04` `task` in `ORCHESTRATION_STATE.json` (authoritative),
including this prompt. Historical records are not rewritten: `handoffs/`, `reports/`,
`decisions/`, `docs/cycle-preparation-history/`, programmes, and prompts for other
tasks that are not live merge-rule statements.
