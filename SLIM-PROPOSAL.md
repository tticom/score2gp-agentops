# SLIM-PROPOSAL: a slimmer governance framework

Status: DRAFT proposal for the maintainer (tticom). Nothing here is applied.
`main` keeps running the current framework untouched. Nothing is deleted or
rewritten by this PR; it only adds this file.

Companion document (same branch name, other repo):
[`agentops-claude-skills` `SLIM-PROPOSAL.md`](https://github.com/tticom/agentops-claude-skills/blob/slim-governance/SLIM-PROPOSAL.md).
That one covers the 12 skills and their scripts in detail. This one covers the
rules, roles, gates, artefacts and scripts in `score2gp-agentops`.

Basis: `origin/main` of `score2gp-agentops` at `6611399` (PR #748), read on
2026-10-01, plus GitHub PR history of `tticom/score2gp-agentops` (751 PRs) and
`tticom/score2gp` (475 PRs).

## 0. Headline

- The framework solves some real problems. Five protections are well evidenced
  and worth keeping (section 2.1): no agent merges or approves its own work, no
  direct pushes to main, no private data in public commits, no false-green
  tests, no silent fallbacks in the converter.
- Almost all of the bulk is not that. Of 751 agentops PRs, 458 (61%) are
  bookkeeping about the process itself (promote, reconcile, record, assign,
  backlog, authorise, dispatcher fixes), a further 170 (23%) are docs or
  research, and only about 120 (16%) are code, rules or tooling. Of the 702
  files under `projects/score2gp/`, 646 are per-task paperwork (182 run
  files, 120 prompts, 114 decisions, 83 reviews, 79 research, 52 reports,
  16 handoffs).
- The authority state machine is the largest single cost.
  `ORCHESTRATION_STATE.json` is 203 KB (completed tasks alone 90 KB, backlog
  73 KB). About 30 PRs only fixed the dispatcher, bootstrap or state resolver.
  The 2026-09-24 report shows the machine itself causing a stall (stale
  authority, failing audit on main, dispatcher failing closed for every role).
- Split of the 67 inventoried items in section 1: 18 real protections or
  lasting knowledge (kept, 3 of them replaced by CI), 19 that pair a real
  goal with heavy mechanism (simplify), 30 pure ceremony or machinery
  (drop). So roughly 27% protection, 28% worth simplifying, 45% ceremony. By
  volume it is more lopsided: about 4,800 lines of process scripts and 11,200
  lines of tests for them, against fewer than 600 lines that guard the real
  protections.
- Independent review does find real defects: in product PRs, 42 of the 91 that
  got a formal review had CHANGES_REQUESTED first (46%). So review should
  stay, but as an option for risky changes, not a state-machine step on every
  task.

## 1. Inventory

Columns: what it prevents, evidence the failure really happened (PR numbers
are `tticom/score2gp-agentops` unless prefixed), and the proposed class.
Class: KEEP, SIMPLIFY, DROP, CI (replace by an automated check). Type: P
(real protection) or C (ceremony / machinery). "No incident found" means I
looked and could not find a concrete occurrence; the rule may still be sound
precaution.

### 1.1 Rules and gates

| ID | Item | Prevents | Evidence it happened | Type | Class |
|---|---|---|---|---|---|
| R1 | No self-approval; reviewer is not the author (`pr_standards` 4/6, role policy) | Author marking own work good | 2026-07-21 incident: agent ran `gh pr review --approve` and `gh pr merge --admin` on #341; the ruleset's last-pusher rule refused (`reports/2026-07-21-fs03c-prohibited-merge-attempt-incident.md`) | P | KEEP |
| R2 | No direct main push, no merge by agents, no `--admin` | Unreviewed code on main | #333 merged with `--admin` by an agent using the maintainer credential (`reports/2026-07-20-unauthorized-agy-merge-incident.md`); second attempt 2026-07-20; #374/#375 prohibited merge attempts | P | KEEP, enforced by ruleset/CI |
| R3 | Three separate GitHub identities + `verify_identity.py` + per-slot credential stores | Agent acting with maintainer credentials | Root cause of R2 incident (agent held `tticom` token). The identity machinery grew from it | P (the goal), C (the mechanism) | SIMPLIFY: agent token cannot merge; no role accounts |
| R4 | Merge executor, merge receipts, 2-approval policy, merge_controller role, executor audit (GOV-01..03) | Out-of-policy merges | 2026-09-24: #681 and #682 merged by the maintainer outside the policy, leaving authority stale (`reports/2026-09-24-win-01-win-02-out-of-policy-merges.md`). The policy was stricter than the owner's own practice | C | DROP (ruleset + CI replaces it) |
| R5 | Sanitised evidence only, no raw logs in PR bodies; `scripts/pr_body.py` redaction | Private paths, credentials and identifying data in PR text | Redaction had to be fixed three times: `2a571f0`, `f1ea989`, `525533d` (multi-word leaks). Credential redaction in runtime logs: `a331b74`, `75c0255` | P | KEEP the rule; CI secret/path scan replaces the helper |
| R6 | No raw private PDF/GP/MXL/screenshots in unrelated commits (AGENT-RULES 3) | Private fixture leak | No committed leak found. Post-merge audit of #239 ran a manual `git ls-files` check for it. Sound precaution | P | CI (extension allow-list + size check) |
| R7 | Skipped tests are NOT_EVALUATED, never PASS (`REVIEW_RULES` section 1) | False-green CI | CRP-10/11/12: private integration tests skipped when fixtures absent, CI "green", defects merged (`reports/2026-08-13-review-skills-failure-assessment.md`, tasks 103, PR #550) | P | CI (report skips; fail if a required private marker skipped on the maintainer machine) |
| R8 | No silent fallbacks; fail closed (`REVIEW_RULES`; `prohibit_destructive_hacks`) | Invented data in output | Same report: `ScoreIRCompiler` injected string=1/fret=0 notes; timeline injected `padding_rest` and truncated overlaps | P | KEEP as short rule list in CLAUDE.md |
| R9 | Mock-only tests cannot be the sole proof; real-fixture check with `skipif` (`pr_standards` 5) | Synthetic-only confidence | Same report (CRP-11 sequential chord logic passed on mocks) | P | SIMPLIFY: required for conversion-fidelity claims only, not "every code modification" |
| R10 | Ground truth by semantic diff; oracle integrity; Rejected Claims register; Evidence Register | Claims contradicted by the source | EV-001 (PR #137): Derek Trucks "omitted measures" claim contradicted by visual inspection; `REJECTED_CLAIMS.md` has 5 such claims | P | SIMPLIFY: keep the 5 rejected claims as a half page; drop the register format |
| R11 | Report strict mode, remediation mode, semantic result, file-exists separately | One "success" hiding failures | Rejected Claims 2-5; PR #239 audit has the four-way report | P | SIMPLIFY: a line in the PR template for conversion PRs |
| R12 | Tier A / Tier B loop | Over-process of small tasks | No incident; it is itself process | C | DROP |
| R13 | `ORCHESTRATION_STATE.json` as sole task authority; `ACTIVE_TASK.md` generated; leases; seven `advance()` decisions | Agents picking their own work, scope drift, duplicate PRs | Early drift: no-progress PRs that repackaged evidence (`decisions/2026-06-18-mandatory-incremental-progress-rule.md`); 382 docs PRs. But the machine's cost: 203 KB state, 4,836 script lines, about 30 repair PRs | C | DROP, replace by a small task list (section 3) |
| R14 | Promotion and reconciliation PRs (every task needs a governance PR to start and another to record completion) | Executing unauthorised or stale work | The goal is sound. The mechanism is about 460 PRs; chain "Task N - Record N-1 and authorise N+1" (#139-#183); #748/#749/#750/#751 added four PRs around one task start | C | DROP |
| R15 | Per-task scope fence (allowed paths) amended by governance PR | Scope creep | Many amendments: #737, #743, #747, #750 ("add tests/... to CFW-04 scope") | P (goal) / C (amend via PR) | SIMPLIFY: scope in the task entry; reviewer flags out-of-scope files |
| R16 | Startup protocol: dispatcher `go`/`got` bootstraps, router, `score2gp_dispatch.py`, fetch/status ritual | Agent starting from stale state | Roughly 30 fix PRs on dispatch and state: #390-#399, #416, #419, #422-#424, #427, #429, #452, #477, #478, #483, #516, #601, #613-#615, #620-#622, #640, #641, #663, #664 | C | DROP |
| R17 | Exact-head author handback comment (`publish_handback.py`) | Reviewer judging a stale head or an unsupported claim | #525 "diagnose stale author handbacks", #537 "reconstruct and publish missing author handbacks" | P (head pinning) / C (handback ritual) | SIMPLIFY: PR body plus CI; reviewer pins the head SHA |
| R18 | Guarded exact-head review publisher, marker summary, post-publication readback | Reviews recorded only in chat; raw `gh pr review` bypassing head binding | Agent review was lost or mis-bound; skills PRs #4, #6 are fixes to this machinery | P (pin to head) / C (markers, readback) | SIMPLIFY |
| R19 | Review evidence gate (falsification ledger, probe counts, strike-adjusted) | Approvals on unverified claims | score2gp#396: approval overturned because claimed end-to-end/privacy evidence was not run (scorecard); CRP-10..12 | P | SIMPLIFY: keep for risky changes only |
| R20 | Reviewer scorecard, strikes, probe quota penalties | Careless reviewers | One recorded incident (#396), no decay event ever exercised | C | DROP |
| R21 | "Accuracy over agreeability": start at cannot-verify; claims are untrusted | Rubber-stamp review | Same incidents as R19 | P | KEEP as prompt text in the review skill |
| R22 | Role set: architect, developer, reviewer, orchestrator, integrator, director, supervisor, governance, merge_controller, TPO sceptic | Role collapse | The real collapse cases are all author-also-approves or agent-also-merges (R1, R2). Other roles have no incident | C | SIMPLIFY to author, reviewer, maintainer |
| R23 | Mandatory architect decision gate; A/B/C outcome; post-task decision records | Unbounded diagnostics loops | 2026-06-17 gate and 2026-06-18 rule; the diagnostics era (tasks 69-175) produced 114 decision records | P (stop unbounded diagnostics) / C (a record per task) | SIMPLIFY: one rule, no records |
| R24 | PR standards: explicit title, populated body, `pr_body.py`, PR Evidence Contract claim ledger | Empty or placeholder PRs; plausible narratives | No incident found for empty titles. Claim ledger responds to #396-style approvals | C / P | SIMPLIFY: 6-line PR template; claim ledger only for conversion claims |
| R25 | Branch hygiene (check branch, switch, new branch for off-task work); one agent per worktree | Cross-task contamination, two agents in one tree | No incident found; the concurrent-agent setup makes it cheap insurance | P | KEEP (two lines) |
| R26 | Real-World Evaluation Loop against private fixtures | Passing synthetic tests while real files fail | Same as R9; Lesson 3 omissions (#718, #722) found only by real run | P | KEEP, as a local script, not a gate on every PR |
| R27 | Governance audit script and CI check | Authority drifting from its generated view | The audit failed on main after #681/#682 (R4 report) | C | DROP with R13 |
| R28 | Skills lock pin and symlink activation (`SKILLS_LOCK.md`, #744) | Skills changing under a running agent | #744 pins skills at `c51d446`; no failure found | P (small) | SIMPLIFY: pin by tag |
| R29 | Single-backlog test and `REVIEWED_MENTIONS` list (683 lines) | Second hidden task list | A rule born of earlier multiple lists (PLAN-01, #700) | C | DROP (with R13) |
| R30 | Concurrency leases and distinct cycle roots per task | Parallel task collision | None found | C | DROP |
| R31 | Governance-control-plane CI (`json.tool`, `py_compile`, `pytest`, `diff --check`) | Broken scripts merged | It works, and it is the only automated gate | P | KEEP (shrinks with the scripts) |
| R32 | Main_Protect ruleset (1 approval, thread resolution, no force push, no deletion) | R1, R2 at the host | Held in the 2026-07-21 incident | P | KEEP (see open question 2 about private repos) |

### 1.2 Roles (as operated)

| ID | Item | Evidence | Type | Class |
|---|---|---|---|---|
| L1 | Author accounts `tticom-automation`, `tticom-codex` | 97 and 15 of 751/475 PRs | C | DROP separate accounts; one agent identity at most |
| L2 | Governance account `tticomgov-code` (153 agentops PRs, nearly all promote/reconcile) | List in section 1 | C | DROP |
| L3 | Reviewer accounts (codex, gov) | 162 approvals, 152 changes-requested in product repo | P (independent view) | SIMPLIFY: any fresh session, no dedicated account |
| L4 | Maintainer `tticom` | 348 PRs | P | KEEP |
| L5 | Role prompts `projects/prompts/01..05` (architect, TPO sceptic, developer, reviewer, director) | n/a | C | DROP into the review and implement skills |

### 1.3 Handback and handoff artefacts (per task)

| ID | Artefact | Count on main | Evidence of value | Type | Class |
|---|---|---|---|---|---|
| A1 | `projects/score2gp/prompts/` task prompts | 120 | Prompt is the task spec; useful at the time | C | DROP archive; spec lives in the task entry and PR |
| A2 | `decisions/` post-task records | 114 | 2 of 114 are lasting architecture decisions (`recognition-architecture-v1`, tab timing policy A/B/C); the rest are "authorise task N+1" | C | KEEP the lasting ones in one ADR file, drop the rest |
| A3 | `runs/` run records | 94 dirs / 182 files | `RUN_RECORD_TEMPLATE`; reviewers cite them | C | DROP (PR description + git history) |
| A4 | `reviews/` | 83 | Review text also lives on the PR | C | DROP |
| A5 | `research/` and `reports/` | 79 and 52 | Real findings (corpus audits, failure analyses) | P (knowledge) | KEEP in a `docs/research/` folder, no per-task index |
| A6 | `handoffs/` | 16, 14 of them promotion/reconciliation notes | | C | DROP |
| A7 | Incident reports (5 in `reports/`) | 5 | They are why R1/R2/R4 exist | P | KEEP as `docs/incidents.md` |
| A8 | `ACTIVE_TASK.md`, `ACTIVE_PLAN.md`, `NEXT.md` views | 2 | Generated view of R13 | C | DROP |
| A9 | Templates (9): task, completion record, prompt record, run record, PR body, requirement packet, research report, prompt manifest, chain README | 9 | | C | DROP all but a PR body template and a requirement template |
| A10 | Requirements register `requirements/REQ-0001..0005` | 5 | Anchors "what must be true" | P | KEEP |
| A11 | Exact-head author handback comment | 1 per PR | #525, #537 | C | DROP |
| A12 | Context and acceptance docs (`CONTEXT.md`, `ACCEPTANCE_TARGETS.md`, `BENCHMARK_LADDER.md`, `MAJOR_TRIADS_BENCHMARK.md`) | 4 | Orientation for new agents | P | SIMPLIFY into one CONTEXT.md |

### 1.4 Scripts (and their tests)

| ID | Script (lines / test lines) | Purpose | Class |
|---|---|---|---|
| S1 | `score2gp_orca_control.py` (1,460 / 1,684) | Authority validator, `advance`, merge executor, frontier | DROP |
| S2 | `score2gp_orchestrator.py` (599 / 401) | The `advance()` decision | DROP |
| S3 | `score2gp_governance_audit.py` (409 / 1,072) | Authority drift audit | DROP |
| S4 | `score2gp_dispatch.py` (315 / 473) + `go`/`got`/`bootstrap` (362) + `score2gp_bootstrap.py` + `bootstrap.py` + `link_session.py` | Dispatcher and startup | DROP |
| S5 | `score2gp_control_plane.py` (283 / 307) | Venv, skills pin activation | SIMPLIFY (pin only) |
| S6 | `score2gp_publish_handback.py` (223 / 142) | Author handback | DROP |
| S7 | `score2gp_publish_review.py` (263 / 298), `score2gp_pr_review_state.py` (87 / 87), `score2gp_review_evidence_gate.py` (165) | Review publication and gate | SIMPLIFY (use the skills-repo copies only) |
| S8 | `verify_identity.py` (136 / 148) | Identity gate | DROP once R3 simplified |
| S9 | `pr_body.py` (125 / 120) | Sanitised PR body | CI (secret/path scan) |
| S10 | `score2gp_agent_workspace_cleanup.py` (145 / 79), `score2gp_task_status.py` | Worktree cleanup, status | SIMPLIFY (skills repo `workspace-cleanup` does this) |
| S11 | Tests for the above (`test_single_backlog`, `test_cp_13_codex_author_lane`, `test_governance_audit`, ...) | | DROP with their targets |
| S12 | `.github/workflows/governance-control-plane.yml` | The only CI | KEEP, replace content (section 3) |

### 1.5 Skills and agent definitions held in this repo

| ID | Item | Class |
|---|---|---|
| K1 | `skills/score2gp-developer.md`, `score2gp-pr-hard-review.md`, `score2gp-project-director.md`, `score2gp-task-orchestration.md` | DROP; content folds into CLAUDE.md and the two kept skills |
| K2 | `.agents/skills/*` (cleanup, project-director, remediation-governance, report-consolidation) | DROP (cleanup duplicated by `workspace-cleanup`) |
| K3 | `projects/score2gp/skills/*` (architect, conversion-recovery-director, developer, orca-supervisor, project-director) | DROP |
| K4 | `.agents/agents/*.json` (architect, developer, project-director, reviewer) | DROP |
| K5 | `.agents/rules/*` (conversion verification, PR standards, destructive hacks) | KEEP the first and third as 10 lines; PR standards simplified (R24) |
| K6 | Three root files saying overlapping things: `AGENT-RULES.md`, `AGENTS.md`, `CLAUDE.md` (6.7 KB each) | MERGE into one `CLAUDE.md` of about 1 page |

Skills in `agentops-claude-skills`: see that repo's SLIM-PROPOSAL, section 4.

## 2. Classification

### 2.1 Real protections (keep, ideally automated)

1. Author cannot approve or merge their own work (R1, R2, R32).
2. No direct pushes to main, no admin bypass, no agent holding a token that
   can do either (R2, R3). This is the root cause of three incidents.
3. No private data in public places: commits, PR bodies, logs (R5, R6).
4. No false green: skipped private tests are reported, not counted (R7, R9, R26).
5. Converter fails closed, no invented data; claims judged against the source
   file, not against summaries (R8, R10, R11).
6. A review, when done, judges one exact head SHA and treats claims as
   untrusted (R17 pinning, R18 pinning, R19, R21).
7. Lasting knowledge: requirements, a few ADRs, incidents, research (A5, A7, A10).

### 2.2 Ceremony and machinery (simplify or drop)

- The authority state machine and everything that feeds it: R13, R14, R16,
  R27, R29, R30, A1, A3, A4, A6, A8, S1-S4, S6, S8, S11.
- Account multiplication: L1, L2, R3, R4, R20.
- Per-task records: A2 (most), A9.
- Role inflation and duplicated rule files: R22, K1-K4, K6.

### 2.3 Why each kind of protection moves

| Protection | Today | Proposed |
|---|---|---|
| No self-approval | 3 accounts + role gate + policy | Maintainer is the only merger; agent token cannot merge; optional independent review is advice, not authority |
| No main pushes | Ruleset + dispatcher + role policy | Ruleset (or local hook) only |
| No leaks | Rule + redaction helper + reviewer checklist | CI scan |
| No false green | Reviewer rule | CI reports skips; local private suite run recorded as counts |
| Right head reviewed | Handback + publisher + readback | Review comment starts with the head SHA; CI is per head anyway |
| Scope control | Authority + amend PRs | Scope line in the task, reviewer flags extra files |

## 3. Proposed minimal framework

Principles: one author per task; CI green is the gate; independent review is
optional and used when risk says so; a small task list, not a state machine;
nothing depends on separate GitHub identities, so the repos can go private.

1. **Task list.** One file, `TASKS.md`, with one entry per open task:
   id, one-sentence outcome, requirement it serves, allowed paths, risk
   (`normal` or `risky`), status (`todo`, `doing`, `done`). Done entries are
   deleted; history is in git and the merged PR. GitHub issues work equally
   well if the maintainer prefers them. No promotion PRs: the maintainer (or
   the agent, following the list order) just starts the next one.
2. **Author flow.** Own worktree, branch `task/<id>`, implement, open a draft
   PR from a 6-line template (task id, what changed, tests run, real-fixture
   result as counts, limits, risk). Mark ready when CI is green.
3. **Gate = CI.** One workflow: unit tests with skip report; lint/type checks
   as today; secret and private-path scan; forbidden-file check (no
   `.pdf/.gp/.mxl/.png` outside an allow-list, size limit); `git diff --check`.
   Failing CI blocks merge (required status check).
4. **Risk and review.** `risky` = changes to conversion logic or the compiler
   or fallbacks, anything touching private fixtures, CI or governance files,
   or a disputed PR. Risky PRs get one independent review by a fresh session
   using the kept `review` skill (adversarial mode available), posted as a PR
   comment that begins with the head SHA. `normal` PRs may merge on green CI.
5. **Merge.** The maintainer merges, or enables auto-merge on `normal` + green.
   Agents never merge, never use `--admin`, never hold a token with merge
   rights. No merge executor, no receipts.
6. **Real-fixture check.** A local script (the Real-World Evaluation Loop)
   run on the maintainer machine; its counts go into the PR. Required for
   `risky` conversion PRs.
7. **Knowledge.** `CLAUDE.md` (one page: rules R5-R11, R25, R26), `docs/`
   for requirements, ADRs, incidents and research.

What disappears: authority JSON, `ACTIVE_TASK.md`, dispatcher and bootstrap,
promotion and reconciliation PRs, handbacks, per-task prompt/run/decision/
review records, scorecard, merge executor, governance audit, three role
accounts, `go`/`got`.

Estimated size: scripts from about 4,800 lines to under 600 (scan plus local
fixture runner); tests from about 11,200 to a few hundred.

## 4. Migration plan (side by side)

Rule throughout: `main` and its dispatcher, launchers and `worktrees/codex|gov|auto` are not touched.

0. **Now.** This proposal on branch `slim-governance`, draft PRs, no merge.
   The slim work uses its own worktrees under `worktrees/tticom/slim-*`.
1. **Wait for the drain.** Let the live task (CFW-04) and any queued
   authority work finish on the old framework. Do not start slim work that
   needs `ORCHESTRATION_STATE.json`.
2. **Additive build (on the slim branch only).** Add: `TASKS.md` seeded from
   the authority backlog (read only, one-off script), the new CI workflow
   under a different file name (`ci-slim.yml`), a one-page `CLAUDE.md-slim`,
   and the PR template. Delete nothing.
3. **Trial.** Run two or three real tasks end to end under the slim flow in
   the slim worktree, branching from product `main`, PR branches prefixed
   `slim/`. Check beforehand with a dry run that the old dispatcher and audit
   do not treat an unknown `slim/` PR as a blocker (the old system fails
   closed on PRs it does not know; see GOV-03 and the 2026-09-24 report).
4. **Decide.** Maintainer reviews trial results: defects caught by CI vs by
   review, time per task, any near-miss on the five protections.
5. **Cutover PR (on `main`, by the maintainer, after approval).** Freeze the
   authority file into `docs/history/`, remove dispatcher, scripts and tests
   in step S1-S4, S6, S8, S11, collapse `projects/score2gp/` to requirements,
   ADRs, incidents and research, replace root rule files, switch CI.
   Retire old role accounts after the last merge.
6. **Skills repo.** Release the slimmed skills under a new tag; pin the cutover
   to it (see the companion proposal).
7. **Going private.** Separate step: check upstream licences for derived
   skills, rotate any credential that ever appeared in logs, decide history
   policy, review that no private fixture appears anywhere in history
   (history is currently public).

Rollback at any step before 5: close the slim PRs; `main` never changed.

## 5. Skills

See `agentops-claude-skills` `SLIM-PROPOSAL.md` section 4. In short: 12 skills
become 6 (`implement`, `review` with an adversarial mode, `address-review`,
`safe-git`, `workspace-cleanup`, `durable-handoff`); `dispatch-task`,
`governance-author`, `governed-development-loop`, `publish-pr-handback` retire.

## 6. Open questions for the maintainer

1. Is it acceptable that "no self-approval" becomes "agents cannot merge and
   the maintainer merges", with independent review optional and advisory? Or
   do you want review required for every PR (more protection, more cost)?
2. Private repos: does your GitHub plan enforce rulesets on private
   repositories? On a free plan it does not, so protection against direct
   main pushes would need an agent token that cannot push to main at all (or
   a local hook). Which plan and which token approach?
3. Should the five lasting ADRs/incidents/research notes be kept in the
   product repo or moved to a separate notes repo before going private?
4. Is `TASKS.md` enough, or do you want GitHub issues/Projects as the list?
5. History: keep full public history when going private, or start a fresh
   history? Public history contains 750 PRs of agent logs.
6. Real-fixture checks: must they remain local to your machine, or should a
   private CI runner be set up?
7. Should the old accounts (`tticom-automation`, `tticom-codex`,
   `tticomgov-code`) be retired or kept for optional independent review?
8. How aggressive on archiving: delete the 600+ per-task files at cutover, or
   move them to an `archive/` branch or tag?
9. Are the derived skills (`code-review`, `verified-implementation`, from the
   upstream collection) licence-compatible with a private, all-rights-reserved
   repo?
10. Is it acceptable for the old dispatcher to be switched off entirely at
    cutover, i.e. no `go`/`got` command afterwards?
