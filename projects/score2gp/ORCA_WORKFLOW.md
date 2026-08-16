# Score2GP Orca Workflow v1

## Decision

Orca owns runtime sequencing, worktree lifecycle, bounded dispatch, handoff, and
parallelism. AgentOps remains the versioned policy and task-authority
repository. Workers do not select tasks, promote successors, interpret incident
history, or decide whether merge prerequisites are complete.

`ORCHESTRATION_STATE.json` is the authoritative migration-state document.
`scripts/score2gp_orca_control.py` is the sole operational reducer. Orca pins the
AgentOps commit, captures live GitHub facts, invokes the reducer, and dispatches
only the returned role. The generated assignment pins the task, branch, PR,
head SHA, paths, acceptance criteria, evidence, and allowed/forbidden actions.

No repository-owned `orca.yaml`, `.orca` configuration, or documented Orca
manifest schema existed at the start of this migration. V1 therefore defines a
tool-neutral JSON handoff contract instead of inventing an Orca configuration
format. The Orca `/orchestration` supervisor invokes this contract from its own
environment.

## Current-system diagnosis

The current system mixes four different concerns:

- Policy: `AGENT_CONTROL.md`, `REVIEW_RULES.md`, `PR_EVIDENCE_CONTRACT.md`,
  protected-branch rules, task prompts, and role skills.
- Orchestration: autonomous-continuation, blocker-pivot, role-transition, and
  queue-promotion rules in `AGENT_CONTROL.md`, project-director skills,
  `ACTIVE_TASK.md`, `APPROVED_TASK_QUEUE.md`, and `go/got` prompts.
- Identity enforcement: Linux user/home checks, per-user clones and GitHub CLI
  stores, Git author checks, dispatcher role selection, GitHub permissions, and
  rulesets.
- Evidence/quality gates: exact-head formal reviews, handback receipts, review
  evidence gate, real-source requirements, CI, unresolved-thread rules, and
  governance review.

The Agy/Codex disagreement was possible for three exact reasons. First, the
incident is a prose heading with no stable lifecycle record connecting its
opening and resolution. Second, agents can read different Git revisions: the
observed local AgentOps checkout declared Task 103 `PROMOTED`, while
`origin/main` declared Task 108 `IN_PROGRESS`. Third, `score2gp_go_bootstrap.py`,
`score2gp_got_bootstrap.py`, `score2gp_bootstrap.py`, the audit script, prompts,
and agent skills each perform overlapping but non-identical reductions of prose
and live GitHub state. M5 being `MERGED` is unrelated to the incident's formal
resolution, but prose inference allowed it to be treated as closure. Conversely,
the still-present incident heading could be treated as an eternal block.

## Responsibility split

| Concern | Owner |
|---|---|
| Product direction, task authorisation, roles, incident declarations, evidence policy | Versioned AgentOps policy |
| State reduction (`BLOCKED`, `READY`, `RUNNING`, `REVIEW_REQUIRED`, `GOVERNANCE_REQUIRED`, `COMPLETE`) | Deterministic control CLI |
| Worktrees, sequencing, parallel research, worker lifecycle, handoffs | Orca supervisor |
| Implementation or evidence collection | Bounded worker |
| Semantic acceptance and adversarial disconfirmation | Independent reviewer/governor |
| Mechanical merge eligibility and exact-head merge | Dedicated non-LLM merge controller |
| Main protection, approval enforcement, bypass restrictions | GitHub rulesets/permissions |

Orca is not a policy authority and cannot override a `BLOCKED` result. Workers
consume assignments; they do not call the resolver to obtain broader work.

## Incident lifecycle

Every incident has a stable ID and exactly one explicit status. `OPEN` and
`BLOCKING` deny all dispatch and merge checks. `RESOLVED` requires a
`resolved_by` governance artifact. Milestones, prose interpretation, elapsed
time, and later task status cannot implicitly close an incident.

## Identity model

Separate Linux users are no longer the primary security boundary. Orca may run
worktrees under the `tticom` WSL user, but each remote action must use a scoped
GitHub identity authorized for the assignment role. Git author identity is
provenance, not authorization. Reviewers remain metadata-only. Implementation,
review, governance, and supervision roles all prohibit merge.

The merge-controller login is deliberately empty in v1. No merge can pass
until a GitHub App or similarly non-interactive, least-privilege identity is
configured in both the policy and GitHub. The controller must have no product
editing or review authority and must never use admin bypass.

## Orca invocation contract

1. Synchronize a clean AgentOps read worktree to `origin/main` and record its SHA.
2. Capture live PR/check/review/thread/ruleset facts as JSON.
3. Run `python3 scripts/score2gp_orca_control.py resolve --live <facts.json>`.
4. Stop on `BLOCKED` or an unknown/error result.
5. For a dispatchable result, create the role-specific worktree and run
   `assign` with the worker's authenticated GitHub login.
