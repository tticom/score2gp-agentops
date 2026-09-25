# PLAN-01 — Single coherent backlog, with research tasks per requirement

- **Status**: PROMOTED (the `task` in `ORCHESTRATION_STATE.json`, authority revision 50; promoted at revision 48 and amended at revisions 49 and 50). Executable by the implementation role.
- **Repository**: `tticom/score2gp-agentops`
- **Branch**: `feat/plan-01-single-coherent-backlog`
- **Owner Role**: `implementation` (governance-repository task, as WIN-04)
- **Reviewer Role**: `reviewer`
- **Delivery Action**: `pull_request`
- **Prerequisites**: tticom/score2gp-agentops#695 (requirements register, REQ-0001 to REQ-0003) merged

## 1. Requirement and authority

Maintainer direction, 2026-09-25: "Producing a coherent single backlog is one of the highest priorities now and should become a dispatchable task, so should the research that will need to be done to fulfil each requirement." The control plane is meant to run a full SDLC with gates, so that the correct product is produced accurately. Accuracy outranks speed, and the number of review rounds is irrelevant.

## 2. Current verified state (agentops `5ce2547`, product `71535f3`)

After L3-01, the task authority is empty: `next_task_proposal` is null and `queued_task_proposals` is empty. Planned work is spread across sources that overlap and conflict. Each of the following must be accounted for:

