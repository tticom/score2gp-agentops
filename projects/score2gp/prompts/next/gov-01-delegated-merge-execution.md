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

1. **Merge executor.** Add one, for example `score2gp_orca_control.py merge`. It captures fresh live
   state, runs `verify_merge_gate`, and only on `ALLOW` does two things:
   - posts a `score2gp/merge-gate` commit status of `success` on the exact reviewed head;
   - runs `gh pr merge --merge --match-head-commit <reviewed head>` as the authenticated merge-controller login.

   It then reads the merge back and records a receipt: a marked PR comment with the gate result,
   the head, the merge commit and the merging login. Any DENY, error, head change or bypass capability
   fails closed. It never uses `--admin`.
2. **Exclusive merge path.** A delegated login must not be able to complete a merge outside the
   executor. Two controls enforce this:
   - **Preventive.** The maintainer adds `score2gp/merge-gate` as a required status check in both
     repositories' `main` rulesets. The executor reads the live ruleset and returns `DENY`
     (`merge_gate_status_not_required`) if that requirement is missing. A direct `gh pr merge` by
     any login is then blocked by GitHub until a gate `ALLOW` has posted the status on that exact head.
     A push after the status is posted creates a new head without it.
   - **Detective.** The governance audit and the agentops CI check every PR merged into either `main`
     after GOV-01 by a login in `roles.merge_controller`. Each must have a matching executor receipt
     for the merged head. A missing or mismatched receipt fails the audit, and the task documents how
     governance records the resulting `OPEN` incident, which blocks dispatch.
3. **Per-repository required checks.** `tticom/score2gp` requires `test`;
   `tticom/score2gp-agentops` requires `deterministic-control-plane`.
4. **Governance-PR path.** Define which non-task PRs the gate may evaluate (governance promotions and
   reconciliations, architect proposals), and what stands in for the task-branch match and the
   governance GO. They must not relax the approval, check or thread requirements.
5. **`role_policy` readiness.** Make `role_policy`, its tests and the executor ready for
   `roles.merge_controller` to hold `tticom-codex` and `tticomgov-code`. **Governance** fills that
   field when it promotes or reconciles this task, and only after the maintainer confirms the
   `score2gp/merge-gate` ruleset requirement is active. The implementation PR does not edit
   `ORCHESTRATION_STATE.json`. An identity never merges a PR it authored, and never in its reviewer run.
6. **Human-only merge semantics in code and states.** These now mean "ready for the merge executor
   or the maintainer":
   - `score2gp_orchestrator.py`: the `AWAIT_HUMAN_MERGE` action and the `human_merge` lifecycle state
     (lines 22, 33, 94, 253, 356).
   - `score2gp_publish_review.py:76`: `READY_FOR_HUMAN_MERGE`.

   Either rename them (for example `READY_FOR_MERGE`, `AWAIT_MERGE`, `merge_ready`) or keep the
   identifiers and redefine them. Whichever is chosen, all producers, consumers, docs and tests change
   together in this PR, and the PR description records the choice.
7. **Restate every live human-only merge rule to the executor-only rule.** The inventory below was
   taken on 2026-09-24. Re-verify it with a repository search at the start of the task.
   - `.agents/rules/pr_standards.md:19-22`
   - `.agents/skills/score2gp-project-director/SKILL.md:40`, `:85-89`
   - `AGENTS.md:86-88`
   - `CLAUDE.md:51`, `:78`, `:84-86`
   - `README.md:160`
   - `docs/agy-cycle-v2-plan.md:86`
   - `projects/score2gp/AGENT_CONTROL.md:22`, `:186-189`, `:295`, `:404`, `:410`, `:470`, `:481-483`, `:525`, `:529-534`
   - `projects/score2gp/ORCA_WORKFLOW.md:59`, `:78-80`, `:150`
   - `projects/score2gp/SIMPLE_AGENT_PROCESS.md:13-15`, `:24`
   - `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md:24`, `:35`, `:45-48`
   - `projects/score2gp/prompts/next/got-dispatch.md:118`, `:164-165`
   - `projects/score2gp/prompts/next/go-dispatch.md:57-58`
   - `projects/score2gp/prompts/next/go-got-dispatcher.md:16`, `:26`
   - `projects/score2gp/skills/orca-supervisor/SKILL.md:48-50`
   - `projects/score2gp/skills/project-director/SKILL.md:54-63`, `:99`
   - `projects/score2gp/templates/AGENT_TASK_TEMPLATE.md:18`, `:20`, `:32`
   - `skills/score2gp-pr-hard-review.md:67-69`
   - `skills/score2gp-task-orchestration.md:5`, `:18`, `:32`
   - `skills/score2gp-project-director.md:53`
   - Tests asserting the old rules or states:
     - `tests/test_dispatch_entrypoint_contract.py::test_reviewer_and_merge_role_firewalls_are_explicit`
     - `tests/test_score2gp_control_plane.py::test_role_policy_is_derived_from_authority_roles`
     - `tests/test_score2gp_orchestrator.py:96-103`, `:331-342`
     - `tests/test_governance_audit.py:495`, `:507`
   - Out of scope, unchanged:
     - `AGENT-RULES.md:63` ("Must never merge to main"), which describes the automation role.
     - Prompts for other tasks (for example L3-00, WIN-01, ORC-04 and the 2026-07-19 teamwork prompt).
     - Plans, and the historical section of `PLANNING_DATA.md`.

## 4. Allowed paths

As listed for `GOV-01` in `ORCHESTRATION_STATE.json` (authoritative). If the repository search at the
start of the task finds a live merge rule outside those paths, stop and ask governance to widen the
scope. Do not edit outside it. Historical records are not rewritten: `handoffs/`, `reports/`,
`decisions/`, `runs/`, `programmes/`, `plans/`, prompts for other tasks, and
`docs/cycle-preparation-history/`.

## 5. Acceptance

- The executor merges only on a gate `ALLOW` computed from fresh live state. It posts
  `score2gp/merge-gate` and merges only the exact reviewed head. Tests cover every DENY reason, a head
  change between the gate and the merge, a stale review, a login outside `merge_controller`, a
  self-authored PR, bypass capability, and a ruleset that does not require `score2gp/merge-gate`.
  It never passes `--admin`.
- **Exclusive path.**
  - A test shows that a delegated login's merge without the executor is refused: `gh pr merge` fails
    because of the required `score2gp/merge-gate` status, simulated at the `gh` boundary.
  - A negative control shows the governance audit fails when a PR merged by a `merge_controller` login
    has no matching executor receipt, or a receipt for a different head.
  - Each of these tests must be shown to fail when its control is disabled.
- Each repository's required checks are evaluated correctly. An agentops PR is not denied for lacking `test`.
- The governance-PR path is explicit and tested. A non-task PR cannot use it to bypass the approval, check or thread requirements.
- After governance fills `merge_controller`, `role_policy` classes only `tticom-automation` as never-merge among the agent logins.
- Human-merge states in code are renamed or redefined consistently across every producer, consumer, doc and test.
- A repository search finds no remaining live human-only or unconditional agent merge rule. Historical records are unchanged.
- The governance audit, full `python -m pytest`, Linux CI and `git diff --check` pass.