6. Give the worker only the emitted assignment plus the referenced prompt.
7. On return, recapture live facts; never reuse a prior resolution.
8. Run independent review/governance as returned by the resolver.
9. Run `merge-check` immediately before integration. V1 is dry-run only.

Example implementation dispatch after Orca has selected the implementation
credential profile:

```bash
GH_CONFIG_DIR=<implementation-credential-dir> \
python3 scripts/score2gp_dispatch.py \
  --agentops . --product ../score2gp \
  --orca-role implementation \
  --live <ignored-live-json> \
  --github-login tticom-automation --json
```

`--github-login` is an expected value, not a role claim: the dispatcher queries
`gh api user` and rejects a mismatch. The AgentOps worktree must be clean, so
the emitted `agentops_sha` always identifies the exact committed authority.

For `got`, use the same dispatcher with the role returned by `resolve`:
`reviewer` under the reviewer credential or `governance` under the governance
credential. A caller cannot request a different role from the one resolved.

Orca may parallelize read-only investigation when assignments do not overlap.
Only one implementation owner may write a task branch. Reviewer worktrees are
detached at the exact PR head and remain read-only.

## Compatibility and migration

The existing `ACTIVE_TASK.md`, queues, `go/got`, and bootstrap scripts remain
active during v1. They are compatibility inputs and audit evidence, not a
second Orca state engine. Every change to task authority must update both
`ACTIVE_TASK.md` and `ORCHESTRATION_STATE.json`; CI must reject divergence.

After shadow runs prove equivalence, replace `ACTIVE_TASK.md` with a generated
human view, retire autonomous continuation/pivot rules, and reduce `go/got` to
thin adapters that call the same resolver. Queue files become planning records,
not executable dispatch inputs. The old bootstrap state reducers become
obsolete only after this cutover.

### Migration steps and acceptance

1. Shadow mode (this change): check the JSON authority against
   `ACTIVE_TASK.md`, resolve state, emit assignments, and deny merges. Legacy
   dispatch remains enforceable. Acceptance: resolver, incident, identity,
   bounded-assignment, and stale-SHA tests pass.
2. Orca pilot: use the resolver for one bounded review-fix cycle, record
   resolver inputs/outputs and worktree ownership, and compare every result with
   legacy `go/got`. Any disagreement is a stop, not a choice between engines.
3. CI authority gate: run alignment and schema tests on every AgentOps PR; add a
   live ruleset audit that verifies automation cannot bypass either main.
4. State cutover: make the JSON task/incident model the only authored authority;
   generate `ACTIVE_TASK.md` as a human view. Convert queues to non-executable
   planning data. Make `go/got` thin compatibility wrappers around this CLI.
5. Merge-controller pilot: install a least-privilege GitHub App, add its login
   to policy, give it merge-only workflow permission without bypass, require a
   signed/immutable governance decision artifact, and test stale-head races.
6. Retirement: after successful shadow/pilot evidence, remove duplicated state
   resolution from the old bootstraps and autonomous dispatcher prose.

### Components scheduled for retirement

- State-reduction branches inside `score2gp_go_bootstrap.py`,
  `score2gp_got_bootstrap.py`, and `score2gp_bootstrap.py`.
- Worker-side continuation, pivot, queue selection, and task-promotion clauses
  in `AGENT_CONTROL.md` and the project-director skill.
- Hand-authored `ACTIVE_TASK.md` and prose status vocabulary after it becomes a
  generated view.
- Role selection based solely on Linux username in `score2gp_dispatch.py`.

The audit, evidence gate, review publisher, and handback publisher are not
obsolete; they should become libraries or commands called by the supervisor and
merge controller.

### Migration risks

- Dual-write drift during compatibility mode. The alignment gate fails closed,
  but every promotion must update both representations until cutover.
- GitHub API snapshots can become stale immediately. Every assignment and merge
  decision must pin a head SHA and be recomputed after any remote mutation.
- A JSON file alone is not authorization if an unprotected governance main can
  be changed. AgentOps currently has an active ruleset, but maintainer-role
  bypass still exists; production merge automation should require a non-bypass
  controller and preferably signed governance decisions.
- A shared OS user weakens filesystem confidentiality between agents. This is
  acceptable only if worktrees are bounded and remote credentials are scoped;
  high-sensitivity credentials may still justify isolated homes or OS users.
- Orca supervisor prompts are not a security boundary. All block/identity/merge
  decisions must remain code and hosting-service enforced.
- Parallel work can create overlapping evidence or branch ownership. Orca must
  allow parallel read-only investigation but serialize writes to a task branch.
- GitHub approvals alone do not prove semantic correctness. Independent review,
  real-source evidence, negative controls, and the evidence ledger remain
  mandatory policy gates.

## PR #441 status

At migration creation, PR #441 is open at
`6fd4d5724aff7bded1155c08984f2a0853d10895`, CI is green, and the current-head
governance review requests changes. The correct operational state is `RUNNING`
with dispatch restricted to the implementation role. Merge remains denied.