| Source | Content | Problem |
|---|---|---|
| `plans/2026-08-19-native-pdf-to-gp-and-audiveris-retirement.md` §16 | NPG-00A to NPG-09C | Partly superseded by REC (see its supersession ledger) |
| `plans/2026-09-05-lesson3-native-working-slice.md` | L3 checkpoints to L3-NATIVE | Only L3-00/L3-01 exist as tasks |
| `tasks/2026-08-27-recognition-architecture-backlog.md` | REC-06 to REC-14 | A sub-folder backlog, which `TASK_RECORDING_CONVENTION.md` forbids |
| `tasks/*.md` (other), `programmes/*.md` | Earlier backlogs and programmes | Superseded; never reconciled |
| `PLANNING_DATA.md` | June-era queue, Tasks 7–78+ and proposals | Declared a backlog location, but read by no script |
| `plan/backlog.yaml`, `.agy/` | AGY (Antigravity) cycle backlog | AGY is no longer used (maintainer, 2026-09-25) |
| `plans/2026-08-04-multimodal-audio-score-platform-roadmap.md` | TSK-101 to TSK-604, programme repos `score2gp-{core,vector-parser,exporter,audio,cloud}` | Future programmes. The repositories exist and are kept |
| `requirements/` (after #695) | REQ-0001 to REQ-0003, with proposed OUT-00 to OUT-07 | Not yet in the authority |
| 2026-09-25 architect research (summarised in §4) | FND, GOV, TOP, RHY, TAB, FUS, SYM, CMP, VER, MSG epics | Exists only in session output |

## 3. Goal

Produce **one** backlog that is the single source of planned work, and make every item traceable and dispatchable in order.

1. **One authority.** The backlog lives in `ORCHESTRATION_STATE.json`. Promotable tasks keep the existing proposal schema. Items not yet detailed enough to promote go in a new top-level `backlog` list with a light schema (below). `ACTIVE_TASK.md` stays generated.
2. **Traceability.** Every item cites the requirement ID(s) it delivers (REQ-xxxx, and U01–U14 obligations where relevant) or a named control-plane need. Every requirement not yet `VERIFIED` has at least one item.
3. **Research per requirement.** Every requirement below `ACCEPTED` has a dispatchable research task (`RES-<REQ>`). Its deliverable is the requirement's research sections, open questions and acceptance criteria, in the form REQ-0002 uses.
4. **Ordering.** Items carry dependencies and a priority rank. The ready frontier (status `READY`, all dependencies terminal) can be computed mechanically.
5. **Supersession.** Every item in every source in §2 is marked, in a supersession table in the PR, as absorbed (with its new ID), superseded (by which ID), done (with evidence), or dropped (with reason). Nothing is silently lost.
6. **One home afterwards.** The superseded backlog sources (`PLANNING_DATA.md`, `tasks/*.md` backlogs, `programmes/`, `plan/`, `.agy/`) are removed. Their history stays in git. `TASK_RECORDING_CONVENTION.md` and the governance `README.md` describe the single method, with no contradictions.

Light backlog item schema (minimum): `id`, `title`, `requirements` (list), `kind` (`research` | `implementation` | `governance` | `decision`), `repository`, `status` (`IDEA` | `NEEDS_RESEARCH` | `NEEDS_DETAIL` | `READY` | `PROMOTED` | `DONE` | `DROPPED`), `priority` (integer rank), `depends_on` (list of IDs), `notes`. Promotion converts an item to the full proposal schema.

## 4. Inputs that must appear in the backlog

The ordering below is the maintainer-endorsed starting point (2026-09-25). The task may refine it with evidence.

- **P0**
  - L3-01 completion (PR #464).
  - GOV-03, dispatcher PR discovery and fail-closed binding (queued with this proposal).
  - OUT-01, containment of fabricated GP6/GP8 output (REQ-0002).
- **P1, measurement integrity** (REQ-0001 U13/U14):
  - remove the pytest-conditional GPIF serializer (`src/score2gp/gpif.py:149`);
  - replace silent ScoreIR clamps with rejection (`ir.py:99,268,516-528`; `gpif.py:833`);
  - one independent oracle. Extend the stdlib reader to repeats and alternate endings, sections, chord diagrams, grace notes, ties, tuplets, slides, hammer-on/pull-off, bends, vibrato, accents and mutes. Compare normalized play order;
  - durable adjudicated oracle manifests in the private corpus;
  - acceptance reproducible on CI, not only with the Windows file-lock provider;
  - a Windows full-suite quarantine or fix for the 16 pre-existing failures.
- **P2, L3-NATIVE critical path** (REQ-0001):
  - topology contract seam;
  - one shared primitive recogniser for noteheads, stems and beams, using painted-contour contact;
  - rhythm, TAB-token and pitch lanes;
  - a bounded per-measure resolver;
  - MusicalDocument → ScoreIR mapping;
  - deterministic GP reference allocation and validators;
  - Lesson 3 slices (system, page, document);
  - Guitar Pro 8 round-trip protocol;
  - anti-overfitting controls.
  Reconcile with REC-06 to REC-14 and NPG IDs; don't duplicate them.
- **P3, breadth** (REQ-0001 U03/U08/U09):
  - barline kinds and repeats with alternate endings (`Ex 2 Hands Up`; baseline 17 detected measures against 11);
  - the technique set in `Can't Find My Way Home`;
  - Lessons 4–7;
  - other engravers;
  - a held-out source policy.
- **P4:** REQ-0002 OUT-00 and OUT-02 to OUT-05 (GP8 first, then GP7). OUT-06/07 (GP5/GP6) are recorded but deferred.
- **Control plane:**
  - governance repository cleanup of superseded record directories (`runs/`, `reviews/`, `handoffs/`, `decisions/`, `archive/`, `audits/`, unreferenced `prompts/next` files), keeping anything a live document cites;
  - skills consolidation. Agents load skills from `.agents` folders. Target is one skills repository (`agentops-claude-skills`), one control-plane repository and product repositories. `agy-skills` is mined for anything useful, then deleted with explicit maintainer confirmation;
  - workspace layout: single instances of private-fixtures, agentops and claude-skills, linked by junction into identity worktrees; product repositories in isolated worktrees;
  - removal of AI artifacts from product repositories (`CLAUDE.md`, `AGENTS.md`, `HANDOFF.md`, `docs/agents/`, `docs/agentops.md`), but only after a workspace-level replacement is loaded from the linked control plane;
  - a **test-adequacy verification** capability (below);
  - tests/test_scoreir_gpif_compiler_refactor.py `_ensure_fixture` writes Lesson-6_{unowned,invalid}_artifact.json into the private corpus (score2gp-private-fixtures/fixtures/private). Tests must never write into the corpus; use tmp_path. Observed repeatedly, 2026-09-25.
  - FND-06 urgency: the 16 known Windows host failures make a zero-exit local full suite impossible, and the devils-advocate reviewer withholds verdicts (#465 re-review, 2026-09-25). Quarantine by exact ID with linked issues, or fix them.
  - **stale review contract.** `CLAUDE.md` and `AGENTS.md` require the reviewer dispatcher to return `REVIEW_CURRENT_HEAD` with `review_skill`, `review_skill_path` and `review_publisher_path`. Since WIN-01 (2026-09-23) the dispatcher emits only Orca `score2gp_bounded_worker` assignments, which have none of those fields. Reviewers correctly refuse. The contract and the implementation must be reconciled: either the assignment carries the pinned skill and publisher paths, or the rules change. Observed 2026-09-25;
  - **durable headless review launcher.** Unattended reviews must not depend on an interactive session. On this host the Codex workspace-write sandbox protects `.git` and cannot be elevated headlessly (`0xC0000142`), and cannot read the Windows keyring. A working pattern exists (2026-09-25):
    - run the reviewer dispatcher and every git-metadata write outside the sandbox, as the reviewer identity;
    - pass a process-scoped `GH_TOKEN`;
    - hand Codex a detached review worktree at the exact head and the SKILLS_LOCK skills checkout;
    - Codex only inspects, tests and publishes.
    It lives only in a session scratchpad. Make it versioned, OS-agnostic (Python) tooling, triggered automatically after each exact-head author handback. The maintainer does not want to request reviews.
- **Decisions to record:**
  - reconcile ADR-006 and product ADR-0004 into one ADR. Maintainer (2026-09-25): observed TAB positions are authoritative ("Position is the TAB's super power"). Inference applies only to notation-only notes, is labelled with provenance, and never overrides TAB;
  - one ADR register location;
  - REQ-0003 dependency licence audit and the PDF-library decision.
- **Later programmes:** multimodal roadmap items (audio → TAB transcription is the maintainer's long-term vision), recorded with status `IDEA` against their programme repositories.

**Test-adequacy verification.** Maintainer question, 2026-09-25: do we need a verifier that checks that tests exercise the intended behaviour and are fit for purpose, rather than being written to pass the code as it stands? The backlog item must cover:
1. traceability from requirement and acceptance criterion to test;
2. mutation testing of changed production code (a mutant that survives the task's tests is a finding);
3. mandatory negative controls for new checks;
4. an audit that no expected value is copied from production output;
5. a reviewer skill in the skills repository that runs these and reports adequacy separately from pass/fail.

## 5. Non-goals

- No product code changes.
- No promotion of any task other than recording statuses. Governance promotes.
- No deletion of any GitHub repository.
- No change to review, merge or identity rules.

## 6. Allowed paths

- `projects/score2gp/ORCHESTRATION_STATE.json` and the generated `projects/score2gp/ACTIVE_TASK.md`
- `projects/score2gp/PLANNING_DATA.md`, `projects/score2gp/tasks/**`, `projects/score2gp/programmes/**`, `plan/**`, `.agy/**` (removal only)
- `projects/score2gp/TASK_RECORDING_CONVENTION.md`, `README.md`, `projects/score2gp/README.md`, `projects/score2gp/requirements/**`
- `projects/score2gp/prompts/next/res-*.md` (new research task prompts)
- `scripts/score2gp_orca_control.py`, `scripts/score2gp_orchestrator.py`, and their tests, only to validate the `backlog` list and compute the ready frontier
- `scripts/agy_cycle.py`, `scripts/agy_spec_job.py`, `docs/agy-*.md`, `docs/spec-job-orca.md`, `requirements-agy-cycle.txt`, `tests/test_agy_*.py` (removal only, if nothing live depends on them)
- `.github/workflows/governance-control-plane.yml`, only to remove AGY-only steps and arguments; keep every other step. Its install step runs `python -m pip install pytest -r requirements-agy-cycle.txt` and its compile step runs `python -m py_compile scripts/score2gp_orca_control.py scripts/score2gp_dispatch.py scripts/agy_cycle.py`, so removing the AGY tooling fails CI, while keeping it fails acceptance 4 because `scripts/agy_cycle.py` names `plan/backlog.yaml`. `requirements-agy-cycle.txt` holds only `PyYAML>=6.0`, and only `scripts/agy_cycle.py` and `scripts/agy_spec_job.py` import `yaml`, so the install step may drop the requirements file; it must install PyYAML directly if any remaining script or test imports `yaml`. (Governance amendment, authority revision 49.)
- **Queue-instruction reconciliation only.** In these files, change only text that directs work into a queue or backlog other than the authority:
  - `projects/score2gp/plans/**`, `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ORCA_WORKFLOW.md`;
  - `projects/score2gp/skills/**`, `skills/**`, `projects/prompts/**`, `.agents/agents/project-director/agent.json`;
  - `projects/score2gp/prompts/*.md` (not `prompts/next/`), `docs/**`;
  - `AGENT-RULES.md`, `.agents/skills/**`, `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md` (governance amendment, authority revision 50).
  Review 5317328303 found that the multimodal roadmap (lines 73–75) still routes tasks into `PLANNING_DATA.md`.
  Review 5322160552 found that the acceptance 4 oracle matches only fixed phrases, so a differently worded claim ("This document is the product backlog") escapes it. The broadened oracle finds live queue instructions in `AGENT-RULES.md` line 57 (Orchestrator: "Must maintain the queue state and dependency graph."), `.agents/skills/score2gp-remediation-governance/SKILL.md` lines 3 and 25 ("the master remediation backlog", "dependency backlog", "the older M6 backlog"; PLAN-01 removes both backlog files) and `.agents/skills/score2gp-report-consolidation/SKILL.md` line 25 ("Commit and push the consolidated report and recovery programme backlog."), and `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md` line 10 ("- Informative only: queues, plans, reports, research, handoffs, task lists, and"), which names queues and task lists without referring to the authority.
- `projects/score2gp/prompts/next/agy-*.md` (removal only: AGY is retired)
- `tests/test_governance_audit.py` or a new `tests/test_single_backlog.py`, for the queue-claim search oracle

## 7. Acceptance

1. `ORCHESTRATION_STATE.json` holds every planned item, either as a proposal or as a `backlog` item. A test validates the backlog schema, rejects duplicate IDs, unknown dependencies and dependency cycles, and computes the ready frontier.
2. Every requirement in `requirements/` below `VERIFIED` is referenced by at least one item. Every requirement below `ACCEPTED` has a `RES-` research task with a prompt file. A test enforces both.
3. The PR includes a supersession table covering every item in every §2 source, each with a disposition. A reviewer can check any source item against it.
4. After the change, no **live** file directs work into, or claims to be, a backlog or queue other than `ORCHESTRATION_STATE.json` and its generated view.
   - A test runs the search oracle: patterns including `PLANNING_DATA`, `backlog.yaml`, `Approved Task Queue` and "queued in".
   - It fails on any match outside an explicit, reviewed exemption list.
   - The exemption list may contain only historical records, by **class**, each with a one-line reason:
     - **(a) dated record directories**, which describe past state and never instruct: `projects/score2gp/{runs,reviews,research,reports,decisions,handoffs,archive,audits}/**`. Review 5317954117 found matches in all four of the first set;
     - **(b)** prompts of tasks listed in `completed_tasks`, and the numbered legacy prompts `projects/score2gp/prompts/next/[0-9][0-9][0-9][0-9]-*.md` from before the authority existed;
     - **(c)** `docs/cycle-preparation-history/**`;
     - **(d)** by name only, `prompts/next/plan-01-single-coherent-backlog.md` and `prompts/next/gov-03-active-task-pr-discovery.md`, which name the superseded sources in order to retire them.
     - **(e)** by name only, the authority and its oracle: `projects/score2gp/ORCHESTRATION_STATE.json` and its generated view `projects/score2gp/ACTIVE_TASK.md` (they list superseded sources in PLAN-01's `allowed_paths` while the task is proposed or promoted), and the oracle test file itself (it must contain the patterns). Review of 186afd7 found these matches.
   - The test encodes these classes literally. A match in any other path fails, including a new file added to an exempt class's *parent* directory.
   - The separate record-directory cleanup (§4, control plane) may later remove class (a) content. This exemption does not depend on it.
5. `TASK_RECORDING_CONVENTION.md` and the governance `README.md` describe the same single method, with no contradictory rules.
6. The dispatcher's behaviour for the current task is unchanged (a characterization test against the pre-change resolution).
7. `python -m pytest` and `python scripts/score2gp_governance_audit.py` pass. `git diff --check` is clean.

## 8. Validation commands

```text
python -m pytest
python scripts/score2gp_governance_audit.py
python scripts/score2gp_dispatch.py --product ../score2gp --agentops . --json
git diff --check
```

## 9. Stop conditions

- `source_item_unaccounted` (any item in a §2 source without a disposition)
- `dispatcher_behaviour_changed_for_current_task`
- `product_edit_required`
- `repository_deletion_required`
- `requirement_without_backlog_item`

## 10. Incremental progress check

- **Baseline:** an empty authority queue and nine disagreeing planning sources.
- **New state:** one authority with a computable ready frontier, full requirement traceability, and research tasks per requirement.
- **Must not merely repeat:** the architect research summary. The deliverable is machine-validated authority, not a document.
- **Enables:** governance can promote the ready frontier directly, with no further planning step.
