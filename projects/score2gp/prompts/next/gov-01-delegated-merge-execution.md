# GOV-01 — Delegated merge execution through the mechanical merge gate

- **Status**: PROPOSED. Not executable until governance promotes it.
- **Repository**: `tticom/score2gp-agentops`
- **Branch**: `feat/gov-01-delegated-merge-execution`
- **Owner Role**: `implementation`
- **Reviewer Role**: `reviewer` (use `devils-advocate-review`: this changes merge authority)
- **Delivery Action**: `pull_request`
- **Prerequisites**: `WIN-04`

## 1. Authority

The maintainer `tticom` decided on 2026-09-24 (`reports/2026-09-24-win-01-win-02-out-of-policy-merges.md`):
- `tticom-codex` and `tticomgov-code` may merge. `tticom-automation` never merges.
- Every PR needs a formal APPROVE at its exact head from a non-author reviewer.
- One approval is enough (`merge_policy.minimum_approvals: 1`, and the GitHub rulesets require 1).

On 2026-09-24 the maintainer also directed that agent merges happen **only through the mechanical
merge gate**, not by an agent's discretion, and that this is a separate task with a complete inventory
of the live human-only merge rules (#687).

## 2. Gaps in the current gate (`scripts/score2gp_orca_control.py::verify_merge_gate`)

1. It is dry-run only (`"dry_run": True`). Nothing executes an exact-head merge.
2. It evaluates only the active task PR (`branch_mismatch` otherwise). Governance PRs cannot pass it.
3. `merge_policy.required_checks` is `["test"]`, but `tticom/score2gp-agentops` CI publishes `deterministic-control-plane`.
4. `require_governance_go` needs a recorded governance `GO`, which the current flow never produces.
5. `roles.merge_controller.github_logins` is empty, so `role_policy` classes every agent as never-merge.

## 3. Objectives

1. Add a merge executor, for example `score2gp_orca_control.py merge`. It captures fresh live state,
   runs `verify_merge_gate`, and only on `ALLOW` runs `gh pr merge --merge --match-head-commit <reviewed head>`
   as the authenticated merge-controller login. It then reads the merge back and records a receipt.
   Any DENY, error, head change or bypass capability fails closed. No `--admin`.
2. Make required checks per repository (`tticom/score2gp`: `test`; `tticom/score2gp-agentops`: `deterministic-control-plane`).
3. Define the governance-PR path: which non-task PRs (governance promotions and reconciliations,
   architect proposals) the gate may evaluate, and what stands in for the task-branch match and the governance GO.
4. Make `role_policy`, its tests and the executor ready for `roles.merge_controller` to hold
   `tticom-codex` and `tticomgov-code`. **Governance** fills that field when it promotes or reconciles
   this task; the implementation PR does not edit `ORCHESTRATION_STATE.json`. An identity never
   merges a PR it authored, and never in its reviewer run.
5. Restate every live human-only merge rule to the executor-only rule. The inventory taken on 2026-09-24
   (to be re-verified with a repository search at the start of the task):
   - `.agents/rules/pr_standards.md:19-22`
   - `AGENTS.md:86-88`, `CLAUDE.md:84-86`
   - `projects/score2gp/AGENT_CONTROL.md:186-189`, `:404`, `:410`, `:470`, `:481-483`, `:525`, `:529-534`
   - `projects/score2gp/ORCA_WORKFLOW.md:59`, `:78-80`, `:150`
   - `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md:24`, `:35`, `:45-48`
   - `projects/score2gp/prompts/next/got-dispatch.md:118`, `:164-165`, `go-dispatch.md:58`, `go-got-dispatcher.md:16`
   - `projects/score2gp/skills/orca-supervisor/SKILL.md:48-50`, `projects/score2gp/skills/project-director/SKILL.md:63`
   - `skills/score2gp-pr-hard-review.md:67-69`, `skills/score2gp-task-orchestration.md:5`, `:18`, `:32`, `skills/score2gp-project-director.md:53`
   - `.agents/skills/score2gp-project-director/SKILL.md:85-89`
   - `projects/score2gp/templates/AGENT_TASK_TEMPLATE.md:18`, `:20`, `:32`
   - Tests asserting the old rules: `tests/test_dispatch_entrypoint_contract.py::test_reviewer_and_merge_role_firewalls_are_explicit` and
     `tests/test_score2gp_control_plane.py::test_role_policy_is_derived_from_authority_roles`
   - `AGENT-RULES.md:63` ("Must never merge to main") stays; it describes the automation role.

## 4. Allowed paths

As listed for `GOV-01` in `ORCHESTRATION_STATE.json` (authoritative). If the repository search at the
start of the task finds a live merge rule outside those paths, stop and ask governance to widen the
scope. Do not edit outside it. Historical records (`handoffs/`, `reports/`, `decisions/`, `runs/`,
`programmes/`, prompts for other tasks, `docs/cycle-preparation-history/`) are not rewritten.

## 5. Acceptance

- The executor merges only on gate `ALLOW`. Tests cover every DENY reason, a head change between the gate and the merge, a stale review, a login outside `merge_controller`, self-authored PRs, and bypass capability. It never passes `--admin`.
- Each repository's required checks are evaluated correctly. An agentops PR is not denied for lacking `test`.
- The governance-PR path is explicit and tested. A non-task PR cannot use it to bypass the approval or check requirements.
- After the change, `role_policy` classes only `tticom-automation` as never-merge among the agent logins.
- A repository search finds no remaining live human-only or unconditional-agent merge rule. Historical records are unchanged.
- The governance audit, full `python -m pytest`, Linux CI and `git diff --check` pass.
