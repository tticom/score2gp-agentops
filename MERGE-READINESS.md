# MERGE-READINESS: what `main` must look like for `slim-governance` to merge

Status: **investigation record and plan for later. Nothing here is to be actioned now.**
Written 2026-10-01 against `origin/main` of `tticom/score2gp-agentops` at `e9a5615`
(PR #750) and `slim-governance` at `7c05d7f`. Companion for the skills repository:
[`agentops-claude-skills` `MERGE-READINESS.md`](https://github.com/tticom/agentops-claude-skills/blob/slim-governance/MERGE-READINESS.md).

This document is awareness and conflict mitigation. The chop and the merge happen only
after the experiment on `slim-governance` has shown the lean flow is worth adopting. No
decision is asked of the maintainer here; where a default is recorded it can be revisited
with evidence at that time. Rules this plan follows:

- Same repositories, same history. The branch is cut from `main`, chopped, `slim-governance`
  is merged into it, the result is proved, and only then merged into `main`.
- The old framework keeps running on `main` in parallel, and agents on it keep starting
  tasks and know nothing about the experiment. Nothing here assumes a drain or a pause.
  Section 8 shows how to cut safely whenever the time comes.
- The fresh-history private repository in `CUTOVER.md` was a misreading: a fresh repository
  is only for the Rust component (`score2gp-vector-parser`), a separate evidence-gated
  decision. `CUTOVER.md` is therefore superseded for this repository (section 9) and its
  steps are mapped in section 10.
- Trimming public history, making repositories private and retiring accounts are later,
  separate questions and are not part of this merge.

## 0. What was verified, and how

Everything marked "verified" was run in a throwaway rehearsal clone (outside every
repository and worktree, nothing pushed, `main` untouched) that fetched `origin/main` and
`slim-governance`, performed the chop on a scratch branch, and ran the test suite after
every step. Python 3.14 with pytest 9.0.3 on Windows, plus Python 3.12 on Linux (a
`python:3.12-slim` container, the CI version). Not verified: anything needing GitHub
write access, the private fixtures, or a live agent run (section 11).

| Fact | Result |
|---|---|
| Suite on `origin/main` (Windows) | 559 passed, 1 skipped (symlink privilege). Matches PR #749's "559 passed, 1 skipped". |
| `slim-governance` merged with current `main` | clean, no conflicts; suite 599 passed, 2 skipped on the merged tree (559 old + 40 lean). Slim touches `main` files in exactly one place: `tests/test_single_backlog.py` (+3 lines, exemption `f`). |
| Old governance audit on merged tree | PASS (offline mode). The lean files do not trip the old audit. |
| Final chopped tree, Windows | 39 passed, 1 skipped (POSIX executable-bit test); `repo_scan.py` 0 findings; 38 tracked files (from 772). |
| Final chopped tree, Linux Python 3.12 | 40 passed, 0 skipped; `repo_scan.py` 0 findings; `git diff --check` clean. |
| Hook in the chopped tree | `install_hooks.py` installed and `--check` OK in a scratch clone with a bare scratch remote; `git push origin <branch>:main` refused by the hook; `task/demo` accepted. |
| Skills repo chopped tree | 196 passed, 1 skipped; `validate_skills.py` OK for 6 skills (details in the companion). |

Test-running note for this machine: with the harness's inherited standard input, pytest
runs fail with `WinError 6: The handle is invalid` in every test that spawns `git` or a
script (12 spurious failures on `main`). Running with `-s` and standard input redirected
from a real file (not `/dev/null`) gives the true result above. Do not read a red run on
this machine as real until that is ruled out.

## 1. What `main` must look like (the end state)

After the merge, the tracked tree of `score2gp-agentops` is about 40 files (from 772; the
rehearsal tree had 38, which includes `SLIM-PROPOSAL.md` and `CUTOVER.md` but not this document):

```text
.github/PULL_REQUEST_TEMPLATE.md   (from lean/PULL_REQUEST_TEMPLATE.md)
.github/workflows/ci.yml           (from lean/ci-slim.yml; replaces governance-control-plane.yml)
.gitignore  LICENSE
CLAUDE.md  AGENTS.md  TASKS.md     (from lean/; replace the old root CLAUDE.md and AGENTS.md)
README.md                          (rewritten)
docs/CONTEXT.md  docs/decisions.md  docs/rejected-claims.md  docs/review-rules.md
docs/acceptance-targets.md  docs/benchmark-ladder.md
docs/requirements/  (README + REQ-0001..0005)
docs/incidents/     (5 incident reports)
lean/               (scripts/, hooks/, tests/, reports/TEMPLATE.md, README.md; guidance copies removed after promotion)
SLIM-PROPOSAL.md  MERGE-READINESS.md  CUTOVER.md -> MIGRATION.md (reworked, section 9)
```

There is no `scripts/`, `tests/`, `.agents/`, `skills/`, `tasks/`, `projects/`, no
`ORCHESTRATION_STATE.json`, no `ACTIVE_TASK.md`, no dispatcher. CI is the lean `gate`
job: `repo_scan.py`, `python -m pytest -q -ra`, `git diff --check`.

## 2. Classification of everything on `origin/main` (772 files)

Every path is covered by exactly one rule (verified by script: 772 of 772, 0 unclassified).

| Rule | Paths | Files | Disposition | Target or superseded by |
|---|---|---:|---|---|
| K1 | `LICENSE`, `.gitignore` | 2 | keep as-is | |
| M1 | `projects/score2gp/requirements/` (README, REQ-0001..0005) | 6 | move | `docs/requirements/` |
| M2 | `projects/score2gp/REJECTED_CLAIMS.md` | 1 | move | `docs/rejected-claims.md` |
| M3 | `projects/score2gp/ARCHITECTURE_DECISIONS.md` | 1 | move | `docs/decisions.md` |
| M4 | `projects/score2gp/CONTEXT.md` | 1 | move | `docs/CONTEXT.md` |
| M5 | `projects/score2gp/REVIEW_RULES.md` | 1 | move | `docs/review-rules.md` (see gap G1) |
| M6 | five incident reports in `projects/score2gp/reports/` (2026-07-20 x2, 2026-07-21 x2, 2026-09-24) | 5 | move | `docs/incidents/` |
| M7 | `projects/score2gp/ACCEPTANCE_TARGETS.md`, `BENCHMARK_LADDER.md` | 2 | move (default keep: policy, not run output) | `docs/acceptance-targets.md`, `docs/benchmark-ladder.md` |
| R1 | `README.md`, `CLAUDE.md`, `AGENTS.md` | 3 | needs rewrite | root `CLAUDE.md`/`AGENTS.md` become the `lean/` versions; `README.md` rewritten (it documents bootstrap, roles, authority) |
| D0 | `.github/workflows/governance-control-plane.yml` | 1 | delete | `lean/ci-slim.yml` promoted to `.github/workflows/ci.yml` |
| D1 | `scripts/` (18 files, 4,836 lines) | 18 | delete | see 2.1 |
| D2 | `tests/` (16 files, 6,385 lines incl. `conftest.py`) | 16 | delete | see 2.2 |
| D3 | `projects/score2gp/{runs,prompts,decisions,reviews,research,handoffs,archive,audits,plans,templates,skills}/` | 618 | delete | per-task paperwork and role skills; not versioned under the decided rule. Evidence that led to a decision is condensed later into `lean/reports/TEMPLATE.md` form, default none |
| D4 | rest of `projects/score2gp/reports/` | 47 | delete | same rule as D3 |
| D5 | `projects/prompts/` (5), `.agents/` (11), `skills/` (5 flat role skills), `tasks/pdf-to-gp-smoke-v1/` (6), `docs/cycle-preparation-history/` (2), `AGENT-RULES.md` | 30 | delete | role prompts, agent JSON, retired-harness skills, a smoke task, history; lean `CLAUDE.md` replaces the rules (gap G2 for two rule files) |
| D6 | authority and machinery in `projects/score2gp/`: `ORCHESTRATION_STATE.json`, `ACTIVE_TASK.md`, `REVIEWER_SCORECARD.json`, `AGENT_CONTROL.md`, `AGENT_PR_READINESS.md`, `ORCA_WORKFLOW.md`, `PR_EVIDENCE_CONTRACT.md`, `PR_REVIEW_TEMPLATE.md`, `REQUIREMENT_PROMPTING_CONTRACT.md`, `REVIEW_PROMPT_TEMPLATE.md`, `SIMPLE_AGENT_PROCESS.md`, `SKILLS_LOCK.md`, `TASK_RECORDING_CONVENTION.md`, `WORKFLOW_SKILLS_PROFILE.md`, `IMPLEMENTATION_PROMPT_TEMPLATE.md`, `ACTIVE_PLAN.md` | 16 | delete | `TASKS.md`; seeded once (appendix C) |
| D7 | `projects/score2gp/{README,EVIDENCE_REGISTER,MAJOR_TRIADS_BENCHMARK,RESEARCH_POST_193_DIAGNOSTICS_BOUNDARY}.md` | 4 | delete (default: not carried; recoverable from history) | |

Total: 2 keep, 17 move, 3 rewrite, 750 delete (2 + 17 + 3 + 750 = 772).

### 2.1 Scripts (`scripts/`, 18 files)

All delete. None is called by the product repository or its CI (section 5.1).

| Script | Lines | What it does | Lean equivalent |
|---|---:|---|---|
| `score2gp_dispatch.py` | 315 | `go`/`got` router; picks role from `gh api user`, binds to workspace | `TASKS.md` + `CLAUDE.md` author flow |
| `score2gp_go_bootstrap.py`, `score2gp_got_bootstrap.py` | 148, 213 | role bootstraps called by the router | none needed |
| `score2gp_bootstrap.py`, `bootstrap.py`, `link_session.py` | 14, 133, 101 | legacy wrapper; agy `define_subagent` loader; per-branch run directory | none (agy retired; run records not versioned) |
| `score2gp_orca_control.py` | 1,460 | authority validation, ready frontier, assignments, merge-receipt audit | `TASKS.md` |
| `score2gp_orchestrator.py` | 599 | renders `ACTIVE_TASK.md` from the authority | none |
| `score2gp_control_plane.py` | 283 | `switch main; merge --ff-only` of three repos, SKILLS_LOCK pin, links pinned skills into `~/.agents/skills` | none: skills are copied (companion doc) |
| `score2gp_governance_audit.py` | 409 | tracked-file bans, policy mentions, ACTIVE_TASK staleness, run-record provenance, delegated-merge receipts | `lean/scripts/repo_scan.py` covers the file-type and path part only |
| `score2gp_publish_handback.py`, `score2gp_publish_review.py`, `score2gp_review_evidence_gate.py`, `score2gp_pr_review_state.py` | 223, 263, 165, 87 | handback and formal-review publication machinery | `review` skill (advisory PR comment, `verify_review_head.py`) |
| `verify_identity.py` | 136 | role/login/workspace identity gate | `safe-git` skill (`safe_git_check.py`) + pre-push hook |
| `score2gp_agent_workspace_cleanup.py` | 145 | stale review-worktree cleanup | `workspace-cleanup` skill |
| `score2gp_task_status.py` | 17 | status vocabulary | none |
| `pr_body.py` | 125 | PR body generator | `.github/PULL_REQUEST_TEMPLATE.md` |

Import graph (why order matters): `dispatch` -> `control_plane`, `verify_identity`,
`orca_control`; `orca_control` -> `orchestrator`, `verify_identity`; `orchestrator` ->
`orca_control` (lazy); `governance_audit` -> `orchestrator`, `task_status`, `orca_control`;
`got_bootstrap` -> `go_bootstrap`; `publish_review` -> `pr_review_state`,
`review_evidence_gate`. `publish_handback`, `agent_workspace_cleanup`, `pr_body`,
`link_session`, `bootstrap` are leaves.

### 2.2 Tests (`tests/`, 16 files)

All delete, each with its subject. Tests that read documents or scan the whole tree are
the ones that block a partial chop (section 5.2).

| Test | Subject | Reads documents / tree? |
|---|---|---|
| `test_single_backlog.py` (683 on `main`; 686 on slim) | authority backlog grammar | **yes: every `git ls-files` text file; verbatim ledger of reviewed mentions** |
| `test_governance_audit.py` (1,072) | audit script, python-only tooling, doc contents | **yes: `git ls-files`, AGENT_CONTROL, REVIEW_RULES, prompts, skills, agent JSON** |
| `test_dispatch_entrypoint_contract.py` (117) | dispatcher entrypoint docs | **yes: `AGENTS.md`, `CLAUDE.md`, AGENT_CONTROL, SKILLS_LOCK, prompts** |
| `test_cp_13_codex_author_lane.py` (639) | CP-13 author lane | yes: `prompts/next/cp-13-*.md` |
| `test_score2gp_orca_control.py` (1,684), `test_score2gp_orchestrator.py` (401), `test_score2gp_dispatch.py` (473), `test_score2gp_control_plane.py` (307) | machinery | authority file |
| `test_legacy_wrappers.py` (108), `test_verify_identity.py` (148) | wrappers, identity | no |
| `test_score2gp_publish_handback.py`, `_publish_review.py`, `_pr_review_state.py`, `_agent_workspace_cleanup.py`, `test_pr_body.py` | leaves | no |
| `conftest.py` | noexec temp-dir guard for executable test doubles | lean tests do not need it (verified green without it) |

### 2.3 Workflow and CI jobs

| Today | After | Notes |
|---|---|---|
| `governance-control-plane.yml`, job `deterministic-control-plane`: `json.tool` on the authority, `py_compile` of `orca_control` and `dispatch`, `pytest -q`, `git diff --check`; on every PR and push to `main` | `ci.yml`, job `gate`: `lean/scripts/repo_scan.py`, `pytest -q -ra`, `git diff --check` | The old workflow turns red the moment the authority or either script is removed, so the workflow swap must be in the same commit as step C4 (section 7). No ruleset requires a status check (see 5.5), so the rename blocks nothing at GitHub; the old authority's `merge_policy` names `deterministic-control-plane`, but it is deleted with the authority. |

## 3. Why the chop cannot be done in arbitrary order

Verified in the rehearsal:

1. Deleting any file that has an entry in `test_single_backlog.py`'s reviewed-mentions ledger,
   or adding a file with a "backlog/queue/task list" line that is not in the ledger, turns
   that test red. The test must therefore go before or with the documents it polices.
2. The test imports `orca_control`, so it must go before `orca_control`. And
   `orca_control` is imported by the dispatcher chain, so the chain goes first.
3. If the chop deletes every old test before `slim-governance` is merged, the tree has
   **zero tests** and `pytest` exits 5 ("no tests ran"): CI is red in that interval. Merge
   `slim-governance` before the last old test is removed.
4. Promoting `lean/` guidance files to the root by moving them breaks the lean guidance
   test (section 9), and later edits to the `lean/` originals then conflict (section 6).

## 4. Skills repository (summary)

Detailed in the companion document. In short: the 12 skills and four tests that police
them (`test_skill_distribution`, `test_migration_inventory`, `test_reviewer_skill_contracts`,
plus `docs/MIGRATION_INVENTORY.md`) are deleted; `lean/skills/*` is promoted to
`skills/*`; the README skill index is rewritten. Verified: 196 passed, 1 skipped;
`validate_skills.py` OK. The skills repo can be cut independently of this one because the
live control plane pins skills by commit SHA (`SKILLS_LOCK.md`), not by branch tip.

## 5. Cross-dependencies that break if removed, and how each is resolved

### 5.1 Product repository (`tticom/score2gp`) and its CI

Checked at `origin/main` of the product repo.

| Dependency | Finding | Resolution |
|---|---|---|
| Product CI (`pylint.yml`, `raster-gate-advisory.yml`) and product scripts (`agent_verify.py`, `artifact_audit.py`, `pr_body.py`, ...) | Nothing calls into agentops code. No non-Markdown product file mentions agentops, the authority or the dispatcher. | None needed. The product's own `scripts/pr_body.py` is a different file from `scripts/pr_body.py` here. |
| Product `CLAUDE.md` / `AGENTS.md` | Tell agents to read `../score2gp-agentops/projects/score2gp/{AGENT_CONTROL,ACTIVE_TASK,TASK_RECORDING_CONVENTION}.md`, stop if `ACTIVE_TASK.md` says `NO_ACTIVE_TASK_APPROVED`, route `go`/`next` through `scripts/score2gp_dispatch.py`, and record results in agentops | **Needs rewrite in a product PR that lands with the cut** (backlog item CP-04 already names this). After the cut those files are gone, so an old-framework agent fails closed (it cannot read them), which is the safe failure but a noisy one. Replace by a short pointer to the lean `CLAUDE.md`. |
| Product `docs/agentops.md` | Links `REVIEW_RULES.md` at agentops `main` and the authority files | Rewrite in the same product PR; keep the link target alive as `docs/review-rules.md` if the link is kept |
| Product `HANDOFF.md` | pointer file | rewrite or delete in the same PR |
| `real_fixture_check.py` (lean) | Default steps call product `scripts/private_e2e_smoke.py` and `scripts/private_gp_quality_audit.py` and read `work/.../*.json` | Both scripts exist on product `main` today. If they are renamed, pass `--config`. |

### 5.2 Tests and tools that scan tracked files

| Item | Behaviour | Resolution |
|---|---|---|
| `tests/test_single_backlog.py` | Reads every tracked text file (`git ls-files -z`); closed-world ledger of mentions; slim already adds exemption `f` for `lean/`, `SLIM-PROPOSAL.md`, `CUTOVER.md` | Deleted with the authority (step C4). **This document is a new file with "backlog" wording**: `MERGE-READINESS.md` is added to exemption `f` on this branch so the slim suite stays green until the test is deleted. |
| `tests/test_governance_audit.py::test_repository_tooling_is_python_only` | Fails if any tracked `*.sh`/`*.ps1` or retired path exists. `lean/hooks/pre-push` is a shell script with no extension, so it passes (verified on the merged tree). | Deleted with the audit (C4). Note for later: a lean test of "no shell tooling" would have to allow the hook. |
| `scripts/score2gp_governance_audit.py` (offline mode passes on slim) | Run by the `got` bootstrap, not by CI | Deleted (C4); `repo_scan.py` is the CI-side replacement for the file-type, size, path and credential rules |
| `lean/scripts/repo_scan.py` | Flags absolute local paths, secrets, forbidden extensions, over 1 MB; allow-list cannot waive secrets or paths | On the chopped tree it reports 0 findings, but **on `slim-governance` itself it reports `CUTOVER.md:74`** (a `drive:\Users\...` example); it reports 289 findings on unchopped `main` (all of rule `local-path`). Fix is in section 9. This document avoids absolute paths for the same reason. |
| `lean/tests/test_lean_guidance_paths.py` | Reads `lean/CLAUDE.md`, `AGENTS.md`, `README.md`, `TASKS.md` and `CUTOVER.md` | Fails once guidance is moved to the root (verified). Rewrite, section 9. |

### 5.3 Launchers (`<workspace>/launchers`, not touched)

These are outside the repositories. They keep working only while `main` is the old
framework. Per-script dependencies on agentops:

| Launcher | Depends on | After the cut |
|---|---|---|
| `codex_author.sh` | `git checkout main && git pull --ff-only` in the codex agentops clone, then `scripts/score2gp_dispatch.py`; `projects/score2gp/PR_EVIDENCE_CONTRACT.md`; `~/.claude/skills/publish-pr-handback/scripts/publish_handback.py` | breaks (dispatcher gone) |
| `codex_reviews2.sh`, `claude_reviews.sh`, `gov_claude_review.sh` | `score2gp_dispatch.py --review-repo/--review-pr`; `SKILLS_LOCK.md` pin parsed with grep; `projects/score2gp/REVIEW_RULES.md` overlay; a detached worktree of the skills pin | break |
| `gov_open_pr.sh` | `publish-pr-handback` skill script | breaks if the installed skill is removed |
| `as_identity.sh`, `review_with_fallback.sh` | `worktrees/<id>/score2gp-agentops` layout | unaffected by content |
| `queue_cfw.py`, `reconcile_promote.py`, `fix*.py`, `memrun.py` | edit `ORCHESTRATION_STATE.json` / `ACTIVE_TASK.md` and `prompts/next/*` | break (one-off governance scripts) |
| `launchers/prompts/*` | per-task prompts and notes | inert files |

Resolution: the old framework is not supposed to run after the cut; the launchers are
retired by being moved aside (not deleted) when the maintainer decides, per `CUTOVER.md`
step 13. Until then, **do not let the three identity clones pull the chopped `main`**: the
control plane and `codex_author.sh` both sync `main` with a fast-forward. If an old-framework
session must still run after the merge, pin its clone to the freeze tag
(`git switch --detach pre-lean-merge`). The launchers themselves were not modified in this
investigation.

### 5.4 Installed skills and the dispatcher

| Item | Finding | Resolution |
|---|---|---|
| Skills under `~/.claude/skills` | Twelve real directories (copies, not links), installed 2026-09-20/21 and **older than the pin** (`code-review` differs from the skills `main` in 8 files; four others differ by one file each) | Copies are independent of repository branches, so chopping the repositories changes nothing for them. After the cut: copy the six lean skills in, and move the four retired ones (`dispatch-task`, `governance-author`, `governed-development-loop`, `publish-pr-handback`) plus the merged-away ones aside (to a `skills-retired` folder, not deleted). `dispatch-task` fails closed by itself without a dispatch config (`STOP_NO_CONFIG`); the others would still instruct an agent to publish handbacks. |
| `~/.agents/skills` (control plane activation target) | does not exist on this machine | nothing to do |
| `SKILLS_LOCK.md` pin `c51d446` | `control_plane` requires the pin to be an ancestor of skills `origin/main` | Holds after any merge-commit or chop of the skills repo (history is kept). A squash that replaced the history would not be safe. Use a merge commit. |
| `go` / `got` | `CLAUDE.md`/`AGENTS.md` mandate `score2gp_dispatch.py` as first action | Replaced by the lean `CLAUDE.md`. Until the cut, nothing changes. |
| CP-10 and the other `CP-*` items | `CP-10` (decode `gh` output as UTF-8 in `orca_control.py`) edits a script this migration deletes. Open `CP-*` items against agentops (07, 08, 11, 12, 14, 15, 16, 18, 19 and GOV-04, GOV-06) all concern the machinery. | If any lands on `main` before the cut it conflicts as modify/delete and delete wins (section 6). They are not carried into `TASKS.md`. Items the migration itself delivers: CP-01 (record cleanup), CP-02 (skills consolidation), CP-09 (retire agy), CP-04 (product AI artifacts, partly). Carry: `CP-06` (tests writing into the private corpus; product, `risky`). |

### 5.5 GitHub-side

| Item | Finding | Resolution |
|---|---|---|
| Ruleset `Main_Protect` on all three repos | Targets the default branch: no deletion, no non-fast-forward, **PR with 1 approving review, review-thread resolution required, stale approvals dismissed on push, Copilot review on drafts**, merge/squash/rebase all allowed, bypass for the Admin role. **No required status checks.** | The cut PR needs one approval from someone other than its author, or the maintainer's admin bypass. Do not push after the approval (it is dismissed). Resolve any Copilot threads first. Keep an approver account usable until the PR merges. |
| `merge_policy` inside the authority | `required_checks_by_repository` names `deterministic-control-plane` for agentops; `merge_controller` role (`tticom-codex`, `tticomgov-code`) can run the merge executor | An automated executor could merge during the cut window. Make sure none is running (section 8). |
| Who can push and merge today | `tticom` is admin; `tticom-automation`, `tticom-codex` and `tticomgov-code` are collaborators with **push** (not admin) on all three repos. The ruleset's bypass is the Admin role only, so the agent accounts cannot bypass it, but each can merge a PR that satisfies it. The old audit's "delegated merge must carry an executor receipt" check is the only detective control for that, and the cut deletes it (C4). | Added as gate P1 in section 7: before the merge, either those credentials are constrained or retired for merge purposes, or the accepted-risk is recorded in `CLAUDE.md`; lean `CLAUDE.md` rule 1 alone is an instruction, not a control. Retiring accounts stays a separate later step. |
| Repos are public | `visibility: public`, plan `User` | Unchanged by this plan. |
| Merge method | all three allowed | Use a **merge commit** for the cut (keeps `slim-governance` history, keeps the skills pin an ancestor, and `git revert -m 1` is then the rollback). |

## 6. Conflicts a merge of `slim-governance` into a chopped branch would hit

Verified by actually doing it (rehearsal).

| # | Case | Result | Resolution |
|---|---|---|---|
| 1 | `tests/test_single_backlog.py`: chopped branch deleted it, slim modified it (+3 lines, exemption `f`) | `CONFLICT (modify/delete)`. The only slim-versus-chop conflict today. | Delete wins: `git rm tests/test_single_backlog.py`. |
| 2 | `ACTIVE_TASK.md`, `ORCHESTRATION_STATE.json` | **No conflict with slim**: slim never touches them. They conflict only with changes from `main` (row 4). | none |
| 3 | A slim edit to a `lean/` file after that file was promoted onto an existing root path (e.g. `lean/CLAUDE.md` -> `CLAUDE.md`, which already existed) | `CONFLICT (modify/delete)`: git cannot pair the rename because the target path is not new | Do not edit `lean/CLAUDE.md`, `AGENTS.md`, `TASKS.md`, `PULL_REQUEST_TEMPLATE.md`, `ci-slim.yml` on slim once promotion starts, or promote after the last slim merge, or apply the edit by hand to the root file. A pure move onto a new path (e.g. `projects/score2gp/CONTEXT.md` -> `docs/CONTEXT.md`) is followed correctly. |
| 4 | Changes landing on `main` while the chop branch lives (old framework keeps working) | Modified-on-main, deleted-on-chop: `CONFLICT (modify/delete)` (verified: `AGENT-RULES.md`, `ACTIVE_TASK.md`, `ORCHESTRATION_STATE.json`). Edits to a moved file follow it (verified: `CONTEXT.md` -> `docs/CONTEXT.md`). **New files added on `main` under deleted paths come back silently with no conflict** (verified: a new run record and a new `tests/test_new_gov.py` reappeared). | Delete-wins sync recipe in section 8. A resurrected test fails the lean suite only if its subject is missing; a resurrected record just pollutes the tree. Always run the resurrection guard. |
| 5 | Both sides modified a rewritten root file (`README.md`, `CLAUDE.md`, `AGENTS.md`) | would conflict as content | keep the chop side: `git checkout --ours -- <file>` |
| 6 | PR #751 (open, edits `AGENT-RULES.md`, `ORCHESTRATION_STATE.json`, `WORKFLOW_SKILLS_PROFILE.md`) or #749 (authority only) merging into `main` after the chop branch was cut | modify/delete on those files | same as row 4 |

Equivalent zero-conflict ordering (also verified): chop only the leaf scripts, merge slim
(clean), then chop the core (step order in section 7). The final tree is identical to the
literal order "chop everything, then merge slim" and the suite is never empty.

## 7. Ordered chop plan, with a proof gate after each step

Branch name `lean-cutover` (not `governance/...`: the old dispatcher classifies agentops
PRs with a `governance/` or `architect/` head branch as governance PRs). Run tests with
`-s` and a real file on standard input on this machine (section 0). Counts below are from
the rehearsal (Windows; `main` baseline 559 passed, 1 skipped).

| Step | Change | Gate (all must hold) | Rehearsal result |
|---|---|---|---|
| C0 | Tag `pre-lean-merge` on `origin/main` in each repo; record the three SHAs; save a copy of `ORCHESTRATION_STATE.json` outside the repos (seed source for `TASKS.md`, appendix C) | tags resolve; copy hashes recorded | n/a (not run: tags are a write) |
| C1 | `git rm` the 6 leaf scripts and 5 tests: `publish_handback`, `publish_review`, `review_evidence_gate`, `pr_review_state`, `agent_workspace_cleanup`, `pr_body` | full suite green; old audit PASS | 523 passed, 1 skipped |
| C2 | `git rm` the dispatcher chain: `dispatch`, `go_bootstrap`, `got_bootstrap`, `score2gp_bootstrap`, `bootstrap`, `link_session`, `control_plane` and their 5 tests (`dispatch`, `dispatch_entrypoint_contract`, `cp_13`, `legacy_wrappers`, `control_plane`) | green | 346 passed |
| C3 | `git merge slim-governance` | clean merge; green; lean tests present | 386 passed, 1 skipped, no conflicts |
| C4 | Retire the state machine **and swap CI in one commit**: `git rm` `orca_control`, `orchestrator`, `verify_identity`, `task_status`, `governance_audit`, their tests, `test_single_backlog.py`, `conftest.py`, `ORCHESTRATION_STATE.json`, `ACTIVE_TASK.md`, `REVIEWER_SCORECARD.json`; replace the workflow (see C7) in this commit if CI is to stay green per commit | only lean tests remain, still green; **never an empty suite** | 40 passed, 1 skipped |
| C5 | `git rm -r` per-task paperwork and role material (rules D3 to D7), keeping the five incident reports | green; `git ls-files` under `projects/score2gp/` lists only the files C6 will move | 40 passed, 1 skipped |
| C6 | `git mv` the knowledge files (rules M1 to M7) | green; moved files keep history (`git log --follow`) | 40 passed, 1 skipped |
| C7 | Promote: remove old root `CLAUDE.md`, `AGENTS.md`, workflow; `git mv` `lean/{CLAUDE,AGENTS,TASKS}.md` to the root, the PR template to `.github/`, `lean/ci-slim.yml` to `.github/workflows/ci.yml`; apply the section 9 fixes in the same commit; rewrite `README.md` | green; `repo_scan.py` 0 findings; `git diff --check` clean; `install_hooks.py --check` OK | Windows 39 passed, 1 skipped; Linux 3.12 40 passed; scan 0 |
| C8 | Final sync with `main` using the section 8 recipe, then the proof below | proof below | verified with a simulated `main` that edited the authority, rules and a moved file and added a run record and a test: 38 files after sync, 39 passed |

Intermediate commits C1 to C3 are green on their own; C4 to C7 can be squashed into fewer
commits if the maintainer prefers, provided the CI swap travels with the authority removal.

### What "it works" means (acceptance for the cut PR)

1. **Suite green** on Windows and on Linux Python 3.12 (the CI version), with the count
   recorded and any skip listed. Treat a skip as not evaluated.
2. **Lean checks run**: `python lean/scripts/repo_scan.py` reports 0 findings (also with
   `--names-file` pointing at the private-fixture names kept outside the repo; **not run
   here**); `install_hooks.py --check` OK; a push of a task branch is accepted and a push
   to `main` is refused in a scratch clone with a scratch remote (done in the rehearsal).
3. **Fixture check**: `python lean/scripts/real_fixture_check.py --product <product checkout>`
   reports PASS on the maintainer machine, or NOT_EVALUATED with a named reason; a skip or
   an empty result is never a pass. **Not run here** (private fixtures).
4. **One live task, end to end, in a scratch repository** (not the product repo): copy the
   chopped tree, seed `TASKS.md` with one trivial `normal` task and one trivial `risky`
   task, run an agent on each following only `CLAUDE.md` (claim by pushing `task/<id>`,
   worktree, implement, tests, draft PR from the template, hook installed, no merge). The
   `risky` task also runs the fixture check and one advisory `review`. Success: both PRs
   exist, CI is green, nothing on `main` was pushed by the agent, and the agent never
   needed a removed file. **Not run here** (needs a scratch GitHub repository and an
   agent run).
5. **Resurrection guard** passes: no tracked file under the retired roots (section 8).
6. **Protections gate** (section 11): G1, G2, G3, G5 and G6 are closed, or each is recorded
   in the PR as deliberately dropped with the reason; and gate P1 (agent merge credentials,
   section 5.5) is met. A green suite and a clean scan alone do **not** show these.
7. **Rollback rehearsed**: on the scratch clone, `git revert -m 1 <merge>` restores the
   old tree and the old suite (559 passed, 1 skipped).

### Rollback

- Before the PR merges: close the PR, delete `lean-cutover`; `main` never changed.
- After it merges: `git revert -m 1 <merge commit>` on a branch and PR it (the ruleset
  forbids force-push and deletion, so history is never rewritten). Reverting a merge
  means a later re-merge of the same branch needs the revert reverted first. The
  `pre-lean-merge` tag marks the old state for reference and for pinning old clones.
- Agent-side: the launchers and identity clones are untouched by the merge. Pin any clone
  that must stay on the old framework to the tag (section 5.3).
- Irreversible items from `CUTOVER.md` (revoking tokens, rotating credentials, making
  repositories private) are not part of this merge and remain separate decisions.

## 8. Cutting while the old framework keeps running (no drain)

Agents on the old framework keep starting tasks and know nothing about the experiment, so
the chop branch has to be cuttable at any moment. Two mechanisms, usable together.

### 8.1 Keep the chop branch current with `main` (delete wins)

Merge `main` into `lean-cutover` regularly (a merge, not a rebase: a rebase replays the
modify/delete conflict once per chop commit). After each merge:

```text
git merge origin/main            # expect modify/delete conflicts on retired paths
# delete wins: remove every retired root from index and tree, whatever its merge state
for p in scripts tests .agents skills tasks projects docs/cycle-preparation-history \
         AGENT-RULES.md .github/workflows/governance-control-plane.yml; do
  git rm -rqf --ignore-unmatch -- "$p"; done
# rewritten roots (README.md CLAUDE.md AGENTS.md): keep the chop side
git checkout --ours -- README.md CLAUDE.md AGENTS.md   # only if they conflicted
git commit
```

`-f` is required: a file newly added on `main` is staged and `git rm` refuses without it
(verified). `projects` is safe to remove wholesale only after C6 moved its kept files; in
the chopped tree it is empty. After the merge run the **resurrection guard**: the output
of `git ls-files -- scripts tests .agents skills tasks projects docs/cycle-preparation-history AGENT-RULES.md`
must be empty (until the cut, because later `tests/` and `scripts/` are legitimate again),
then the suite and `repo_scan.py`. Verified end to end in the rehearsal. What it cannot do:
changes made on `main` to retired files are discarded on purpose; changes to moved
knowledge files are carried **only if git pairs the rename** (similarity of about half the file or more).

Cases the rehearsal did not cover, to check by hand on each sync:

- `main` adding `.github/workflows/ci.yml` or `.github/PULL_REQUEST_TEMPLATE.md` (paths the
  chop creates) gives an add/add conflict; keep the chop side and review what `main` added.
- A heavily edited moved file (`projects/score2gp/CONTEXT.md`, `REVIEW_RULES.md`, the
  requirements, ...) whose rename is not detected stays at its old path and is then removed
  by the `projects` sweep. After every sync list the files `main` changed since the last
  sync (`git diff --name-status <last-sync>..origin/main -- projects/score2gp`) and confirm
  each moved-source file's change appears at its `docs/` target; apply it by hand otherwise.

### 8.2 Choosing the moment

A quiet point is useful but not required, because section 8.1 absorbs whatever `main` did.
Prefer a moment where:

- no open pull request on `main` of the three repositories edits a retired path other
  than through the old governance flow (check `gh pr list` and each PR's files). Open
  agentops governance PRs (today #749 and #751) and any later promotion or reconciliation
  PR will, after the cut, target files that no longer exist: they must be closed, with
  their intent already covered by `TASKS.md` or abandoned;
- no merge executor, launcher run or reviewer session is mid-flight on the three repos
  (an executor merging after the final sync reintroduces the conflicts and lands changes
  the chop never saw). `merge_controller` is a live role today;
- the final sync, the proof (section 7) and the PR approval happen back to back, with no
  push after the approval (it would be dismissed).

### 8.3 What happens to work in flight at the cut

| In flight today (2026-10-01) | At the cut |
|---|---|
| Product PR `tticom/score2gp#476` (CFW-04, draft, authored by `tticom-codex`, checks currently failing) | Product repo is not chopped, so the PR and its branch are unaffected and can be finished and merged by the maintainer. What disappears is the surrounding governance (handback, governance review, promotion/reconcile PR). Re-home: add a `TASKS.md` entry `CFW-04` (`risky`, branch `feat/cfw-04-grace-small-heads`, allowed paths from the authority record), finish with the local fixture check and an optional advisory review. The authority record at the freeze tag keeps the allowed paths and acceptance text. |
| `next_task_proposal` SCALE-01 (`PROPOSED`, product, author `tticom-codex`, prompt in `prompts/next/`) | Not started under the authority yet. Carry as a `TASKS.md` entry from the freeze-tag record (`risky`: it changes detection constants); the prompt text is copied into the entry's notes, not versioned as a file. If the old framework promotes it before the cut it becomes the same case as CFW-04. |
| Open agentops PRs #749 (drops CFW-01, CFW-02, OMIT-03-FU2 from the authority) and #751 (parallel lanes, `AGENT-RULES.md` rules 10 to 12, CP-14 to READY) | Both edit only retired files. If still open: close (nothing to carry; the intent of #751 is already lean `CLAUDE.md` rule 12). If they merge first they are just more delete-wins conflicts. #749 matters in the meantime only because it removes superseded items from the old ready frontier. |
| PR #752 (this slim PR, draft) | Keep draft. It becomes redundant once `lean-cutover` merges. |
| Any promotion/reconcile PR created by the old flow between the final sync and the merge | Closed; its authority edit is moot. |
| Old-framework agents mid-session | Their clones pull `main` on the next `go`/`got` (fast-forward sync), find no dispatcher and no `ACTIVE_TASK.md`, and stop (fail closed). Pin clones that must continue (section 5.3). The product `CLAUDE.md` rewrite should land with the cut so product-side agents are not told to read removed files. |

> Update 2026-10-03: `CUTOVER.md` was renamed to `MIGRATION.md` and reworked as proposed here.

## 9. Superseding `CUTOVER.md`, and slim-side fixes needed before the merge

`CUTOVER.md` was written for a fresh-history private repository. That part is wrong for
this repository (and applies at most to the Rust component, later, with its own evidence
gate). **Proposal: rename `CUTOVER.md` to `MIGRATION.md` and rework it from section 10**,
keeping the reversibility labels, the scan step and the irreversible-items list. It is
not renamed or deleted by this change; it carries a status banner only.

Needed on `slim-governance` before the cut (all verified in the rehearsal; not applied,
except the first two which keep this branch's own checks green):

| # | Fix | Why | Applied now |
|---|---|---|---|
| S1 | Add `MERGE-READINESS.md` to exemption `f` in `tests/test_single_backlog.py` | new document uses "backlog/queue" wording; the old test would fail | yes |
| S2 | `CUTOVER.md` line 74: replace the literal `drive:\Users\...` example with a placeholder | `repo_scan.py` flags it (`local-path`), so the lean CI would be red on the promoted tree | yes |
| S3 | `lean/tests/test_lean_guidance_paths.py`: look for `CLAUDE.md`, `AGENTS.md`, `TASKS.md` at the root when no `lean/` copy exists; stop reading `CUTOVER.md`; skip `lean/skills` paths | fails after promotion (verified 2 failures) | no (promotion-time) |
| S4 | `lean/CLAUDE.md`: remove "`lean/PULL_REQUEST_TEMPLATE.md` before cutover" and "`lean/ci-slim.yml`, promoted to"; update "moved to `docs/rejected-claims.md` at cutover" to the final path; **also align names the path test does not check** (it reads only backticked `lean/` paths): `docs/incidents.md` (line 101; the plan produces `docs/incidents/`), `reports/` (line 101; the template is `lean/reports/`), and the `CUTOVER.md` references in `lean/CLAUDE.md` (line 124), `lean/README.md` (lines 4 and 26) and `lean/TASKS.md` (line 40) once `CUTOVER.md` becomes `MIGRATION.md` | the S3 test flags the first two once the files moved; the rest become stale or dangling. Consider widening the test to every backticked repo-relative path | no (promotion-time) |
| S5 | `lean/README.md`: drop "inert until cutover" wording | stale after promotion | no (promotion-time) |
| S6 | Do not edit the promoted `lean/` guidance files on slim after promotion starts (section 6, row 3) | modify/delete conflicts | process |

## 10. `CUTOVER.md` steps mapped to this plan

| `CUTOVER.md` step | Status here |
|---|---|
| 1 Drain | **Removed.** Replaced by section 8 (no drain assumed). |
| 2 Freeze marker (tags) | Keep, as `pre-lean-merge` (C0). |
| 3 Seed the task list | Keep (appendix C). |
| 4 Build snapshot tree in a scratch directory | Replaced by the `lean-cutover` branch. |
| 5 Scan the snapshot | Keep: `repo_scan.py` on the branch, plus `--names-file`. |
| 6 Run the lean tests | Keep (gate in C7/C8). |
| 7, 8 New private repo, fresh history | **Not this repo.** Rust component only, separate. |
| 9 Hooks | Keep (`install_hooks.py`, verified). |
| 10 Agent credential | Keep as an evidence-gated later decision. |
| 11 CI before any trial | Keep (`ci.yml` arrives in C4/C7). |
| 12 Trial | Keep (acceptance item 4, scratch repository). |
| 13 Switch off the dispatcher | Later, after the merge; move launchers aside, do not delete. |
| 14 Retire role accounts | Later and separate. Keep an approver usable until the cut PR merges. |
| 15 Archive old repos | **Not applicable** (same repositories). |
| 16, 17 History audit, make private | Separate later decisions, irreversible; unchanged by this plan. |
| 18 Final checks | Keep: agent identity cannot merge. |

## 11. Where lean is weaker than `main` (gaps to close before or when merging)

| # | Protection on `main` that lean does not carry | Suggested handling |
|---|---|---|
| G1 | `REVIEW_RULES.md` is the "Score2GP overlay" the launchers apply on top of the generic review skill. The lean `review` skill and `CLAUDE.md` never mention it. | Keep it as `docs/review-rules.md` (done in the rehearsal) and reference it from the `risky` review paragraph of `CLAUDE.md`, or consciously drop it. |
| G2 | `.agents/rules/prohibit_destructive_hacks.md` lists four specific bans (do not widen geometry tolerances, do not scale durations to fit a bar, do not merge digits without semantic guards, do not synthesise open-string TAB defaults). `conversion_verification_standards.md` bans treating synthetic-test pass rates as fidelity and using private fixtures as source of constants. Lean rules 5 and 6 are the general form but not the specifics. | Fold the four bans into `docs/rejected-claims.md` or `CLAUDE.md` before deleting `.agents/rules/`. |
| G3 | `.agents/rules/pr_standards.md`: explicit descriptive PR title, conventional-commit style, non-default fields. | Check `lean/PULL_REQUEST_TEMPLATE.md` covers the title rule; add one line if not. |
| G4 | Old audit checks that distinct reviewer and publisher identities are recorded and SHA metadata is full-length. | Not needed once those records no longer exist (the delegated-merge receipt check is G7, which is needed). |
| G5 | `repo_scan.py` checks do not include the old audit's `work/`, `inspect/`, `overlays/` banned-path rule or `.html`/`.musicxml` extensions. | Add `work/`, `inspect/`, `overlays/` and the two extensions to the scan before relying on it as the only gate. |
| G6 | `repo_scan.py` stops reading a file at its first NUL byte, so a private binary renamed to an extension outside its forbidden list and under 1 MB passes unexamined; and CI cannot run `--names-file` because that file lives outside the repository by design. | Make any tracked file containing a NUL byte a finding unless allow-listed, and run the names scan locally as part of the acceptance gate (item 2), not as a CI claim. |
| G7 | Today a merge by a delegated credential without an executor receipt is detected by the audit; lean has an instruction (`CLAUDE.md` rule 1) and a push hook only. | Gate P1 (section 5.5). |

## 12. The five biggest risks

1. **The old flow keeps moving, and the cut needs one quiet resolution.** Every old-flow
   merge touches files that will be deleted, and new per-task files reappear silently.
   Mitigation: section 8.1 recipe plus the resurrection guard; the recipe was verified but
   only against a simulated `main`.
2. **Identity clones, launchers and merge-capable credentials.** The first `go`/`got` or
   launcher run after the merge fast-forwards onto a tree with no dispatcher (safe, fails
   closed, disruptive). Separately, the three agent accounts keep push access and can merge
   a PR that satisfies the ruleset, and the only detective control for that (the audit's
   executor-receipt check) is deleted by the chop: gate P1.
3. **Product-side guidance still points at removed files.** The product `CLAUDE.md`,
   `AGENTS.md`, `docs/agentops.md` and `HANDOFF.md` must change in a product PR (ruleset:
   one approval) that lands with the cut, or product agents stop at preflight.
4. **Lean is not a superset of today's protections** (section 11): the review overlay and
   the four conversion-hack bans exist only in files the chop deletes, and the privacy
   scan has a NUL-byte blind spot (G6). A green suite and a clean scan can pass while these
   are lost, so they are an explicit gate (acceptance item 6), not a footnote.
5. **Gates that cannot be proved from here.** The fixture check, the scratch-repository
   task run and the `--names-file` private-name scan need the maintainer machine; until
   they run, "it works" is shown for static checks, the hook and the test suites only.

## 13. What could not be determined

- Whether the new CI job passes on GitHub's runners (it passes locally on Windows and in a
  `python:3.12-slim` container; not run on Actions: needs a push).
- Real-fixture check result, private-name scan, and a live agent task on the lean flow.
- Whether GitHub treats an extra open agentops PR (such as #752) as a blocker for the old
  dispatcher: by reading, active-task PR discovery queries by the task's branch
  (`gh pr list` per branch in `score2gp_orca_control.py`), so it should not; no live
  dispatch was run.
- Whether any session, launcher or merge executor is running right now, and whether
  `merge_controller` automation is armed.
- Whether the product repository's ruleset or CI changed since the read on 2026-10-01.
- Behaviour on a Windows host without long-path support: the rehearsal needed
  `core.longpaths=true` to check out `main` (some 160-character paths under `runs/`);
  after the chop this no longer matters.

## Appendix A. Seeding `TASKS.md` (read-only extraction at the freeze tag)

The authority at `e9a5615` holds 142 backlog items (READY 48, NEEDS_DETAIL 71, IDEA 18,
NEEDS_RESEARCH 5; 38 READY items target the product repository, 10 target agentops),
37 completed tasks, the active task CFW-04 (`PROMOTED`, authority revision 95), the
proposal SCALE-01, and three resolved incidents. Backlog items carry `title`,
`requirements`, `kind`, `repository`, `status`, `priority`, `depends_on`, `notes`; a
`TASKS.md` entry also needs `allowed paths` and `done when`, which backlog items do not
have, so the extraction is lossy by design:

- Seed only what the maintainer still wants; default is CFW-04 and SCALE-01 (their
  records have allowed paths and acceptance), plus `CP-06`.
- Map `kind` and content to `risk`: conversion logic, parsers, geometry, timing,
  fallbacks and private fixtures are `risky`.
- Items that concern the old machinery (the `CP-*` items against agentops, `GOV-*`) are
  not carried.
- `NEEDS_DETAIL` and `IDEA` items stay in history until someone details them.

## Appendix B. Rehearsal log

Rehearsal clone: created with `git init` plus `git fetch` of the two refs, long paths on,
nothing pushed. Branches: `chop-c` (the recommended order, C1 to C7d), `chop-a` (literal
order: everything chopped, then slim merged), `chop-b` (slim merged first, then chopped),
`trial-merge` (slim plus `main`, no chop), `main2` (a simulated `main` that edited the
authority, `AGENT-RULES.md`, `ACTIVE_TASK.md`, a moved file and added a run record and a
test). `chop-a` and `chop-b` produced the same tree. Counts after each step are in the
section 7 table. Skills: `main` 613 passed, 1 skipped, validate 12 skills; chopped 196
passed, 1 skipped, validate 6 skills.
